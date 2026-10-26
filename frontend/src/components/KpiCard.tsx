type Props = {
  title: string;
  value: string;
  hint?: string;
  tone?: "ok" | "warn" | "bad" | "neutral";
};

const tones = {
  ok: "border-emerald-600/30 bg-emerald-50",
  warn: "border-amber-600/30 bg-amber-50",
  bad: "border-rose-600/30 bg-rose-50",
  neutral: "border-[var(--line)] bg-[var(--surface)]",
};

export default function KpiCard({ title, value, hint, tone = "neutral" }: Props) {
  return (
    <div className={`rounded-xl border p-5 shadow-sm ${tones[tone]}`}>
      <p className="text-xs uppercase tracking-[0.14em] text-[var(--muted)]">{title}</p>
      <p className="mt-2 font-display text-3xl text-[var(--ink)]">{value}</p>
      {hint ? <p className="mt-2 text-sm text-[var(--muted)]">{hint}</p> : null}
    </div>
  );
}
