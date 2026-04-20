import type { CSSProperties, MouseEventHandler, ReactNode } from "react";

export type StatusTone = "red" | "yellow" | "green" | "blue";

export type StatusBadgeProps = {
  tone: StatusTone;
  label: string;
  detail?: string;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  selected?: boolean;
};

type ToneStyle = {
  background: string;
  border: string;
  dot: string;
  text: string;
};

const toneStyles: Record<StatusTone, ToneStyle> = {
  red: {
    background: "#fef2f2",
    border: "#fca5a5",
    dot: "#dc2626",
    text: "#991b1b",
  },
  yellow: {
    background: "#fffbeb",
    border: "#fcd34d",
    dot: "#ca8a04",
    text: "#92400e",
  },
  green: {
    background: "#f0fdf4",
    border: "#86efac",
    dot: "#16a34a",
    text: "#166534",
  },
  blue: {
    background: "#eff6ff",
    border: "#93c5fd",
    dot: "#2563eb",
    text: "#1d4ed8",
  },
};

export function StatusBadge({ tone, label, detail, onClick, selected = false }: StatusBadgeProps) {
  const styles = toneStyles[tone];
  const content: ReactNode = (
    <>
      <span
        aria-hidden="true"
        style={{
          width: 10,
          height: 10,
          borderRadius: 999,
          backgroundColor: styles.dot,
          boxShadow: `0 0 0 3px ${styles.dot}22`,
          flexShrink: 0,
        }}
      />
      <span style={{ display: "grid", gap: 2, textAlign: "left" }}>
        <span>{label}</span>
        {detail ? <span style={{ fontSize: 12, opacity: 0.86 }}>{detail}</span> : null}
      </span>
    </>
  );

  const baseStyle: CSSProperties = {
    alignItems: "center",
    background: styles.background,
    border: selected ? `2px solid ${styles.dot}` : `1px solid ${styles.border}`,
    borderRadius: 999,
    color: styles.text,
    display: "inline-flex",
    gap: 8,
    justifyContent: "center",
    minHeight: 40,
    padding: "8px 12px",
    width: "100%",
  };

  if (onClick) {
    return (
      <button
        type="button"
        aria-pressed={selected}
        aria-label={[label, detail].filter(Boolean).join("，")}
        onClick={onClick}
        style={baseStyle}
      >
        {content}
      </button>
    );
  }

  return (
    <span aria-label={[label, detail].filter(Boolean).join("，")} style={baseStyle}>
      {content}
    </span>
  );
}
