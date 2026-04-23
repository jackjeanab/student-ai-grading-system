import { useEffect, useState } from "react";

import { StudentAssignmentsPage, type StudentAssignment } from "./features/student/StudentAssignmentsPage";
import { StudentClassStatusPage, sampleStatusLights } from "./features/student/StudentClassStatusPage";
import { StudentSubmissionPage } from "./features/student/StudentSubmissionPage";
import { TeacherActivitiesPage } from "./features/teacher/TeacherActivitiesPage";
import { TeacherDashboardPage } from "./features/teacher/TeacherDashboardPage";
import { TeacherReportPage } from "./features/teacher/TeacherReportPage";
import { getAssignments } from "./lib/api";

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

  useEffect(() => {
    let ignore = false;

    async function loadAssignments() {
      try {
        const remoteAssignments = await getAssignments();
        if (!ignore && remoteAssignments.length > 0) {
          setAssignments(
            remoteAssignments.map((assignment) => ({
              id: String(assignment.id),
              title: assignment.title,
              description: assignment.description ?? "",
              dueDate: "2026-04-24",
              status: "已開放",
            })),
          );
        }
      } catch {
        // 保留預設作業，讓教室現場即使網路短暫不穩也能展示畫面。
      }
    }

    void loadAssignments();

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1 className="app-title">學生作業 AI 評分與即時進度燈號顯示系統</h1>
        <nav className="app-nav" aria-label="角色切換">
          <button type="button" onClick={() => setRole("student")} aria-pressed={role === "student"}>
            學生端
          </button>
          <button type="button" onClick={() => setRole("teacher")} aria-pressed={role === "teacher"}>
            老師端
          </button>
        </nav>
      </header>

      {role === "student" ? (
        <section className="workspace" aria-label="學生端">
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
        <section className="workspace" aria-label="老師端">
          <nav className="view-nav" aria-label="老師端頁面切換">
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
