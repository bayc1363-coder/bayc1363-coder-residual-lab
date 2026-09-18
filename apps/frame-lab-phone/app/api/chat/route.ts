import { getApiKey, getBaseUrl, getModel } from "@/lib/config";
import { buildMockReply, sleep } from "@/lib/mock";
import { CONTINUE_FRAMES, EQUAL_RES_PROTOCOL } from "@/lib/protocol";
import {
  formatSearchSystem,
  mergeSearchBundles,
  retrieveNotes,
  type SearchBundle,
} from "@/lib/search";
import type { ChatRole, SourceHit, StreamEvent } from "@/lib/types";

export const dynamic = "force-dynamic";
export const maxDuration = 60;

type IncomingMessage = {
  role: ChatRole;
  content: string;
};

export async function POST(req: Request) {
  let payload: { messages?: IncomingMessage[]; equalRes?: boolean; search?: boolean };
  try {
    payload = await req.json();
  } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const messages = (payload.messages ?? []).filter(
    (message) =>
      (message.role === "user" || message.role === "assistant") &&
      typeof message.content === "string"
  );
  const equalRes = Boolean(payload.equalRes);
  const wantSearch = Boolean(payload.search);
  const lastUser = [...messages].reverse().find((message) => message.role === "user");
  if (!lastUser) {
    return Response.json({ error: "A user message is required." }, { status: 400 });
  }

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const send = (event: StreamEvent) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
      };

      let search = emptySearch(lastUser.content);
      if (wantSearch) {
        try {
          search = await retrieveNotes(lastUser.content);
        } catch {
          search = emptySearch(lastUser.content);
        }
      }
      const sources = toSources(search);

      const pumpMock = async (
        mode: "mock" | "fallback",
        error?: string
      ) => {
        send({
          type: "meta",
          mode,
          model: "frame-lab-mock",
          error,
          searchProvider: wantSearch ? search.provider : undefined,
          sources,
        });
        const text = buildMockReply(lastUser.content, equalRes);
        await streamText(text, send);
        send({ type: "done" });
      };

      const key = getApiKey();
      if (!key) {
        await pumpMock("mock");
        controller.close();
        return;
      }

      try {
        await streamLive({
          key,
          equalRes,
          wantSearch,
          messages,
          search,
          send,
        });
        send({ type: "done" });
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Live path failed";
        await pumpMock("fallback", message);
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}

function emptySearch(query: string): SearchBundle {
  return { provider: "none", query, hits: [], notes: "", missedTerms: [] };
}

function toSources(bundle: SearchBundle): SourceHit[] {
  return bundle.hits.map(({ title, url }) => ({ title, url }));
}

const WEB_SEARCH_TOOL = {
  type: "function" as const,
  function: {
    name: "web_search",
    description:
      "Run another live web retrieve. Use only when current excerpts miss a named person, theory, paper, or claim.",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Exact query, including the names the excerpts missed.",
        },
      },
      required: ["query"],
    },
  },
};

async function streamLive({
  key,
  equalRes,
  wantSearch,
  messages,
  search,
  send,
}: {
  key: string;
  equalRes: boolean;
  wantSearch: boolean;
  messages: IncomingMessage[];
  search: SearchBundle;
  send: (event: StreamEvent) => void;
}) {
  const model = getModel();
  const url = `${getBaseUrl()}/chat/completions`;
  let bundle = search;

  const continuing =
    equalRes &&
    messages.some(
      (message) =>
        message.role === "assistant" && /##\s*Frame A/i.test(message.content)
    );

  const chatMessages = (extra: Record<string, unknown>[] = []) => [
    ...(equalRes ? [{ role: "system" as const, content: EQUAL_RES_PROTOCOL }] : []),
    ...(continuing
      ? [{ role: "system" as const, content: CONTINUE_FRAMES }]
      : []),
    ...(wantSearch
      ? [{ role: "system" as const, content: formatSearchSystem(bundle) }]
      : []),
    ...messages.map((message) => ({
      role: message.role,
      content: message.content,
    })),
    ...extra,
  ];

  send({
    type: "meta",
    mode: "live",
    model,
    searchProvider: wantSearch ? bundle.provider : undefined,
    sources: toSources(bundle),
  });

  if (wantSearch) {
    try {
      const first = await streamCompletion({
        key,
        url,
        model,
        equalRes,
        messages: chatMessages(),
        useTools: true,
        send,
      });
      const query = first.toolQueries[0];
      if (query) {
        const extra = await retrieveNotes(query);
        bundle = mergeSearchBundles(bundle, extra);
        send({
          type: "sources",
          searchProvider: bundle.provider,
          sources: toSources(bundle),
        });
        const followUp = first.followUp.map((item) =>
          item.role === "tool"
            ? { ...item, content: extra.notes || "No usable pages for that follow-up query." }
            : item
        );
        await streamCompletion({
          key,
          url,
          model,
          equalRes,
          messages: chatMessages(followUp),
          useTools: false,
          send,
        });
      }
      return;
    } catch (error) {
      const message = error instanceof Error ? error.message : "";
      if (!message.startsWith("Upstream")) throw error;
    }
  }

  await streamCompletion({
    key,
    url,
    model,
    equalRes,
    messages: chatMessages(),
    useTools: false,
    send,
  });
}

async function streamCompletion({
  key,
  url,
  model,
  equalRes,
  messages,
  useTools,
  send,
}: {
  key: string;
  url: string;
  model: string;
  equalRes: boolean;
  messages: Record<string, unknown>[];
  useTools: boolean;
  send: (event: StreamEvent) => void;
}) {
  const body: Record<string, unknown> = {
    model,
    stream: true,
    temperature: equalRes ? 0.7 : 0.5,
    messages,
  };
  if (useTools) {
    body.tools = [WEB_SEARCH_TOOL];
    body.tool_choice = "auto";
  }

  const response = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const detail = (await response.text()).slice(0, 280);
    throw new Error(`Upstream ${response.status}${detail ? `: ${detail}` : ""}`);
  }
  if (!response.body) {
    throw new Error("Upstream returned an empty body.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  const toolCalls = new Map<number, { id: string; name: string; arguments: string }>();
  let emitted = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n");
    buffer = parts.pop() ?? "";
    for (const line of parts) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue;
      const data = trimmed.slice(5).trim();
      if (!data || data === "[DONE]") continue;
      try {
        const json = JSON.parse(data) as {
          choices?: {
            delta?: {
              content?: string;
              tool_calls?: {
                index?: number;
                id?: string;
                function?: { name?: string; arguments?: string };
              }[];
            };
          }[];
        };
        const delta = json.choices?.[0]?.delta;
        if (delta?.content) {
          emitted += delta.content;
          send({ type: "delta", text: delta.content });
        }
        for (const call of delta?.tool_calls ?? []) {
          const index = call.index ?? 0;
          const current = toolCalls.get(index) ?? { id: "", name: "", arguments: "" };
          if (call.id) current.id = call.id;
          if (call.function?.name) current.name = call.function.name;
          if (call.function?.arguments) current.arguments += call.function.arguments;
          toolCalls.set(index, current);
        }
      } catch {
        // ignore malformed chunks
      }
    }
  }

  const parsedCalls = [...toolCalls.values()].filter(
    (call) => call.name === "web_search" && call.id
  );
  const toolQueries = parsedCalls
    .map((call) => {
      try {
        const args = JSON.parse(call.arguments || "{}") as { query?: string };
        return args.query?.trim() ?? "";
      } catch {
        return call.arguments.trim();
      }
    })
    .filter((query) => query.length >= 3);

  const followUp: Record<string, unknown>[] = [];
  if (parsedCalls.length) {
    followUp.push({
      role: "assistant",
      content: emitted || null,
      tool_calls: parsedCalls.map((call) => ({
        id: call.id,
        type: "function",
        function: { name: call.name, arguments: call.arguments || "{}" },
      })),
    });
    for (const call of parsedCalls) {
      followUp.push({
        role: "tool",
        tool_call_id: call.id,
        content: `Search scheduled for follow-up retrieve. Use the updated retrieved notes.`,
      });
    }
  }

  return { toolQueries, followUp };
}

async function streamText(
  text: string,
  send: (event: StreamEvent) => void
) {
  const chunks = text.match(/\S+\s*/g) ?? [text];
  for (const chunk of chunks) {
    send({ type: "delta", text: chunk });
    await sleep(18);
  }
}
