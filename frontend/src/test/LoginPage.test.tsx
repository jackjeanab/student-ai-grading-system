import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { expect, test } from "vitest";

import { LoginPage } from "../features/auth/LoginPage";

test("renders login fields", () => {
  render(<LoginPage />);

  expect(screen.getByLabelText("帳號")).toBeInTheDocument();
  expect(screen.getByLabelText("密碼")).toBeInTheDocument();
});
