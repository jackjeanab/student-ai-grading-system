type ReportSummary = {
  label: string;
  value: string;
  note: string;
};

const sampleReportSummaries: readonly ReportSummary[] = [
  { label: "平均通過率", value: "82%", note: "較上次課程提升 6%" },
  { label: "需修正比例", value: "11%", note: "多數集中在步驟順序" },
  { label: "待補交比例", value: "7%", note: "已通知 2 位學生" },
];

const sampleDistribution: readonly { label: string; count: number; tone: "red" | "yellow" | "green" | "blue" }[] = [
  { label: "紅燈", count: 3, tone: "red" },
  { label: "黃燈", count: 5, tone: "yellow" },
  { label: "綠燈", count: 18, tone: "green" },
  { label: "藍燈", count: 4, tone: "blue" },
];

export function TeacherReportPage() {
  return (
    <section style={{ display: "grid", gap: 16 }}>
      <header>
        <p style={{ color: "#6b7280", margin: 0 }}>老師端工作區</p>
        <h1 style={{ margin: "6px 0 0" }}>報表</h1>
        <p style={{ color: "#4b5563", lineHeight: 1.6 }}>
          呈現課後成果、燈號分布與可追蹤的班級統計。
        </p>
      </header>

      <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))" }}>
        {sampleReportSummaries.map((item) => (
          <article
            key={item.label}
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: 18,
              padding: 18,
            }}
          >
            <p style={{ margin: 0, color: "#6b7280" }}>{item.label}</p>
            <h2 style={{ margin: "8px 0 0" }}>{item.value}</h2>
            <p style={{ margin: "8px 0 0", color: "#4b5563" }}>{item.note}</p>
          </article>
        ))}
      </div>

      <section aria-label="燈號分布" style={{ border: "1px solid #e5e7eb", borderRadius: 18, padding: 18 }}>
        <h2 style={{ marginTop: 0 }}>課後結果分布</h2>
        <div style={{ display: "grid", gap: 12 }}>
          {sampleDistribution.map((item) => (
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
                    width: `${item.count * 4}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
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
