import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { expect, test } from "vitest";

import { TeacherDashboardPage } from "../features/teacher/TeacherDashboardPage";

test("renders class overview and progress status", () => {
  render(<TeacherDashboardPage />);

  expect(screen.getByRole("heading", { name: "班級總覽" })).toBeInTheDocument();
  expect(screen.getByText("進度狀況")).toBeInTheDocument();
});
