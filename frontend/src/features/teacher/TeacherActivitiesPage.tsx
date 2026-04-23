import { useState } from "react";

import { createAssignment } from "../../lib/api";
import type { StudentAssignment } from "../student/StudentAssignmentsPage";

type TeacherActivity = {
  className: string;
  courseTitle: string;
  progress: string;
  nextStep: string;
};

type TeacherActivitiesPageProps = {
  onAssignmentCreated?: (assignment: StudentAssignment) => void;
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

export function TeacherActivitiesPage({ onAssignmentCreated }: TeacherActivitiesPageProps) {
  const [title, setTitle] = useState("LED 控制任務");
  const [description, setDescription] = useState("請設計 LED 每 1 秒閃爍一次。");
  const [message, setMessage] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  async function handleCreateAssignment(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setIsSaving(true);

    try {
      const assignment = await createAssignment({
        id: 101,
        title,
        description,
      });
      onAssignmentCreated?.({
        id: String(assignment.id),
        title: assignment.title,
        description: assignment.description ?? "",
        dueDate: "2026-04-24",
        status: "已開放",
      });
      setMessage("題目已儲存，學生提交時會一起送給 AI 評分。");
    } catch (caught) {
      setMessage(caught instanceof Error ? caught.message : "題目儲存失敗。");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <section style={{ display: "grid", gap: 16 }}>
      <header>
        <p style={{ color: "#6b7280", margin: 0 }}>老師端工作區</p>
        <h1 style={{ margin: "6px 0 0" }}>活動與課堂管理</h1>
        <p style={{ color: "#4b5563", lineHeight: 1.6 }}>
          集中檢視各班目前的作業批次、追蹤進度與後續待辦。
        </p>
      </header>

      <form
        onSubmit={handleCreateAssignment}
        style={{
          border: "1px solid #d1d5db",
          borderRadius: 18,
          display: "grid",
          gap: 12,
          padding: 18,
        }}
      >
        <h2 style={{ margin: 0 }}>教師設定作業題目</h2>
        <label htmlFor="assignment-title">作業名稱</label>
        <input
          id="assignment-title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />

        <label htmlFor="assignment-description">題目說明</label>
        <textarea
          id="assignment-description"
          rows={4}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />

        <button type="submit" disabled={isSaving || title.trim().length === 0}>
          {isSaving ? "儲存中..." : "儲存題目"}
        </button>
        {message ? <p role="status">{message}</p> : null}
      </form>

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
