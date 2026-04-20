import type { CSSProperties } from "react";

import type { AssignmentGridCell } from "../../components/AssignmentGrid";
import { StatusBadge } from "../../components/StatusBadge";

export type TeacherReviewDrawerProps = {
  cell: AssignmentGridCell | null;
  open: boolean;
  onClose?: () => void;
};

export function TeacherReviewDrawer({ cell, open, onClose }: TeacherReviewDrawerProps) {
  if (!open || !cell) {
    return null;
  }

  return (
    <aside aria-label="覆核回饋" style={drawerStyle}>
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
        <div>
          <h2 style={{ margin: 0 }}>覆核回饋</h2>
          <p style={{ marginTop: 8, color: "#4b5563" }}>點選燈號後，可查看 AI 回饋、教師覆核與最新狀態。</p>
        </div>
        {onClose ? (
          <button type="button" onClick={onClose} style={closeButtonStyle}>
            關閉
          </button>
        ) : null}
      </div>

      <div style={{ display: "grid", gap: 16 }}>
        <div>
          <p style={metaStyle}>{cell.studentName}</p>
          <h3 style={{ margin: "4px 0 0" }}>{cell.assignmentTitle}</h3>
        </div>

        <StatusBadge tone={cell.tone} label={cell.statusLabel} detail={cell.updatedAt} />

        <section style={panelStyle}>
          <h4 style={sectionTitleStyle}>AI 回饋</h4>
          <p style={sectionTextStyle}>{cell.feedbackSummary}</p>
        </section>

        <section style={panelStyle}>
          <h4 style={sectionTitleStyle}>教師覆核</h4>
          <p style={sectionTextStyle}>{cell.reviewNote}</p>
        </section>
      </div>
    </aside>
  );
}

const drawerStyle: CSSProperties = {
  border: "1px solid #d1d5db",
  borderRadius: 20,
  background: "#ffffff",
  padding: 20,
  boxShadow: "0 12px 30px rgba(15, 23, 42, 0.08)",
};

const closeButtonStyle: CSSProperties = {
  background: "#f3f4f6",
  border: "1px solid #d1d5db",
  borderRadius: 999,
  padding: "8px 12px",
};

const panelStyle: CSSProperties = {
  background: "#f9fafb",
  border: "1px solid #e5e7eb",
  borderRadius: 16,
  padding: 16,
};

const metaStyle: CSSProperties = {
  margin: 0,
  color: "#6b7280",
  fontSize: 14,
};

const sectionTitleStyle: CSSProperties = {
  margin: 0,
  fontSize: 15,
};

const sectionTextStyle: CSSProperties = {
  marginBottom: 0,
  color: "#374151",
  lineHeight: 1.6,
};
