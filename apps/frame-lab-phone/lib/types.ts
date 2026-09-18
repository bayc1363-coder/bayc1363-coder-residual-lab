export type ChatRole = "user" | "assistant" | "system";

export type SourceHit = {
  title: string;
  url: string;
};

export type ChatMessage = {
  id: string;
  role: Exclude<ChatRole, "system">;
  content: string;
  mode?: ReplyMode;
  model?: string;
  equalRes?: boolean;
  search?: boolean;
  sources?: SourceHit[];
  searchProvider?: string;
};

export type ReplyMode = "live" | "mock" | "fallback";

export type StatusPayload = {
  live: boolean;
  model: string;
  baseHost: string;
  searchProvider: string;
};

export type StreamMeta = {
  type: "meta";
  mode: ReplyMode;
  model: string;
  error?: string;
  searchProvider?: string;
  sources?: SourceHit[];
};

export type StreamDelta = {
  type: "delta";
  text: string;
};

export type StreamSources = {
  type: "sources";
  searchProvider?: string;
  sources: SourceHit[];
};

export type StreamDone = {
  type: "done";
};

export type StreamEvent = StreamMeta | StreamDelta | StreamSources | StreamDone;
