import { useState } from "react";

import { AssignmentGrid, type AssignmentGridCell, type AssignmentGridRow } from "../../components/AssignmentGrid";
import { TeacherReviewDrawer } from "./TeacherReviewDrawer";

type TeacherDashboardAssignment = {
  id: string;
  title: string;
};

type TeacherDashboardStats = {
  red: number;
  yellow: number;
  green: number;
  blue: number;
};

export const sampleTeacherAssignments: readonly TeacherDashboardAssignment[] = [
  { id: "assignment-led", title: "LED 控制任務" },
  { id: "assignment-loop", title: "迴圈練習" },
  { id: "assignment-sensor", title: "感測器讀值" },
];

export const sampleTeacherRows: readonly AssignmentGridRow[] = [
  {
    studentId: "student-001",
    studentName: "林子涵",
    cells: [
      {
        assignmentId: "assignment-led",
        assignmentTitle: "LED 控制任務",
        feedbackSummary: "XML 結構完整，但燈號切換節奏還可以更穩定。",
        reviewNote: "建議補上等待節點，避免閃爍過快。",
        studentId: "student-001",
        studentName: "林子涵",
        tone: "yellow",
        statusLabel: "AI 檢查中",
        updatedAt: "更新於 10:12",
      },
      {
        assignmentId: "assignment-loop",
        assignmentTitle: "迴圈練習",
        feedbackSummary: "流程正確，已完成教師覆核。",
        reviewNote: "表現穩定，已標記為通過。",
        studentId: "student-001",
        studentName: "林子涵",
        tone: "green",
        statusLabel: "已通過",
        updatedAt: "更新於 09:40",
      },
      {
        assignmentId: "assignment-sensor",
        assignmentTitle: "感測器讀值",
        feedbackSummary: "尚未完成上傳，系統待補件。",
        reviewNote: "請提醒學生補交。",
        studentId: "student-001",
        studentName: "林子涵",
        tone: "blue",
        statusLabel: "待補交",
        updatedAt: "更新於 08:55",
      },
    ],
  },
  {
    studentId: "student-002",
    studentName: "陳映辰",
    cells: [
      {
        assignmentId: "assignment-led",
        assignmentTitle: "LED 控制任務",
        feedbackSummary: "目前有參數錯誤，AI 建議先修正輸出腳位。",
        reviewNote: "需要重送一次。",
        studentId: "student-002",
        studentName: "陳映辰",
        tone: "red",
        statusLabel: "需修正",
        updatedAt: "更新於 10:05",
      },
      {
        assignmentId: "assignment-loop",
        assignmentTitle: "迴圈練習",
        feedbackSummary: "已完成初步比對。",
        reviewNote: "等待教師確認。",
        studentId: "student-002",
        studentName: "陳映辰",
        tone: "yellow",
        statusLabel: "AI 檢查中",
        updatedAt: "更新於 09:30",
      },
      {
        assignmentId: "assignment-sensor",
        assignmentTitle: "感測器讀值",
        feedbackSummary: "資料格式完整，進入覆核。",
        reviewNote: "可視情況直接批改。",
        studentId: "student-002",
        studentName: "陳映辰",
        tone: "green",
        statusLabel: "已通過",
        updatedAt: "更新於 08:20",
      },
    ],
  },
  {
    studentId: "student-003",
    studentName: "黃品妤",
    cells: [
      {
        assignmentId: "assignment-led",
        assignmentTitle: "LED 控制任務",
        feedbackSummary: "已送出，等待系統整理回饋。",
        reviewNote: "稍後再看即可。",
        studentId: "student-003",
        studentName: "黃品妤",
        tone: "blue",
        statusLabel: "待整理",
        updatedAt: "更新於 10:18",
      },
      {
        assignmentId: "assignment-loop",
        assignmentTitle: "迴圈練習",
        feedbackSummary: "題目已完成，細節正由 AI 檢查。",
        reviewNote: "待回饋完成後再覆核。",
        studentId: "student-003",
        studentName: "黃品妤",
        tone: "yellow",
        statusLabel: "AI 檢查中",
        updatedAt: "更新於 09:58",
      },
      {
        assignmentId: "assignment-sensor",
        assignmentTitle: "感測器讀值",
        feedbackSummary: "完成度高，已通過。",
        reviewNote: "可作為示範作品。",
        studentId: "student-003",
        studentName: "黃品妤",
        tone: "green",
        statusLabel: "已通過",
        updatedAt: "更新於 08:05",
      },
    ],
  },
];

const sampleTeacherStats: TeacherDashboardStats = {
  red: 2,
  yellow: 4,
  green: 5,
  blue: 3,
};

function findSelectedCell(selectedCellId: string | null): AssignmentGridCell | null {
  if (!selectedCellId) {
    return null;
  }

  return sampleTeacherRows.flatMap((row) => row.cells).find((cell) => `${cell.studentId}:${cell.assignmentId}` === selectedCellId) ?? null;
}

export function TeacherDashboardPage() {
  const [selectedCellId, setSelectedCellId] = useState<string | null>(
    sampleTeacherRows[0]?.cells[0] ? `${sampleTeacherRows[0].cells[0].studentId}:${sampleTeacherRows[0].cells[0].assignmentId}` : null,
  );

  const selectedCell = findSelectedCell(selectedCellId);

  return (
    <section style={{ display: "grid", gap: 20 }}>
      <header style={heroStyle}>
        <div style={{ display: "grid", gap: 8 }}>
          <p style={eyebrowStyle}>老師端工作區</p>
          <h1 style={{ margin: 0 }}>班級總覽</h1>
          <p style={{ margin: 0, color: "#4b5563", lineHeight: 1.6 }}>
            以學生與作業矩陣檢視全班進度，點選燈號即可查看 AI 回饋與教師覆核。
          </p>
        </div>

        <div style={statsGridStyle} aria-label="進度狀況">
          <StatCard label="紅燈" value={sampleTeacherStats.red} tone="red" />
          <StatCard label="黃燈" value={sampleTeacherStats.yellow} tone="yellow" />
          <StatCard label="綠燈" value={sampleTeacherStats.green} tone="green" />
          <StatCard label="藍燈" value={sampleTeacherStats.blue} tone="blue" />
        </div>
      </header>

      <div style={layoutStyle}>
        <section style={{ display: "grid", gap: 12 }}>
          <h2 style={{ margin: 0 }}>進度狀況</h2>
          <AssignmentGrid
            assignments={sampleTeacherAssignments}
            rows={sampleTeacherRows}
            selectedCellId={selectedCellId}
            onCellSelect={(cell) => setSelectedCellId(`${cell.studentId}:${cell.assignmentId}`)}
          />
        </section>

        <TeacherReviewDrawer cell={selectedCell} open={selectedCell !== null} onClose={() => setSelectedCellId(null)} />
      </div>
    </section>
  );
}

function StatCard({ label, value, tone }: { label: string; tone: "red" | "yellow" | "green" | "blue"; value: number }) {
  const background: Record<typeof tone, string> = {
    red: "#fef2f2",
    yellow: "#fffbeb",
    green: "#f0fdf4",
    blue: "#eff6ff",
  };

  const border: Record<typeof tone, string> = {
    red: "#fecaca",
    yellow: "#fde68a",
    green: "#bbf7d0",
    blue: "#bfdbfe",
  };

  return (
    <article
      style={{
        background: background[tone],
        border: `1px solid ${border[tone]}`,
        borderRadius: 16,
        padding: 16,
      }}
    >
      <p style={{ margin: 0, color: "#6b7280" }}>{label}</p>
      <p style={{ margin: "8px 0 0", fontSize: 28, fontWeight: 700 }}>{value}</p>
    </article>
  );
}

const heroStyle = {
  display: "grid",
  gap: 20,
  background: "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
  border: "1px solid #e5e7eb",
  borderRadius: 24,
  boxShadow: "0 16px 40px rgba(15, 23, 42, 0.06)",
  padding: 24,
} as const;

const eyebrowStyle = {
  color: "#6b7280",
  fontSize: 12,
  letterSpacing: "0.12em",
  margin: 0,
  textTransform: "uppercase",
} as const;

const statsGridStyle = {
  display: "grid",
  gap: 12,
  gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))",
} as const;

const layoutStyle = {
  alignItems: "start",
  display: "grid",
  gap: 20,
  gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 320px), 1fr))",
} as const;
