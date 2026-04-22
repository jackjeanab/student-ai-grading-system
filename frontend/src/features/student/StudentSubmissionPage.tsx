import { useState } from "react";

import { FeedbackCard } from "../../components/FeedbackCard";
import { submitAssignmentXml, type SubmissionEvaluation } from "../../lib/api";
import type { StudentAssignment } from "./StudentAssignmentsPage";

type StudentSubmissionPageProps = {
  assignment: StudentAssignment;
  onBackToAssignments: () => void;
};

const DEFAULT_ACTIVITY_ID = 1;

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
        xmlContent: xmlCode,
      });
      setEvaluation(result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Submission failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h1>{assignment.title}</h1>
      <p>Paste Arduino Blockly XML and submit it for AI grading.</p>
      <button type="button" onClick={onBackToAssignments}>
        Back to assignments
      </button>

      <form onSubmit={handleSubmit}>
        <label htmlFor="xml-code">XML content</label>
        <textarea
          id="xml-code"
          name="xml-code"
          value={xmlCode}
          onChange={(event) => setXmlCode(event.target.value)}
          rows={12}
        />

        <button type="submit" disabled={isSubmitting || xmlCode.trim().length === 0}>
          {isSubmitting ? "Submitting..." : "Submit for AI grading"}
        </button>
      </form>

      {error ? <p role="alert">{error}</p> : null}

      {evaluation ? (
        <FeedbackCard
          title="AI grading result"
          summary={evaluation.feedback}
          status={`${evaluation.light} / ${evaluation.grade}`}
          points={[
            `Submission ID: ${evaluation.submission_id}`,
            `Source: ${evaluation.source}`,
            `Status: ${evaluation.status}`,
          ]}
        />
      ) : null}
    </section>
  );
}

