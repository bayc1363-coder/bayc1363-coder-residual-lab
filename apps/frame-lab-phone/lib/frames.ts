export type FrameKind = "a" | "b" | "residual" | "audit" | "working";

export type ParsedFrame = {
  kind: FrameKind;
  title: string;
  body: string;
};

export type AuditScores = {
  thicknessA?: string;
  thicknessB?: string;
  collapseRisk?: string;
};

const HEADING =
  /^(?:#{1,3}\s*)?(?:(?:\*\*)?(Frame A|Frame B|Residual|Self-audit|Working answer)(?:\*\*)?)(?:\s*[—–-]\s*(.+?))?\s*$/i;

export function parseEqualResFrames(text: string): ParsedFrame[] | null {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const frames: ParsedFrame[] = [];
  let current: ParsedFrame | null = null;

  const flush = () => {
    if (current) {
      current.body = current.body.trim();
      frames.push(current);
      current = null;
    }
  };

  for (const line of lines) {
    const match = line.trim().match(HEADING);
    if (match) {
      flush();
      const label = match[1].toLowerCase();
      const kind: FrameKind =
        label === "frame a"
          ? "a"
          : label === "frame b"
            ? "b"
            : label === "residual"
              ? "residual"
              : label === "self-audit"
                ? "audit"
                : "working";
      const extra = match[2]?.replace(/\*+/g, "").trim();
      const title =
        kind === "a"
          ? extra
            ? `Frame A — ${extra}`
            : "Frame A"
          : kind === "b"
            ? extra
              ? `Frame B — ${extra}`
              : "Frame B"
            : kind === "residual"
              ? "Residual"
              : kind === "audit"
                ? "Self-audit"
                : "Working answer";
      current = { kind, title, body: "" };
      continue;
    }
    if (current) {
      current.body += (current.body ? "\n" : "") + line;
    }
  }
  flush();

  if (frames.some((frame) => frame.kind === "a" || frame.kind === "b")) {
    return frames;
  }
  return null;
}

export function parseAuditScores(body: string): AuditScores {
  const normalized = body.replace(/\s+/g, " ");
  const grab = (keys: string[]) => {
    for (const key of keys) {
      const match = normalized.match(
        new RegExp(`${key}\\s*[:=]\\s*([0-9]+(?:\\.[0-9]+)?)`, "i")
      );
      if (match) return match[1];
    }
    return undefined;
  };
  return {
    thicknessA: grab([
      "thickness-a",
      "thickness a",
      "thicknessA",
      "thick a",
      "thick-a",
    ]),
    thicknessB: grab([
      "thickness-b",
      "thickness b",
      "thicknessB",
      "thick b",
      "thick-b",
    ]),
    collapseRisk: grab([
      "collapse-risk",
      "collapse risk",
      "collapseRisk",
      "collapse",
    ]),
  };
}
