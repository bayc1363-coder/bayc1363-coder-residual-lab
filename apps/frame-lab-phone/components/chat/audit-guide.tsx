"use client";

import { AUDIT_HELP, CLAIM_HYGIENE, SCORE_HELP } from "@/lib/protocol";

export function AuditGuide({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-black/60 p-3 pb-[max(12px,env(safe-area-inset-bottom))] md:items-center"
      onClick={onClose}
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="audit-guide-title"
        className="w-full max-w-[390px] rounded-[1.6rem] border border-white/10 bg-[#16141e] p-4 shadow-[0_24px_80px_-24px_black]"
        onClick={(event) => event.stopPropagation()}
      >
        <p className="text-[11px] tracking-[0.14em] text-muted-foreground uppercase">
          Frame Lab
        </p>
        <h2
          id="audit-guide-title"
          className="mt-1 font-serif text-[22px] leading-7 text-foreground"
        >
          How to read the scores
        </h2>
        <p className="mt-2 text-[14px] leading-5 text-muted-foreground">
          {AUDIT_HELP.body} Search, when on, does a live web retrieve. Excerpts
          should feed A and B; if the corpus is one-sided, Residual says so.
          Named theories stay intact in Frame A — do not split them against
          themselves. Scores are a self-check, not proof.
        </p>
        <ul className="mt-4 space-y-2">
          {Object.values(SCORE_HELP).map((item) => (
            <li
              key={item.label}
              className="rounded-2xl border border-white/8 bg-white/4 px-3 py-2.5"
            >
              <p className="text-[11px] font-medium tracking-[0.12em] text-teal uppercase">
                {item.label}
              </p>
              <p className="mt-0.5 font-serif text-[16px] text-foreground">
                {item.title}
              </p>
              <p className="mt-1 text-[13px] leading-5 text-muted-foreground">
                {item.body}
              </p>
            </li>
          ))}
        </ul>
        <p className="mt-3 text-center text-[11px] text-muted-foreground">
          {CLAIM_HYGIENE}
        </p>
        <button
          type="button"
          onClick={onClose}
          className="mt-3 min-h-12 w-full rounded-2xl bg-copper text-[15px] font-medium text-primary-foreground"
        >
          Close
        </button>
      </div>
    </div>
  );
}
