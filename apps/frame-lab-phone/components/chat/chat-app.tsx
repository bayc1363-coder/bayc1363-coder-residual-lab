"use client";

import { CLAIM_HYGIENE } from "@/lib/protocol";
import type { ChatMessage, StatusPayload, StreamEvent } from "@/lib/types";
import { useEffect, useRef, useState } from "react";
import { AuditGuide } from "./audit-guide";
import { Composer } from "./composer";
import { EmptyState } from "./empty-state";
import { HeaderBar } from "./header-bar";
import { MessageBubble } from "./message-bubble";

export function ChatApp() {
  const [equalRes, setEqualRes] = useState(true);
  const [search, setSearch] = useState(false);
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<StatusPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [guideOpen, setGuideOpen] = useState(false);
  const scroller = useRef<HTMLDivElement>(null);
  const runId = useRef(0);
  const abortRef = useRef<AbortController | null>(null);

  function resetChat() {
    runId.current += 1;
    abortRef.current?.abort();
    abortRef.current = null;
    setBusy(false);
    setMessages([]);
    setError(null);
    setDraft("");
  }

  useEffect(() => {
    fetch("/api/status")
      .then((res) => res.json())
      .then((data: StatusPayload) => setStatus(data))
      .catch(() =>
        setStatus({
          live: false,
          model: "frame-lab-mock",
          baseHost: "local",
          searchProvider: "wikipedia",
        })
      );
  }, []);

  useEffect(() => {
    const node = scroller.current;
    if (!node) return;
    node.scrollTo({ top: node.scrollHeight, behavior: "smooth" });
  }, [messages, busy]);

  async function send(text: string) {
    const content = text.trim();
    if (!content || busy) return;
    const thisRun = ++runId.current;
    abortRef.current?.abort();
    const abort = new AbortController();
    abortRef.current = abort;
    setDraft("");
    setError(null);
    const user: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content,
    };
    const assistantId = crypto.randomUUID();
    const history = [...messages, user];
    setMessages([
      ...history,
      { id: assistantId, role: "assistant", content: "", equalRes, search },
    ]);
    setBusy(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          equalRes,
          search,
          messages: history.map(({ role, content: body }) => ({
            role,
            content: body,
          })),
        }),
        signal: abort.signal,
      });
      if (!response.ok || !response.body) {
        throw new Error(`Chat route failed (${response.status})`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let assembled = "";
      let mode: ChatMessage["mode"] = "mock";
      let model = "frame-lab-mock";

      const apply = (next: string, extra?: Partial<ChatMessage>) => {
        assembled = next;
        setMessages((current) =>
          current.map((message) =>
            message.id === assistantId
              ? { ...message, content: next, mode, model, equalRes, search, ...extra }
              : message
          )
        );
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";
        if (runId.current !== thisRun) return;
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith("data:")) continue;
          const event = JSON.parse(trimmed.slice(5).trim()) as StreamEvent;
          if (event.type === "meta") {
            mode = event.mode;
            model = event.model;
            if (event.error) setError(event.error);
            apply(assembled, {
              search,
              sources: event.sources,
              searchProvider: event.searchProvider,
            });
          } else if (event.type === "sources") {
            apply(assembled, {
              search: true,
              sources: event.sources,
              searchProvider: event.searchProvider,
            });
          } else if (event.type === "delta") {
            apply(assembled + event.text);
          }
        }
      }
    } catch (err) {
      if (runId.current !== thisRun) return;
      if (err instanceof DOMException && err.name === "AbortError") return;
      const message = err instanceof Error ? err.message : "Send failed";
      setError(message);
      setMessages((current) =>
        current.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                content:
                  item.content ||
                  "The mock path could not finish that send. Try again — this demo is meant to stay up even without a key.",
                mode: "mock",
                equalRes,
              }
            : item
        )
      );
    } finally {
      if (runId.current === thisRun) {
        setBusy(false);
        abortRef.current = null;
      }
    }
  }

  return (
    <div className="flex min-h-dvh justify-center bg-black md:items-center md:p-6">
      <div className="lab-shell relative z-10 flex h-dvh w-full max-w-[390px] flex-col overflow-hidden md:h-[min(844px,calc(100dvh-48px))] md:rounded-[2.2rem] md:border md:border-white/10 md:shadow-[0_30px_80px_-32px_black]">
        <div className="lab-noise pointer-events-none absolute inset-0 z-0" />
        <div className="relative z-10 flex min-h-0 flex-1 flex-col">
          <HeaderBar
            equalRes={equalRes}
            onEqualRes={setEqualRes}
            search={search}
            onSearch={setSearch}
            status={status}
            onReset={resetChat}
            onOpenGuide={() => setGuideOpen(true)}
          />
          <div
            ref={scroller}
            className="min-h-0 flex-1 overflow-y-auto px-3 py-4"
          >
            {messages.length === 0 ? (
              <EmptyState onPick={send} />
            ) : (
              <div className="flex flex-col gap-4">
                {messages.map((message, index) => (
                  <MessageBubble
                    key={message.id}
                    message={message}
                    streaming={
                      busy &&
                      message.role === "assistant" &&
                      index === messages.length - 1
                    }
                    onOpenGuide={() => setGuideOpen(true)}
                  />
                ))}
              </div>
            )}
            {error ? (
              <p className="mt-3 px-1 text-[11px] leading-4 text-copper/90">
                Live path note: {error}. Showing mock so the demo stays up.
              </p>
            ) : null}
          </div>
          <Composer
            value={draft}
            onChange={setDraft}
            onSend={() => send(draft)}
            disabled={busy}
          />
          <p className="sr-only">{CLAIM_HYGIENE}</p>
        </div>
        <AuditGuide open={guideOpen} onClose={() => setGuideOpen(false)} />
      </div>
    </div>
  );
}
