import { useState } from "react";

import { FeedbackCard } from "../../components/FeedbackCard";

export type StatusLight = {
  key: "red" | "yellow" | "green" | "blue";
  label: string;
  status: string;
  summary: string;
  points: readonly string[];
  color: string;
};

export const sampleStatusLights: readonly StatusLight[] = [
  {
    key: "red",
    label: "需修改",
    status: "紅燈",
    summary: "目前有需要調整的地方，請依回饋修正後再提交。",
    points: ["缺少必要節點", "程式流程可再補強"],
    color: "#dc2626",
  },
  {
    key: "yellow",
    label: "AI 評閱中",
    status: "黃燈",
    summary: "系統正在分析 XML 內容，請稍後查看回饋。",
    points: ["正在檢查 XML 結構", "正在比對作業要求"],
    color: "#ca8a04",
  },
  {
    key: "green",
    label: "已提交",
    status: "綠燈",
    summary: "學生已完成提交，等待 AI 評閱結果。",
    points: ["提交時間正常", "內容格式正確"],
    color: "#16a34a",
  },
  {
    key: "blue",
    label: "已完成",
    status: "藍燈",
    summary: "作業已完成評分，學生可檢視最終回饋。",
    points: ["已完成評分", "可下載回饋摘要"],
    color: "#2563eb",
  },
];

type StudentClassStatusPageProps = {
  statusLights: readonly StatusLight[];
};

export function StudentClassStatusPage({ statusLights }: StudentClassStatusPageProps) {
  const [selectedKey, setSelectedKey] = useState<StatusLight["key"] | null>(statusLights[0]?.key ?? null);
  const selectedStatus = statusLights.find((light) => light.key === selectedKey) ?? statusLights[0] ?? null;

  if (statusLights.length === 0) {
    return (
      <section>
        <h1>全班作業進度</h1>
        <p>尚無燈號資料。</p>
      </section>
    );
  }

  return (
    <section>
      <h1>全班作業進度</h1>
      <p>點選燈號可查看對應狀態的學生回饋。</p>

      <div role="group" aria-label="作業燈號">
        {statusLights.map((light) => (
          <button
            key={light.key}
            type="button"
            aria-pressed={selectedStatus?.key === light.key}
            onClick={() => setSelectedKey(light.key)}
            style={{
              alignItems: "center",
              background: "#fff",
              border: selectedStatus?.key === light.key ? "2px solid #111827" : "1px solid #d1d5db",
              borderRadius: 999,
              display: "inline-flex",
              gap: 8,
              marginBottom: 8,
              marginRight: 8,
              padding: "8px 12px",
            }}
          >
            <span
              aria-hidden="true"
              style={{
                width: 12,
                height: 12,
                borderRadius: "999px",
                backgroundColor: light.color,
                boxShadow: `0 0 0 3px ${light.color}33`,
              }}
            />
            <span>
              {light.label} {light.status}
            </span>
          </button>
        ))}
      </div>

      {selectedStatus ? (
        <FeedbackCard
          title={selectedStatus.label}
          summary={selectedStatus.summary}
          status={selectedStatus.status}
          points={selectedStatus.points}
        />
      ) : (
        <p>尚無燈號資料。</p>
      )}
    </section>
  );
}
