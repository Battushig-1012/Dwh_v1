"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Report = {
  as_of: string;
  title: string;
  qualitative_summary: string;
  risk_areas: { code: string; status: string; commentary: string }[];
  forward_looking: {
    horizon: string;
    scenarios: { name: string; car_pct: number; npl_pct: number; lcr_pct: number; narrative: string }[];
    recommended_actions: string[];
  };
  approximations_used: { id: string; description: string; reliability: string }[];
};

type Recipient = {
  recipient: string;
  needs: string[];
  detail_level: string;
  qual_vs_quant: string;
  last_confirmation: string;
  confirmed_relevant: boolean;
};

export default function RiskReportPage() {
  const router = useRouter();
  const [report, setReport] = useState<Report | null>(null);
  const [recipients, setRecipients] = useState<Recipient[]>([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([api<Report>("/api/bcbs/risk-report"), api<Recipient[]>("/api/bcbs/recipients")]).then(
      ([r, rec]) => {
        setReport(r);
        setRecipients(rec);
      }
    );
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">BCBS P8 · P9</p>
          <h1 className="font-display text-4xl mt-1">Comprehensive Risk Report</h1>
          <p className="mt-2 text-[var(--muted)]">{report?.title} · {report?.as_of}</p>
        </div>

        <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
          <h2 className="font-display text-xl mb-2">Qualitative narrative (Board-oriented)</h2>
          <p className="text-sm leading-relaxed">{report?.qualitative_summary}</p>
        </section>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {(report?.risk_areas || []).map((a) => (
            <div key={a.code} className="rounded-xl border border-[var(--line)] bg-white p-4 text-sm">
              <div className="text-xs text-[var(--muted)]">{a.code}</div>
              <div className="font-medium mt-1">{a.status}</div>
              <div className="text-xs mt-2 text-[var(--muted)]">{a.commentary}</div>
            </div>
          ))}
        </div>

        <section>
          <h2 className="font-display text-xl mb-3">Forward-looking ({report?.forward_looking.horizon})</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {(report?.forward_looking.scenarios || []).map((s) => (
              <div key={s.name} className="rounded-xl border border-[var(--line)] bg-white p-4 text-sm">
                <div className="font-display text-lg">{s.name}</div>
                <ul className="mt-2 space-y-1 text-xs">
                  <li>CAR {s.car_pct}%</li>
                  <li>NPL {s.npl_pct}%</li>
                  <li>LCR {s.lcr_pct}%</li>
                </ul>
                <p className="mt-2 text-[var(--muted)] text-xs">{s.narrative}</p>
              </div>
            ))}
          </div>
          <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4">
            <h3 className="font-medium text-sm mb-2">Recommended actions</h3>
            <ul className="list-disc pl-5 text-sm space-y-1">
              {(report?.forward_looking.recommended_actions || []).map((a) => (
                <li key={a}>{a}</li>
              ))}
            </ul>
          </div>
        </section>

        <section className="grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[var(--line)] bg-white p-5">
            <h2 className="font-display text-xl mb-3">Recipient profiles (clarity)</h2>
            {(recipients || []).map((r) => (
              <div key={r.recipient} className="border-b border-[var(--line)] py-2 text-sm">
                <div className="font-medium">{r.recipient}</div>
                <div className="text-xs text-[var(--muted)]">
                  {r.detail_level} · {r.qual_vs_quant} · confirmed {r.last_confirmation}
                </div>
                <div className="text-xs mt-1">{r.needs.join(" · ")}</div>
              </div>
            ))}
          </div>
          <div className="rounded-xl border border-[var(--line)] bg-white p-5">
            <h2 className="font-display text-xl mb-3">Approximations (P7)</h2>
            {(report?.approximations_used || []).map((a) => (
              <div key={a.id} className="text-sm border-b border-[var(--line)] py-2">
                <strong>{a.id}</strong> — {a.description}
                <div className="text-xs text-[var(--muted)]">Reliability: {a.reliability}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
