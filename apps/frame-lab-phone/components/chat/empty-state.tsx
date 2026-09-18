const STARTERS = [
  "How did the Earth originate?",
  "Why should someone forgive?",
  "Why do markets crash?",
];

export function EmptyState({
  onPick,
}: {
  onPick: (prompt: string) => void;
}) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-5 pb-4">
      <div className="relative mb-8 h-28 w-32" aria-hidden>
        <span className="absolute top-2 left-2 h-[4.6rem] w-[4.6rem] rotate-[-16deg] rounded-2xl border-2 border-teal/70 bg-teal/15 shadow-[0_0_24px_oklch(0.8_0.1_185/0.18)]" />
        <span className="absolute top-3 left-10 h-[4.6rem] w-[4.6rem] rotate-[12deg] rounded-2xl border-2 border-copper/80 bg-copper/16 shadow-[0_0_24px_oklch(0.82_0.1_65/0.18)]" />
        <span className="absolute top-8 left-6 h-[4.6rem] w-[4.6rem] rounded-2xl border-2 border-dashed border-white/35 bg-white/6" />
      </div>
      <p className="font-serif text-[28px] leading-8 tracking-tight text-foreground">
        Hold rival frames.
      </p>
      <p className="mt-2 max-w-[280px] text-center text-[14px] leading-5 text-muted-foreground">
        Equal thickness. Residual included. Then a working answer — not a
        collapse onto one story. Leave the chat open to grow both frames.
        Tap ⓘ for Thick A / B and Collapse — self-audit, not a rating.
      </p>
      <div className="mt-6 flex w-full flex-col gap-2">
        {STARTERS.map((prompt) => (
          <button
            key={prompt}
            type="button"
            data-testid={`starter-${prompt}`}
            onClick={() => onPick(prompt)}
            className="min-h-12 rounded-2xl border border-white/8 bg-white/4 px-4 text-left text-[14px] text-foreground/90 transition active:scale-[0.99] active:bg-white/7"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
