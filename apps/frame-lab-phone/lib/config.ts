export function getApiKey() {
  return process.env.EXPLABS_API_KEY?.trim() || process.env.OPENAI_API_KEY?.trim() || "";
}

export function getModel() {
  return process.env.MODEL?.trim() || "deepseek-v4.1-flash";
}

export function getBaseUrl() {
  const raw =
    process.env.BASE_URL?.trim() ||
    process.env.OPENAI_BASE_URL?.trim() ||
    "https://api.experientiallabs.ai";
  return normalizeOpenAiBase(raw);
}

export function normalizeOpenAiBase(url: string) {
  const trimmed = url.replace(/\/+$/, "");
  return trimmed.endsWith("/v1") ? trimmed : `${trimmed}/v1`;
}

export function getBaseHost() {
  try {
    return new URL(getBaseUrl()).host;
  } catch {
    return "api.experientiallabs.ai";
  }
}
