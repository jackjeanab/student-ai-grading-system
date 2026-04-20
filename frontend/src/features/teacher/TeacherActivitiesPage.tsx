type TeacherActivity = {
  className: string;
  courseTitle: string;
  progress: string;
  nextStep: string;
};

const sampleActivities: readonly TeacherActivity[] = [
  {
    className: "三年級 A 班",
    courseTitle: "LED 控制任務",
    progress: "22 / 24 已送出",
    nextStep: "等待 2 位學生補交",
  },
  {
    className: "三年級 B 班",
    courseTitle: "感測器讀值",
    progress: "18 / 24 已通過",
    nextStep: "整理需修正名單",
  },
  {
    className: "四年級 A 班",
    courseTitle: "迴圈練習",
    progress: "26 / 28 已完成初評",
    nextStep: "安排教師覆核",
  },
];

export function TeacherActivitiesPage() {
  return (
    <section style={{ display: "grid", gap: 16 }}>
      <header>
        <p style={{ color: "#6b7280", margin: 0 }}>老師端工作區</p>
        <h1 style={{ margin: "6px 0 0" }}>活動與課堂管理</h1>
        <p style={{ color: "#4b5563", lineHeight: 1.6 }}>
          集中檢視各班目前的作業批次、追蹤進度與後續待辦。
        </p>
      </header>

      <div style={{ display: "grid", gap: 12 }}>
        {sampleActivities.map((activity) => (
          <article
            key={`${activity.className}-${activity.courseTitle}`}
            style={{
              border: "1px solid #e5e7eb",
              borderRadius: 18,
              padding: 18,
            }}
          >
            <h2 style={{ margin: 0 }}>{activity.className}</h2>
            <p style={{ margin: "8px 0 0", color: "#374151" }}>{activity.courseTitle}</p>
            <p style={{ margin: "8px 0 0", color: "#6b7280" }}>{activity.progress}</p>
            <p style={{ margin: "8px 0 0", fontWeight: 600 }}>{activity.nextStep}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
