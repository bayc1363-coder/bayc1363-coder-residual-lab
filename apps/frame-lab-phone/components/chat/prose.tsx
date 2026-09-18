export function Prose({ text }: { text: string }) {
  const blocks = text.replace(/\r\n/g, "\n").split(/\n{2,}/);
  return (
    <div className="space-y-2.5">
      {blocks.map((block, index) => {
        const lines = block.split("\n");
        const isList = lines.every((line) => /^\s*(?:[-*]|\d+\.)\s+/.test(line));
        if (isList) {
          return (
            <ul key={index} className="space-y-1 pl-4 text-[15px] leading-6">
              {lines.map((line, lineIndex) => (
                <li key={lineIndex} className="list-disc">
                  <Inline text={line.replace(/^\s*(?:[-*]|\d+\.)\s+/, "")} />
                </li>
              ))}
            </ul>
          );
        }
        const heading = block.match(/^(#{1,3})\s+(.+)$/);
        if (heading) {
          return (
            <h3 key={index} className="font-serif text-[16px] leading-5">
              <Inline text={heading[2]} />
            </h3>
          );
        }
        return (
          <p key={index} className="text-[15px] leading-6">
            {lines.map((line, lineIndex) => (
              <span key={lineIndex}>
                {lineIndex > 0 ? <br /> : null}
                <Inline
                  text={line.replace(/^(#{1,3})\s+/, "")}
                />
              </span>
            ))}
          </p>
        );
      })}
    </div>
  );
}

function Inline({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, index) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return (
            <strong key={index} className="font-medium text-foreground">
              {part.slice(2, -2)}
            </strong>
          );
        }
        return <span key={index}>{part}</span>;
      })}
    </>
  );
}
