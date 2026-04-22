import { useEffect, useState } from "react";

import { getAssignmentReport, type AssignmentReport } from "../../lib/api";

const DEFAULT_ASSIGNMENT_ID = 101;

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
          setError(caught instanceof Error ? caught.message : "Failed to load report.");
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
    return <p>Loading grading report...</p>;
  }

  if (error) {
    return <p role="alert">{error}</p>;
  }

  if (!report) {
    return <p>No report data.</p>;
  }

  const distribution = [
    { label: "Green", count: report.summary.green, tone: "green" },
    { label: "Blue", count: report.summary.blue, tone: "blue" },
    { label: "Yellow", count: report.summary.yellow, tone: "yellow" },
    { label: "Red", count: report.summary.red, tone: "red" },
  ] as const;

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <header>
        <p style={{ color: "#6b7280", margin: 0 }}>Teacher report</p>
        <h1 style={{ margin: "6px 0 0" }}>Assignment {report.assignment_id}</h1>
        <p style={{ color: "#4b5563", lineHeight: 1.6 }}>
          {report.summary.evaluated} of {report.summary.total} submissions evaluated.
        </p>
      </header>

      <section aria-label="Light distribution" style={{ border: "1px solid #e5e7eb", borderRadius: 18, padding: 18 }}>
        <h2 style={{ marginTop: 0 }}>Light distribution</h2>
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

      <section aria-label="Submission feedback" style={{ border: "1px solid #e5e7eb", borderRadius: 18, padding: 18 }}>
        <h2 style={{ marginTop: 0 }}>Submission feedback</h2>
        {report.rows.length === 0 ? (
          <p>No submissions yet.</p>
        ) : (
          <ul>
            {report.rows.map((row) => (
              <li key={row.submission_id}>
                Student {row.student_id}: {row.light} / {row.grade} - {row.feedback}
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

