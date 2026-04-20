import { fireEvent, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { expect, test } from "vitest";

import { StudentSubmissionPage } from "../features/student/StudentSubmissionPage";
import type { StudentAssignment } from "../features/student/StudentAssignmentsPage";

test("renders xml submission fields", () => {
  const assignment: StudentAssignment = {
    id: "A1",
    title: "LED 閃爍控制",
    dueDate: "2026-04-24",
    status: "待提交",
  };

  render(<StudentSubmissionPage assignment={assignment} onBackToAssignments={() => undefined} />);

  expect(screen.getByLabelText("XML 程式碼")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "送出作業" })).toBeInTheDocument();

  fireEvent.change(screen.getByLabelText("XML 程式碼"), {
    target: { value: "<xml />" },
  });
  fireEvent.click(screen.getByRole("button", { name: "送出作業" }));

  expect(screen.getByText("提交完成")).toBeInTheDocument();
  expect(screen.getByText("AI 已完成初步評閱，請查看以下回饋。")).toBeInTheDocument();
});
