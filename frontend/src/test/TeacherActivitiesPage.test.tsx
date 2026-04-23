import { fireEvent, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { afterEach, expect, test, vi } from "vitest";

import { TeacherActivitiesPage } from "../features/teacher/TeacherActivitiesPage";

afterEach(() => {
  vi.restoreAllMocks();
});

test("teacher creates assignment prompt from teacher page", async () => {
  const onAssignmentCreated = vi.fn();
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(
      JSON.stringify({
        id: 101,
        title: "LED 控制任務",
        description: "請設計 LED 每 1 秒閃爍一次。",
      }),
      { status: 201 },
    ),
  );

  render(<TeacherActivitiesPage onAssignmentCreated={onAssignmentCreated} />);

  fireEvent.change(screen.getByLabelText("作業名稱"), {
    target: { value: "LED 控制任務" },
  });
  fireEvent.change(screen.getByLabelText("題目說明"), {
    target: { value: "請設計 LED 每 1 秒閃爍一次。" },
  });
  fireEvent.click(screen.getByRole("button", { name: "儲存題目" }));

  expect(await screen.findByText("題目已儲存，學生提交時會一起送給 AI 評分。")).toBeInTheDocument();
  expect(onAssignmentCreated).toHaveBeenCalledWith(
    expect.objectContaining({
      id: "101",
      title: "LED 控制任務",
      description: "請設計 LED 每 1 秒閃爍一次。",
    }),
  );
  expect(fetchMock).toHaveBeenCalledWith(
    "https://student-ai-grading-backend.onrender.com/api/assignments",
    expect.objectContaining({
      method: "POST",
      body: JSON.stringify({
        id: 101,
        title: "LED 控制任務",
        description: "請設計 LED 每 1 秒閃爍一次。",
      }),
    }),
  );
});
