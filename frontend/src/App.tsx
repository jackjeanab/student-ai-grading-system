import { useState } from "react";

import { StudentAssignmentsPage, type StudentAssignment } from "./features/student/StudentAssignmentsPage";
import { StudentClassStatusPage, sampleStatusLights } from "./features/student/StudentClassStatusPage";
import { StudentSubmissionPage } from "./features/student/StudentSubmissionPage";
import { TeacherActivitiesPage } from "./features/teacher/TeacherActivitiesPage";
import { TeacherDashboardPage } from "./features/teacher/TeacherDashboardPage";
import { TeacherReportPage } from "./features/teacher/TeacherReportPage";

const sampleAssignments: readonly StudentAssignment[] = [
  {
    id: "101",
    title: "LED 控制任務",
    description: "請設計 LED 每 1 秒閃爍一次。",
    dueDate: "2026-04-24",
    status: "待繳交",
  },
  {
    id: "102",
    title: "感測器讀值",
    description: "請使用感測器積木讀取數值，並依照條件控制輸出。",
    dueDate: "2026-04-26",
    status: "AI 檢查中",
  },
];

type AppRole = "student" | "teacher";
type TeacherView = "activities" | "dashboard" | "report";

export function App() {
  const [role, setRole] = useState<AppRole>("student");
  const [assignments, setAssignments] = useState<readonly StudentAssignment[]>(sampleAssignments);
  const [selectedAssignment, setSelectedAssignment] = useState<StudentAssignment | null>(null);
  const [showClassStatus, setShowClassStatus] = useState(false);
  const [teacherView, setTeacherView] = useState<TeacherView>("dashboard");

  return (
    <main>
      <header>
        <h1>學生作業 AI 評分與即時進度燈號顯示系統</h1>
        <nav aria-label="角色切換">
          <button type="button" onClick={() => setRole("student")} aria-pressed={role === "student"}>
            學生端
          </button>
          <button type="button" onClick={() => setRole("teacher")} aria-pressed={role === "teacher"}>
            老師端
          </button>
        </nav>
      </header>

      {role === "student" ? (
        <section aria-label="學生端">
          <header>
            <button type="button" onClick={() => setShowClassStatus((current) => !current)}>
              {showClassStatus ? "返回作業列表" : "查看班級燈號"}
            </button>
          </header>

          {showClassStatus ? (
            <StudentClassStatusPage statusLights={sampleStatusLights} />
          ) : selectedAssignment ? (
            <StudentSubmissionPage
              assignment={selectedAssignment}
              onBackToAssignments={() => setSelectedAssignment(null)}
            />
          ) : (
            <StudentAssignmentsPage assignments={assignments} onSelectAssignment={setSelectedAssignment} />
          )}
        </section>
      ) : (
        <section aria-label="老師端">
          <nav aria-label="老師端頁面切換">
            <button
              type="button"
              onClick={() => setTeacherView("activities")}
              aria-pressed={teacherView === "activities"}
            >
              活動管理
            </button>
            <button
              type="button"
              onClick={() => setTeacherView("dashboard")}
              aria-pressed={teacherView === "dashboard"}
            >
              班級總覽
            </button>
            <button
              type="button"
              onClick={() => setTeacherView("report")}
              aria-pressed={teacherView === "report"}
            >
              課後報表
            </button>
          </nav>

          {teacherView === "activities" ? (
            <TeacherActivitiesPage
              onAssignmentCreated={(assignment) =>
                setAssignments((current) => [
                  assignment,
                  ...current.filter((candidate) => candidate.id !== assignment.id),
                ])
              }
            />
          ) : teacherView === "report" ? (
            <TeacherReportPage />
          ) : (
            <TeacherDashboardPage />
          )}
        </section>
      )}
    </main>
  );
}
