import { useEffect, useState } from "react";

import { getAssignmentReport, type AssignmentReport } from "../../lib/api";

const DEFAULT_ASSIGNMENT_ID = 101;
const lightLabels: Record<"green" | "blue" | "yellow" | "red", string> = {
  green: "綠燈",
  blue: "藍燈",
  yellow: "黃燈",
  red: "紅燈",
};

export function TeacherReportPage() {
  const [report, setReport] = useState<AssignmentReport | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;

    async function loadReport() {
      try {
        const nextReport = await getAssignmentReport(DEFAULT_ASSIGNMENT_ID);
        if (!ignore) {
          setReport(nextReport);
        }
      } catch (caught) {
        if (!ignore) {
          setError(caught instanceof Error ? caught.message : "無法載入報表。");
        }
      } finally {
        if (!ignore) {
          setIsLoading(false);
        }
      }
    }

    void loadReport();

    return () => {
      ignore = true;
    };
  }, []);

  if (isLoading) {
    return <p>正在載入評分報表...</p>;
  }

  if (error) {
    return <p role="alert">{error}</p>;
  }

  if (!report) {
    return <p>目前沒有報表資料。</p>;
  }

  const distribution = [
    { label: "綠燈", count: report.summary.green, tone: "green" },
    { label: "藍燈", count: report.summary.blue, tone: "blue" },
    { label: "黃燈", count: report.summary.yellow, tone: "yellow" },
    { label: "紅燈", count: report.summary.red, tone: "red" },
  ] as const;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <header>
        <p style={{ color: "#6b7280", margin: 0 }}>教師課後報表</p>
        <h1 style={{ margin: "6px 0 0" }}>作業 {report.assignment_id}</h1>
        <p style={{ color: "#4b5563", lineHeight: 1.6 }}>
          已完成 {report.summary.evaluated} 份評分，共 {report.summary.total} 份提交。
        </p>
      </header>

      <section aria-label="燈號分布" style={{ border: "1px solid #e5e7eb", borderRadius: 18, padding: 18 }}>
        <h2 style={{ marginTop: 0 }}>燈號分布</h2>
        <div style={{ display: "grid", gap: 12 }}>
          {distribution.map((item) => (
            <div key={item.label} style={{ display: "grid", gap: 6 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                <span>{item.label}</span>
                <span>{item.count}</span>
              </div>
              <div style={{ background: "#e5e7eb", borderRadius: 999, height: 10, overflow: "hidden" }}>
                <div
                  style={{
                    background: barColor[item.tone],
                    height: "100%",
                    width: `${Math.min(item.count * 12, 100)}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      <section aria-label="學生作業回饋" style={{ border: "1px solid #e5e7eb", borderRadius: 18, padding: 18 }}>
        <h2 style={{ marginTop: 0 }}>學生作業回饋</h2>
        {report.rows.length === 0 ? (
          <p>目前還沒有學生提交。</p>
        ) : (
          <ul>
            {report.rows.map((row) => (
              <li key={row.submission_id}>
                學生 {row.student_id}：{lightLabels[row.light]} / {row.grade} - {row.feedback}
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}

const barColor: Record<"red" | "yellow" | "green" | "blue", string> = {
  red: "#dc2626",
  yellow: "#ca8a04",
  green: "#16a34a",
  blue: "#2563eb",
};
