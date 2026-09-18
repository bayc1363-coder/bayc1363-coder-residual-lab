export type SearchHit = {
  title: string;
  url: string;
  snippet: string;
};

export type SearchProvider = "tavily" | "brave" | "duckduckgo" | "wikipedia" | "none";

export type SearchBundle = {
  provider: SearchProvider;
  query: string;
  hits: SearchHit[];
  notes: string;
  missedTerms: string[];
};

const UA = "FrameLab/1.0 (research demo; equal-res chat)";
const NOTE_CAP = 3800;
const FETCH_MS = 8000;
const STOP = new Set([
  "what",
  "who",
  "where",
  "when",
  "why",
  "how",
  "is",
  "are",
  "was",
  "were",
  "does",
  "do",
  "did",
  "can",
  "the",
  "a",
  "an",
  "of",
  "and",
  "or",
  "to",
  "in",
  "on",
  "for",
  "with",
  "about",
  "that",
  "this",
  "from",
  "into",
  "please",
  "tell",
  "explain",
  "now",
  "latest",
  "current",
  "status",
  "seeing",
]);

export function getSearchProvider(): Exclude<SearchProvider, "none"> {
  if (process.env.TAVILY_API_KEY?.trim()) return "tavily";
  if (process.env.BRAVE_API_KEY?.trim()) return "brave";
  return "duckduckgo";
}

export function searchHintLabel(provider?: string) {
  if (provider === "tavily") return "Tavily web";
  if (provider === "brave") return "Brave web";
  if (provider === "wikipedia") return "Wikipedia";
  if (provider === "none") return "No hits";
  return "Live web";
}

export function mergeSearchBundles(base: SearchBundle, extra: SearchBundle): SearchBundle {
  const hits = uniqueHits([...base.hits, ...extra.hits]);
  const provider = extra.hits.length
    ? extra.provider
    : base.provider !== "none"
      ? base.provider
      : extra.provider;
  const terms = distinctiveTerms(base.query || extra.query);
  const matched = preferRelevant(hits, terms);
  const used = matched.length ? matched : hits;
  const missed =
    matched.length > 0 ? [] : terms.filter((term) => !mentions(used, term));
  return bundle(provider, base.query || extra.query, used.slice(0, 8), missed);
}

export async function retrieveNotes(rawQuery: string): Promise<SearchBundle> {
  const query = rawQuery.trim().replace(/\s+/g, " ").slice(0, 240);
  if (query.length < 3) {
    return { provider: "none", query, hits: [], notes: "", missedTerms: [] };
  }

  try {
    const planned = planQueries(query);
    const batches = await Promise.all(
      planned.map((item) => searchWeb(item).catch(() => empty(item)))
    );
    const provider =
      batches.find((item) => item.hits.length && item.provider !== "none")
        ?.provider ?? batches[0]?.provider ?? "none";
    const merged = uniqueHits(batches.flatMap((item) => item.hits));
    const terms = distinctiveTerms(query);
    const matched = preferRelevant(merged, terms);
    const used = matched.length ? matched : merged;
    const missed =
      matched.length > 0
        ? []
        : terms.filter((term) => !mentions(merged, term));
    return bundle(provider, query, used.slice(0, 6), missed);
  } catch {
    return { provider: "none", query, hits: [], notes: "", missedTerms: distinctiveTerms(query) };
  }
}

export function formatSearchSystem(bundle: SearchBundle): string {
  const lines = [
    "You do not have a Google / live-browse tool in this session.",
    "The server ran a live web retrieve for the user message and is giving you the excerpts below.",
    "Say that plainly if asked: these are retrieved excerpts, not a search you conducted.",
    "Name a title only when you lean on that excerpt. Do not invent sources or URLs.",
    "If a named person, theory, paper, or claim is missing from the excerpts, say so. Do not treat a nearby generic page as if it were that named work.",
    "Allocate each usable excerpt to Frame A or Frame B. Prestige/science pages must not colonize both frames.",
    "If every usable excerpt sits in one register, Residual says in one line that the retrieved corpus is one-sided. Do not turn Residual into a second literature review in A's voice, and do not crush a retrieved source-register page into one bullet inside A.",
    "If the user named a system, Frame A inhabits that system in its own terms even when search is prestige-heavy. Frame B is the strongest rival reading — not a second outsider gloss that splits the object against itself.",
  ];

  if (bundle.missedTerms.length) {
    lines.push(
      `NONE of the retrieved pages mention: ${bundle.missedTerms.join(", ")}. State that immediately. Do not invent that named subject.`
    );
  }

  if (!bundle.notes) {
    lines.push(
      `Live web retrieve for “${bundle.query}” returned no usable pages. Answer from uncertainty, not from a fabricated source list.`
    );
    return lines.join("\n");
  }

  lines.push("", `## Retrieved notes (${bundle.provider})`, bundle.notes);
  return lines.join("\n");
}

export function planQueries(text: string): string[] {
  const q = text.trim().replace(/\s+/g, " ").slice(0, 240);
  const out = [q];
  const stripped = q
    .replace(
      /^(what|who|where|when|why|how|is|are|was|were|does|do|can|tell me|explain)\b[\s:,-]*/i,
      ""
    )
    .replace(/\?+$/g, "")
    .trim();
  if (stripped && stripped.toLowerCase() !== q.toLowerCase() && stripped.length >= 4) {
    out.push(stripped);
  }
  return uniqueStrings(out).slice(0, 2);
}

export function distinctiveTerms(query: string): string[] {
  const possessives = [...query.matchAll(/\b([A-Za-z][A-Za-z0-9]+)['’]s?\b/g)].map((m) =>
    m[1].toLowerCase()
  );
  const quoted = [...query.matchAll(/"([^"]{2,80})"/g)].map((m) => m[1].toLowerCase());
  const strong = new Set<string>([...possessives]);
  for (const phrase of quoted) {
    for (const part of phrase.split(/\s+/)) {
      if (part.length > 2 && !STOP.has(part)) strong.add(part);
    }
  }
  const words = query.replace(/['’]s?\b/g, " ").split(/[^A-Za-z0-9]+/).filter(Boolean);
  words.forEach((word, index) => {
    if (STOP.has(word.toLowerCase())) return;
    if (index > 0 && word[0] === word[0].toUpperCase() && /[A-Za-z]/.test(word[0]) && word.length > 1) {
      strong.add(word.toLowerCase());
    }
  });
  if (strong.size) return [...strong];
  return words
    .map((word) => word.toLowerCase())
    .filter((word) => word.length > 3 && !STOP.has(word));
}

async function searchWeb(query: string): Promise<SearchBundle> {
  const tavily = process.env.TAVILY_API_KEY?.trim();
  if (tavily) return searchTavily(query, tavily);
  const brave = process.env.BRAVE_API_KEY?.trim();
  if (brave) return searchBrave(query, brave);
  try {
    return await searchDuckDuckGo(query);
  } catch {
    return searchWikipedia(query);
  }
}

async function searchTavily(query: string, apiKey: string): Promise<SearchBundle> {
  const response = await fetchWithTimeout("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      query,
      search_depth: "basic",
      max_results: 6,
      include_answer: false,
    }),
  });
  if (!response.ok) throw new Error(`Tavily ${response.status}`);
  const json = (await response.json()) as {
    results?: { title?: string; url?: string; content?: string }[];
  };
  const hits = (json.results ?? [])
    .map((row) => ({
      title: clean(row.title) || hostname(row.url),
      url: row.url?.trim() || "",
      snippet: clean(row.content).slice(0, 420),
    }))
    .filter((hit) => hit.url && hit.snippet);
  return bundle("tavily", query, hits, []);
}

async function searchBrave(query: string, apiKey: string): Promise<SearchBundle> {
  const url = new URL("https://api.search.brave.com/res/v1/web/search");
  url.searchParams.set("q", query);
  url.searchParams.set("count", "6");
  const response = await fetchWithTimeout(url, {
    headers: {
      Accept: "application/json",
      "X-Subscription-Token": apiKey,
    },
  });
  if (!response.ok) throw new Error(`Brave ${response.status}`);
  const json = (await response.json()) as {
    web?: { results?: { title?: string; url?: string; description?: string }[] };
  };
  const hits = (json.web?.results ?? [])
    .map((row) => ({
      title: clean(row.title) || hostname(row.url),
      url: row.url?.trim() || "",
      snippet: clean(row.description).slice(0, 420),
    }))
    .filter((hit) => hit.url && hit.snippet);
  return bundle("brave", query, hits, []);
}

async function searchDuckDuckGo(query: string): Promise<SearchBundle> {
  const url = new URL("https://lite.duckduckgo.com/lite/");
  url.searchParams.set("q", query);
  const response = await fetchWithTimeout(url, {
    headers: {
      "User-Agent": UA,
      Accept: "text/html",
    },
  });
  if (!response.ok) throw new Error(`DuckDuckGo ${response.status}`);
  const html = await response.text();
  const hits = parseDuckLite(html);
  if (!hits.length) throw new Error("DuckDuckGo returned no results");
  return bundle("duckduckgo", query, hits, []);
}

async function searchWikipedia(query: string): Promise<SearchBundle> {
  const searchUrl = new URL("https://en.wikipedia.org/w/api.php");
  searchUrl.searchParams.set("action", "query");
  searchUrl.searchParams.set("list", "search");
  searchUrl.searchParams.set("srsearch", query);
  searchUrl.searchParams.set("srlimit", "4");
  searchUrl.searchParams.set("srprop", "snippet");
  searchUrl.searchParams.set("format", "json");
  searchUrl.searchParams.set("utf8", "1");

  const searchRes = await fetchWithTimeout(searchUrl, { headers: { "User-Agent": UA } });
  if (!searchRes.ok) throw new Error(`Wikipedia search ${searchRes.status}`);
  const searchJson = (await searchRes.json()) as {
    query?: { search?: { pageid: number; title: string; snippet?: string }[] };
  };
  const pages = searchJson.query?.search ?? [];
  if (pages.length === 0) {
    return { provider: "wikipedia", query, hits: [], notes: "", missedTerms: [] };
  }

  const extractUrl = new URL("https://en.wikipedia.org/w/api.php");
  extractUrl.searchParams.set("action", "query");
  extractUrl.searchParams.set("prop", "extracts|info");
  extractUrl.searchParams.set("exintro", "1");
  extractUrl.searchParams.set("explaintext", "1");
  extractUrl.searchParams.set("exsentences", "4");
  extractUrl.searchParams.set("inprop", "url");
  extractUrl.searchParams.set("pageids", pages.map((page) => page.pageid).join("|"));
  extractUrl.searchParams.set("format", "json");
  extractUrl.searchParams.set("utf8", "1");

  const extractRes = await fetchWithTimeout(extractUrl, { headers: { "User-Agent": UA } });
  if (!extractRes.ok) throw new Error(`Wikipedia extract ${extractRes.status}`);
  const extractJson = (await extractRes.json()) as {
    query?: {
      pages?: Record<string, { title?: string; extract?: string; fullurl?: string }>;
    };
  };

  const hits: SearchHit[] = pages
    .map((page) => {
      const detail = extractJson.query?.pages?.[String(page.pageid)];
      const snippet = clean(detail?.extract) || stripHtml(page.snippet ?? "");
      return {
        title: clean(detail?.title || page.title),
        url:
          detail?.fullurl ||
          `https://en.wikipedia.org/wiki/${encodeURIComponent(page.title.replace(/ /g, "_"))}`,
        snippet: snippet.slice(0, 420),
      };
    })
    .filter((hit) => hit.title && hit.snippet);

  return bundle("wikipedia", query, hits, []);
}

function parseDuckLite(html: string): SearchHit[] {
  const uniqueAnchors = [...new Set(html.match(/<a\b[^>]*result-link[^>]*>[\s\S]*?<\/a>/gi) ?? [])];
  const snippets = [...html.matchAll(/class=(['"])result-snippet\1[^>]*>([\s\S]*?)<\/td>/gi)].map(
    (match) => stripHtml(match[2])
  );

  const hits: SearchHit[] = [];
  uniqueAnchors.forEach((tag, index) => {
    const href = tag.match(/href=(['"])([\s\S]*?)\1/i)?.[2];
    const title = stripHtml(tag.replace(/^<a\b[^>]*>/i, "").replace(/<\/a>$/i, ""));
    const url = unwrapDuckHref(href ?? "");
    const snippet = snippets[index] ?? "";
    if (!url || !title || !/^https?:\/\//i.test(url)) return;
    if (/duckduckgo\.com$/i.test(hostname(url))) return;
    hits.push({ title, url, snippet: snippet.slice(0, 420) });
  });
  return uniqueHits(hits);
}

function unwrapDuckHref(href: string): string {
  let url = htmlUnescape(href).trim();
  if (url.startsWith("//")) url = `https:${url}`;
  try {
    const parsed = new URL(url);
    const target = parsed.searchParams.get("uddg");
    if (target) return target;
  } catch {
    return url;
  }
  return url;
}

function bundle(
  provider: SearchProvider,
  query: string,
  hits: SearchHit[],
  missedTerms: string[]
): SearchBundle {
  const lines: string[] = [];
  let used = 0;
  for (const [index, hit] of hits.entries()) {
    const block = `[${index + 1}] ${hit.title}\n${hit.url}\n${hit.snippet}`;
    if (used + block.length + 2 > NOTE_CAP) break;
    lines.push(block);
    used += block.length + 2;
  }
  return {
    provider,
    query,
    hits,
    notes: lines.join("\n\n"),
    missedTerms,
  };
}

function empty(query: string): SearchBundle {
  return { provider: "none", query, hits: [], notes: "", missedTerms: [] };
}

function preferRelevant(hits: SearchHit[], terms: string[]) {
  if (!terms.length) return hits;
  return hits.filter((hit) => terms.some((term) => mentions([hit], term)));
}

function mentions(hits: SearchHit[], term: string) {
  const needle = term.toLowerCase();
  return hits.some((hit) => `${hit.title} ${hit.snippet}`.toLowerCase().includes(needle));
}

function uniqueHits(hits: SearchHit[]) {
  const seen = new Set<string>();
  const out: SearchHit[] = [];
  for (const hit of hits) {
    const key = hit.url.replace(/\/+$/, "").toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(hit);
  }
  return out;
}

function uniqueStrings(values: string[]) {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const value of values) {
    const key = value.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(value);
  }
  return out;
}

async function fetchWithTimeout(input: URL | string, init: RequestInit = {}) {
  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), FETCH_MS);
  try {
    return await fetch(input, { ...init, signal: abort.signal, cache: "no-store" });
  } finally {
    clearTimeout(timer);
  }
}

function clean(value?: string) {
  return (value ?? "").replace(/\s+/g, " ").trim();
}

function stripHtml(value: string) {
  return clean(htmlUnescape(value.replace(/<[^>]+>/g, " ")));
}

function htmlUnescape(value: string) {
  return value
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#x27;|&apos;/gi, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)));
}

function hostname(url?: string) {
  try {
    return url ? new URL(url).hostname : "Source";
  } catch {
    return "Source";
  }
}
