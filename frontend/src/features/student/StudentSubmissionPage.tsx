import { useState } from "react";

import { FeedbackCard } from "../../components/FeedbackCard";
import type { StudentAssignment } from "./StudentAssignmentsPage";

type StudentSubmissionPageProps = {
  assignment: StudentAssignment;
  onBackToAssignments: () => void;
};

export function StudentSubmissionPage({ assignment, onBackToAssignments }: StudentSubmissionPageProps) {
  const [xmlCode, setXmlCode] = useState("");
  const [submitted, setSubmitted] = useState(false);

  return (
    <section>
      <h1>{assignment.title}</h1>
      <p>請直接貼上 Arduino Blockly XML 文字，再按送出作業。</p>
      <button type="button" onClick={onBackToAssignments}>
        返回作業列表
      </button>

      <form
        onSubmit={(event) => {
          event.preventDefault();
          setSubmitted(true);
        }}
      >
        <label htmlFor="xml-code">XML 程式碼</label>
        <textarea
          id="xml-code"
          name="xml-code"
          value={xmlCode}
          onChange={(event) => setXmlCode(event.target.value)}
          rows={12}
        />

        <button type="submit">送出作業</button>
      </form>

      {submitted ? (
        <FeedbackCard
          title="提交完成"
          summary="AI 已完成初步評閱，請查看以下回饋。"
          status="已送出"
          points={["XML 格式可讀", "程式流程清楚", "可再補充註解說明"]}
        />
      ) : null}
    </section>
  );
}
