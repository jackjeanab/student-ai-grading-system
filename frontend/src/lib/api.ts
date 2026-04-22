export type SubmissionEvaluation = {
  submission_id: number;
  activity_id: number;
  assignment_id: number;
  status: string;
  light: "green" | "blue" | "yellow" | "red";
  grade: string;
  feedback: string;
  source: string;
};

export type AssignmentReportRow = SubmissionEvaluation & {
  student_id: number;
};

export type AssignmentReport = {
  assignment_id: number;
  summary: {
    total: number;
    evaluated: number;
    green: number;
    blue: number;
    yellow: number;
    red: number;
  };
  rows: AssignmentReportRow[];
};

const DEFAULT_API_BASE_URL = "https://student-ai-grading-backend.onrender.com";
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL;

export function getApiBaseUrl(): string {
  return API_BASE_URL.replace(/\/$/, "");
}

export async function submitAssignmentXml(params: {
  assignmentId: number;
  activityId: number;
  xmlContent: string;
}): Promise<SubmissionEvaluation> {
  return request<SubmissionEvaluation>("/api/submissions", {
    method: "POST",
    headers: {
      Authorization: "Bearer student-token",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      assignment_id: params.assignmentId,
      activity_id: params.activityId,
      xml_content: params.xmlContent,
    }),
  });
}

export async function getAssignmentReport(assignmentId: number): Promise<AssignmentReport> {
  return request<AssignmentReport>(`/api/reports/assignments/${assignmentId}`, {
    headers: {
      Authorization: "Bearer dev-token",
    },
  });
}

async function request<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, init);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}
