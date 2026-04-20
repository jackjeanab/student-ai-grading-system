type FeedbackCardProps = {
  title: string;
  summary: string;
  status: string;
  points: readonly string[];
};

export function FeedbackCard({ title, summary, status, points }: FeedbackCardProps) {
  return (
    <section aria-label="AI 回饋" style={{ border: "1px solid #d1d5db", borderRadius: 12, padding: 16 }}>
      <h3>{title}</h3>
      <p>{summary}</p>
      <p>
        狀態：<strong>{status}</strong>
      </p>
      <ul>
        {points.map((point) => (
          <li key={point}>{point}</li>
        ))}
      </ul>
    </section>
  );
}
