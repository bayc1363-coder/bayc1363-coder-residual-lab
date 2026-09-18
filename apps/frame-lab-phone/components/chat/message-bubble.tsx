"use client";

import { parseAuditScores, parseEqualResFrames, type ParsedFrame } from "@/lib/frames";
import { AUDIT_HELP, SCORE_HELP } from "@/lib/protocol";
import type { ChatMessage } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Info } from "lucide-react";
import { Prose } from "./prose";

export function MessageBubble({
  message,
  streaming,
  onOpenGuide,
}: {
  message: ChatMessage;
  streaming?: boolean;
  onOpenGuide?: () => void;
}) {
  if (message.role === "user") {
    return (
      <div className="msg-in flex justify-end pl-10">
        <div className="rounded-[22px] rounded-br-md bg-linear-to-br from-copper to-[#c27a4a] px-3.5 py-2.5 text-[15px] leading-6 text-primary-foreground shadow-[0_10px_24px_-16px_oklch(0.6_0.12_70)]">
          <Prose text={message.content} />
        </div>
      </div>
    );
  }

  const frames =
    message.equalRes && !streaming
      ? parseEqualResFrames(message.content)
      : message.equalRes
        ? parseEqualResFrames(message.content)
        : null;

  return (
    <div className="msg-in flex justify-start pr-6">
      <div className="w-full max-w-[340px] space-y-2">
        <div className="flex flex-wrap items-center gap-1.5 px-1">
          <ModeChip
            mode={message.mode}
            equalRes={message.equalRes}
            search={message.search}
          />
          {streaming ? (
            <span className="text-[11px] tracking-wide text-muted-foreground/80">
              {message.search && !message.sources ? "searching" : "writing"}
            </span>
          ) : null}
        </div>
        {message.sources?.length ? (
          <SourceList
            sources={message.sources}
            provider={message.searchProvider}
          />
        ) : null}
        {frames ? (
          <div className="space-y-2">
            {frames.map((frame) => (
              <FrameCard
                key={frame.kind + frame.title}
                frame={frame}
                onOpenGuide={onOpenGuide}
              />
            ))}
          </div>
        ) : (
          <div className="rounded-[22px] rounded-bl-md border border-white/8 bg-white/4 px-3.5 py-3 text-foreground/92 shadow-[inset_0_1px_0_oklch(1_0_0/0.05)]">
            {message.content ? (
              <Prose text={message.content} />
            ) : (
              <TypingDots />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function ModeChip({
  mode,
  equalRes,
  search,
}: {
  mode?: ChatMessage["mode"];
  equalRes?: boolean;
  search?: boolean;
}) {
  const label =
    mode === "live" ? "Live" : mode === "fallback" ? "Fallback" : "Mock";
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-white/8 bg-black/20 px-2 py-0.5 text-[10px] font-medium tracking-wide text-muted-foreground uppercase">
      <span
        className={cn(
          "size-1.5 rounded-full",
          mode === "live" ? "bg-teal" : "bg-copper/80"
        )}
      />
      {label}
      {equalRes ? " · equal-res" : " · plain"}
      {search ? " · search" : ""}
    </span>
  );
}

function SourceList({
  sources,
  provider,
}: {
  sources: NonNullable<ChatMessage["sources"]>;
  provider?: string;
}) {
  return (
    <div className="rounded-2xl border border-white/8 bg-black/20 px-3 py-2">
      <p className="text-[10px] font-medium tracking-[0.14em] text-muted-foreground uppercase">
        Sources{provider && provider !== "none" ? ` · ${provider}` : ""}
        {" · retrieved excerpts"}
      </p>
      <ol className="mt-1.5 space-y-1">
        {sources.map((source, index) => (
          <li key={source.url} className="min-w-0 text-[12px] leading-4">
            <a
              href={source.url}
              target="_blank"
              rel="noreferrer"
              className="text-teal underline decoration-teal/30 underline-offset-2"
            >
              {index + 1}. {source.title}
            </a>
          </li>
        ))}
      </ol>
    </div>
  );
}

function FrameCard({
  frame,
  onOpenGuide,
}: {
  frame: ParsedFrame;
  onOpenGuide?: () => void;
}) {
  if (frame.kind === "audit") {
    const scores = parseAuditScores(frame.body);
    return (
      <div className="rounded-2xl border border-white/8 bg-black/20 px-3 py-2.5">
        <div className="mb-2 flex items-center justify-between gap-2">
          <p className="text-[11px] font-medium tracking-[0.14em] text-muted-foreground uppercase">
            Self-audit
          </p>
          <button
            type="button"
            onClick={onOpenGuide}
            className="inline-flex size-8 items-center justify-center rounded-full border border-white/10 bg-white/6 text-muted-foreground"
            aria-label="How to read the scores"
          >
            <Info className="size-3.5" />
          </button>
        </div>
        <div className="grid grid-cols-3 gap-1.5">
          <Score
            label={SCORE_HELP.thicknessA.label}
            hint={SCORE_HELP.thicknessA.body}
            value={scores.thicknessA}
            onOpen={onOpenGuide}
          />
          <Score
            label={SCORE_HELP.thicknessB.label}
            hint={SCORE_HELP.thicknessB.body}
            value={scores.thicknessB}
            onOpen={onOpenGuide}
          />
          <Score
            label={SCORE_HELP.collapse.label}
            hint={SCORE_HELP.collapse.body}
            value={scores.collapseRisk}
            onOpen={onOpenGuide}
          />
        </div>
        <ul className="mt-2 space-y-1 text-[11px] leading-4 text-muted-foreground">
          <li>
            <span className="text-foreground/80">Thick A</span> —{" "}
            {SCORE_HELP.thicknessA.body}
          </li>
          <li>
            <span className="text-foreground/80">Thick B</span> —{" "}
            {SCORE_HELP.thicknessB.body}
          </li>
          <li>
            <span className="text-foreground/80">Collapse</span> —{" "}
            {SCORE_HELP.collapse.body}
          </li>
        </ul>
        <p className="mt-2 text-[10px] text-muted-foreground/80">
          {AUDIT_HELP.body}
        </p>
        {!scores.thicknessA && !scores.thicknessB ? (
          <div className="mt-2 text-muted-foreground">
            <Prose text={frame.body} />
          </div>
        ) : null}
      </div>
    );
  }

  const tone =
    frame.kind === "a"
      ? "border-l-teal/80"
      : frame.kind === "b"
        ? "border-l-copper/80"
        : frame.kind === "residual"
          ? "border-dashed border-white/16 bg-transparent"
          : "border-l-foreground/40 bg-white/6";

  return (
    <section
      className={cn(
        "rounded-2xl border border-white/8 bg-white/4 px-3 py-2.5 border-l-[3px]",
        tone
      )}
    >
      <h3 className="mb-1.5 font-serif text-[15px] leading-5 text-foreground/95">
        {frame.title}
      </h3>
      <div className="text-foreground/88">
        <Prose text={frame.body} />
      </div>
    </section>
  );
}

function Score({
  label,
  hint,
  value,
  onOpen,
}: {
  label: string;
  hint: string;
  value?: string;
  onOpen?: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onOpen}
      className="rounded-xl bg-white/4 px-2 py-1.5 text-center"
      aria-label={`${label}: ${value ?? "no score"}. ${hint}`}
    >
      <div className="font-serif text-lg leading-none text-foreground">
        {value ?? "—"}
      </div>
      <div className="mt-1 text-[9px] tracking-[0.12em] text-muted-foreground uppercase">
        {label}
      </div>
    </button>
  );
}

export function TypingDots() {
  return (
    <div className="flex h-5 items-center gap-1 px-0.5" aria-label="Assistant is writing">
      <span className="typing-dot size-1.5 rounded-full bg-foreground/80" />
      <span className="typing-dot size-1.5 rounded-full bg-foreground/80" />
      <span className="typing-dot size-1.5 rounded-full bg-foreground/80" />
    </div>
  );
}
