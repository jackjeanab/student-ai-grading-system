export type StudentAssignment = {
  id: string;
  title: string;
  dueDate: string;
  status: string;
};

type StudentAssignmentsPageProps = {
  assignments: readonly StudentAssignment[];
  onSelectAssignment: (assignment: StudentAssignment) => void;
};

export function StudentAssignmentsPage({ assignments, onSelectAssignment }: StudentAssignmentsPageProps) {
  return (
    <section>
      <h1>我的作業</h1>
      <p>先選擇一份作業，再進入提交頁。</p>

      <ul>
        {assignments.map((assignment) => (
          <li key={assignment.id}>
            <article>
              <h2>{assignment.title}</h2>
              <p>截止日：{assignment.dueDate}</p>
              <p>狀態：{assignment.status}</p>
              <button type="button" onClick={() => onSelectAssignment(assignment)}>
                選擇作業
              </button>
            </article>
          </li>
        ))}
      </ul>
    </section>
  );
}
