import { useState } from "react";

import { FeedbackCard } from "../../components/FeedbackCard";
import { submitAssignmentXml, type SubmissionEvaluation } from "../../lib/api";
import type { StudentAssignment } from "./StudentAssignmentsPage";

type StudentSubmissionPageProps = {
  assignment: StudentAssignment;
  onBackToAssignments: () => void;
};

const DEFAULT_ACTIVITY_ID = 1;
const lightLabels: Record<SubmissionEvaluation["light"], string> = {
  green: "綠燈",
  blue: "藍燈",
  yellow: "黃燈",
  red: "紅燈",
};

export function StudentSubmissionPage({ assignment, onBackToAssignments }: StudentSubmissionPageProps) {
  const [xmlCode, setXmlCode] = useState("");
  const [evaluation, setEvaluation] = useState<SubmissionEvaluation | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setEvaluation(null);
    setIsSubmitting(true);

    try {
      const result = await submitAssignmentXml({
        assignmentId: Number.parseInt(assignment.id, 10),
        activityId: DEFAULT_ACTIVITY_ID,
        assignmentPrompt: [assignment.title, assignment.description].filter(Boolean).join("\n"),
        xmlContent: xmlCode,
      });
      setEvaluation(result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "作業送出失敗。");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h1>{assignment.title}</h1>
      {assignment.description ? <p>{assignment.description}</p> : null}
      <p>請貼上 Arduino Blockly XML，系統會依照老師設定的題目進行 AI 評分。</p>
      <button type="button" onClick={onBackToAssignments}>
        返回作業列表
      </button>

      <form onSubmit={handleSubmit}>
        <label htmlFor="xml-code">XML 內容</label>
        <textarea
          id="xml-code"
          name="xml-code"
          value={xmlCode}
          onChange={(event) => setXmlCode(event.target.value)}
          rows={12}
        />

        <button type="submit" disabled={isSubmitting || xmlCode.trim().length === 0}>
          {isSubmitting ? "送出中..." : "送出給 AI 評分"}
        </button>
      </form>

      {error ? <p role="alert">{error}</p> : null}

      {evaluation ? (
        <FeedbackCard
          title="AI 評分結果"
          summary={evaluation.feedback}
          status={`${lightLabels[evaluation.light]} / ${evaluation.grade}`}
          points={[
            `提交編號：${evaluation.submission_id}`,
            `評分來源：AI`,
            `處理狀態：已完成評分`,
          ]}
        />
      ) : null}
    </section>
  );
}
