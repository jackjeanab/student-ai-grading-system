import type { CSSProperties } from "react";

import { StatusBadge, type StatusTone } from "./StatusBadge";

export type AssignmentGridCell = {
  assignmentId: string;
  assignmentTitle: string;
  feedbackSummary: string;
  reviewNote: string;
  studentId: string;
  studentName: string;
  tone: StatusTone;
  statusLabel: string;
  updatedAt: string;
};

export type AssignmentGridRow = {
  studentId: string;
  studentName: string;
  cells: readonly AssignmentGridCell[];
};

export type AssignmentGridProps = {
  assignments: readonly { id: string; title: string }[];
  onCellSelect?: (cell: AssignmentGridCell) => void;
  rows: readonly AssignmentGridRow[];
  selectedCellId?: string | null;
};

export function AssignmentGrid({ assignments, onCellSelect, rows, selectedCellId = null }: AssignmentGridProps) {
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ borderCollapse: "collapse", minWidth: 760, width: "100%" }}>
        <caption style={{ captionSide: "bottom", paddingTop: 12, textAlign: "left" }}>進度狀況以學生與作業矩陣呈現。</caption>
        <thead>
          <tr>
            <th scope="col" style={headerCellStyle}>
              學生
            </th>
            {assignments.map((assignment) => (
              <th key={assignment.id} scope="col" style={headerCellStyle}>
                {assignment.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.studentId}>
              <th scope="row" style={rowHeaderStyle}>
                {row.studentName}
              </th>
              {assignments.map((assignment) => {
                const cell = row.cells.find((candidate) => candidate.assignmentId === assignment.id);
                if (!cell) {
                  return (
                    <td key={assignment.id} style={bodyCellStyle}>
                      <span style={{ color: "#6b7280" }}>-</span>
                    </td>
                  );
                }

                return (
                  <td key={assignment.id} style={bodyCellStyle}>
                    <StatusBadge
                      tone={cell.tone}
                      label={cell.statusLabel}
                      detail={cell.feedbackSummary}
                      onClick={onCellSelect ? () => onCellSelect(cell) : undefined}
                      selected={selectedCellId === `${cell.studentId}:${cell.assignmentId}`}
                    />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const headerCellStyle: CSSProperties = {
  borderBottom: "1px solid #d1d5db",
  color: "#374151",
  fontSize: 14,
  fontWeight: 700,
  padding: "12px 10px",
  textAlign: "left",
  verticalAlign: "bottom",
  whiteSpace: "nowrap",
};

const rowHeaderStyle: CSSProperties = {
  borderBottom: "1px solid #e5e7eb",
  color: "#111827",
  fontSize: 14,
  fontWeight: 600,
  padding: "12px 10px",
  textAlign: "left",
  whiteSpace: "nowrap",
};

const bodyCellStyle: CSSProperties = {
  borderBottom: "1px solid #e5e7eb",
  padding: "10px",
  verticalAlign: "top",
};
