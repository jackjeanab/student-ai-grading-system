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
    title: "LED blink",
    dueDate: "2026-04-24",
    status: "open",
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
        feedback: "Looks ready.",
        source: "gemini",
      }),
      { status: 202 },
    ),
  );

  render(<StudentSubmissionPage assignment={assignment} onBackToAssignments={() => undefined} />);

  fireEvent.change(screen.getByLabelText("XML content"), {
    target: { value: '<xml xmlns="https://developers.google.com/blockly/xml" />' },
  });
  fireEvent.click(screen.getByRole("button", { name: "Submit for AI grading" }));

  expect(await screen.findByText("AI grading result")).toBeInTheDocument();
  expect(screen.getByText("Looks ready.")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenCalledWith(
    "https://student-ai-grading-backend.onrender.com/api/submissions",
    expect.objectContaining({
      method: "POST",
      body: JSON.stringify({
        assignment_id: 101,
        activity_id: 1,
        xml_content: '<xml xmlns="https://developers.google.com/blockly/xml" />',
      }),
    }),
  );
});
