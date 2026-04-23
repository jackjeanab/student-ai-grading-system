import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { afterEach, expect, test, vi } from "vitest";

import { TeacherReportPage } from "../features/teacher/TeacherReportPage";

afterEach(() => {
  vi.restoreAllMocks();
});

test("loads assignment report from backend", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(
      JSON.stringify({
        assignment_id: 101,
        summary: {
          total: 1,
          evaluated: 1,
          green: 1,
          blue: 0,
          yellow: 0,
          red: 0,
        },
        rows: [
          {
            submission_id: 55,
            student_id: 1,
            activity_id: 1,
            assignment_id: 101,
            status: "evaluated",
            light: "green",
            grade: "優",
            feedback: "同學做得很好。",
            source: "gemini",
          },
        ],
      }),
      { status: 200 },
    ),
  );

  render(<TeacherReportPage />);

  expect(await screen.findByRole("heading", { name: "作業 101" })).toBeInTheDocument();
  expect(screen.getByText("已完成 1 份評分，共 1 份提交。")).toBeInTheDocument();
  expect(screen.getByText("學生 1：綠燈 / 優 - 同學做得很好。")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenCalledWith(
    "https://student-ai-grading-backend.onrender.com/api/reports/assignments/101",
    expect.objectContaining({
      headers: {
        Authorization: "Bearer dev-token",
      },
    }),
  );
});
