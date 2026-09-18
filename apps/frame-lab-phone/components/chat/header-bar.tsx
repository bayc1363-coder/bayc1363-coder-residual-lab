"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { CLAIM_HYGIENE } from "@/lib/protocol";
import type { StatusPayload } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Info, RotateCcw } from "lucide-react";

export function HeaderBar({
  equalRes,
  onEqualRes,
  search,
  onSearch,
  status,
  onReset,
  onOpenGuide,
}: {
  equalRes: boolean;
  onEqualRes: (next: boolean) => void;
  search: boolean;
  onSearch: (next: boolean) => void;
  status: StatusPayload | null;
  onReset: () => void;
  onOpenGuide: () => void;
}) {
  const searchHint = hintForProvider(status?.searchProvider);

  return (
    <header
      className="sticky top-0 z-20 border-b border-white/6 bg-[#121018]/78 backdrop-blur-xl"
      style={{ paddingTop: "max(10px, env(safe-area-inset-top))" }}
    >
      <div className="flex items-center gap-2 px-3 pb-2">
        <div className="min-w-0 flex-1">
          <div className="flex items-baseline gap-2">
            <h1 className="font-serif text-[22px] leading-none tracking-tight">
              Frame Lab
            </h1>
            <Badge
              variant="outline"
              className="h-5 border-white/10 bg-white/4 px-1.5 text-[10px] font-normal text-muted-foreground"
            >
              Residual Lab
            </Badge>
          </div>
          <p className="mt-1 truncate text-[11px] text-muted-foreground">
            Equal-res chat · {status?.live ? status.model : "mock path"}
            {search ? ` · ${searchHint}` : ""}
          </p>
        </div>
        <div
          className={cn(
            "shrink-0 rounded-full px-2.5 py-1 text-[10px] font-medium tracking-wide uppercase",
            status?.live ? "bg-teal/15 text-teal" : "bg-copper/15 text-copper"
          )}
        >
          {status?.live ? "Live" : "Mock"}
        </div>
        <Button
          variant="ghost"
          size="icon-lg"
          aria-label="How to read the scores"
          data-testid="score-guide"
          onClick={onOpenGuide}
          className="text-muted-foreground"
        >
          <Info />
        </Button>
        <Button
          variant="ghost"
          size="icon-lg"
          aria-label="New chat"
          data-testid="new-chat"
          onClick={onReset}
          className="text-muted-foreground"
        >
          <RotateCcw />
        </Button>
      </div>

      <div className="grid grid-cols-2 gap-2 px-3 pb-3">
        <ToggleCard
          id="equal-res"
          testId="equal-res"
          title="Equal-res"
          subtitle={equalRes ? "Rival frames on" : "Plain model"}
          checked={equalRes}
          onCheckedChange={onEqualRes}
          accent="teal"
        />
        <ToggleCard
          id="web-search"
          testId="web-search"
          title="Search"
          subtitle={search ? searchHint : "Model only"}
          checked={search}
          onCheckedChange={onSearch}
          accent="copper"
        />
      </div>
      <button
        type="button"
        onClick={onOpenGuide}
        className="w-full px-3 pb-2 text-center text-[10px] tracking-wide text-muted-foreground/90 underline decoration-white/20 underline-offset-2"
      >
        {CLAIM_HYGIENE} · tap for scores
      </button>
    </header>
  );
}

function hintForProvider(provider?: string) {
  if (provider === "tavily") return "Tavily web";
  if (provider === "brave") return "Brave web";
  if (provider === "wikipedia") return "Wikipedia";
  return "Live web";
}

function ToggleCard({
  id,
  testId,
  title,
  subtitle,
  checked,
  onCheckedChange,
  accent,
}: {
  id: string;
  testId: string;
  title: string;
  subtitle: string;
  checked: boolean;
  onCheckedChange: (next: boolean) => void;
  accent: "teal" | "copper";
}) {
  return (
    <label
      htmlFor={id}
      className="flex min-h-11 items-center justify-between gap-2 rounded-2xl border border-white/8 bg-white/4 px-2.5"
    >
      <span className="min-w-0">
        <span className="block text-[13px] font-medium">{title}</span>
        <span className="block truncate text-[11px] text-muted-foreground">
          {subtitle}
        </span>
      </span>
      <Switch
        id={id}
        data-testid={testId}
        checked={checked}
        onCheckedChange={(value) => onCheckedChange(Boolean(value))}
        className={cn(
          checked && accent === "teal" && "data-checked:bg-teal",
          checked && accent === "copper" && "data-checked:bg-copper"
        )}
      />
    </label>
  );
}
