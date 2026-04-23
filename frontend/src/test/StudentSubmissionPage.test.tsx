import { fireEvent, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { afterEach, expect, test, vi } from "vitest";

import { StudentSubmissionPage } from "../features/student/StudentSubmissionPage";
import type { StudentAssignment } from "../features/student/StudentAssignmentsPage";

afterEach(() => {
  vi.restoreAllMocks();
});

test("submits xml to backend and renders ai feedback", async () => {
  const assignment: StudentAssignment = {
    id: "101",
    title: "LED 控制任務",
    description: "請設計 LED 每 1 秒閃爍一次。",
    dueDate: "2026-04-24",
    status: "已開放",
  };
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(
      JSON.stringify({
        submission_id: 55,
        activity_id: 1,
        assignment_id: 101,
        status: "evaluated",
        light: "green",
        grade: "優",
        feedback: "同學做得很好。",
        source: "gemini",
      }),
      { status: 202 },
    ),
  );

  render(<StudentSubmissionPage assignment={assignment} onBackToAssignments={() => undefined} />);

  fireEvent.change(screen.getByLabelText("XML 內容"), {
    target: { value: '<xml xmlns="https://developers.google.com/blockly/xml" />' },
  });
  fireEvent.click(screen.getByRole("button", { name: "送出給 AI 評分" }));

  expect(await screen.findByText("AI 評分結果")).toBeInTheDocument();
  expect(screen.getByText("同學做得很好。")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenCalledWith(
    "https://student-ai-grading-backend.onrender.com/api/submissions",
    expect.objectContaining({
      method: "POST",
      body: JSON.stringify({
        assignment_id: 101,
        activity_id: 1,
        assignment_prompt: "LED 控制任務\n請設計 LED 每 1 秒閃爍一次。",
        xml_content: '<xml xmlns="https://developers.google.com/blockly/xml" />',
      }),
    }),
  );
});
