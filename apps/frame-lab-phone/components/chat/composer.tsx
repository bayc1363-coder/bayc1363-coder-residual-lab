import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ArrowUp } from "lucide-react";
import { useEffect, useRef } from "react";

export function Composer({
  value,
  onChange,
  onSend,
  disabled,
}: {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    node.style.height = "0px";
    node.style.height = `${Math.min(node.scrollHeight, 140)}px`;
  }, [value]);

  return (
    <div
      className="sticky bottom-0 z-20 border-t border-white/6 bg-[#121018]/86 backdrop-blur-xl"
      style={{
        paddingBottom: "max(12px, env(safe-area-inset-bottom))",
        paddingLeft: "max(12px, env(safe-area-inset-left))",
        paddingRight: "max(12px, env(safe-area-inset-right))",
      }}
    >
      <form
        className="flex items-end gap-2 px-1 pt-2.5"
        onSubmit={(event) => {
          event.preventDefault();
          onSend();
        }}
      >
        <Textarea
          ref={ref}
          value={value}
          disabled={disabled}
          rows={1}
          placeholder="Ask something contested…"
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSend();
            }
          }}
          className="max-h-[140px] min-h-12 resize-none rounded-2xl border-white/10 bg-white/6 px-3.5 py-3 text-[16px] leading-5 dark:bg-white/6"
        />
        <Button
          type="submit"
          size="icon-lg"
          disabled={disabled || !value.trim()}
          aria-label="Send"
          data-testid="send"
          className="size-12 shrink-0 rounded-2xl bg-copper text-primary-foreground hover:bg-copper/90 disabled:opacity-40"
        >
          <ArrowUp className="size-5" />
        </Button>
      </form>
    </div>
  );
}
