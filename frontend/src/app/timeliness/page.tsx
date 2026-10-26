"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Timeliness = {
  calendar: {
    report_id: string;
    frequency: string;
    sla_working_days: number;
    cutoff: string;
    last_produced: string;
    production_days: number;
    within_sla: boolean;
    ecb_benchmark_max_days?: number;
  }[];
  stress: {
    fire_drill_ready: boolean;
    last_fire_drill: string;
    scenarios: { code: string; name: string; granularity: string; sla_hours: number; last_result: string }[];
    note: string;
  };
  ecb_note: string;
};

export default function TimelinessPage() {
  const router = useRouter();
  const [data, setData] = useState<Timeliness | null>(null);
  const [drillMsg, setDrillMsg] = useState("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Timeliness>("/api/rdarr/timeliness").then(setData);
  }, [router]);

  async function runDrill(code: string) {
    setDrillMsg("Running…");
    try {
      const res = await api<{ result: { message: string; within_sla: boolean } }>(`/api/rdarr/fire-drill/${code}`, {
        method: "POST",
      });
      setDrillMsg(`${res.result.message} · within SLA: ${res.result.within_sla}`);
    } catch (e) {
      setDrillMsg(String(e));
    }
  }

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM Guide §3.6</p>
          <h1 className="font-display text-4xl mt-1">Timeliness & Stress Capability</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">{data?.ecb_note}</p>
        </div>

        <section className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-[var(--ink)] text-white">
              <tr>
                <th className="text-left px-3 py-2">Report</th>
                <th className="text-left px-3 py-2">Frequency</th>
                <th className="text-right px-3 py-2">Prod. days</th>
                <th className="text-right px-3 py-2">SLA</th>
                <th className="text-left px-3 py-2">ECB ≤20 WD</th>
                <th className="text-left px-3 py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {(data?.calendar || []).map((c) => (
                <tr key={c.report_id} className="border-t border-[var(--line)]">
                  <td className="px-3 py-2 font-mono text-xs">{c.report_id}</td>
                  <td className="px-3 py-2">{c.frequency}</td>
                  <td className="px-3 py-2 text-right">{c.production_days}</td>
                  <td className="px-3 py-2 text-right">
                    {c.sla_working_days} ({c.cutoff})
                  </td>
                  <td className="px-3 py-2">{c.ecb_benchmark_max_days ?? "n/a (daily)"}</td>
                  <td className="px-3 py-2">{c.within_sla ? "WITHIN SLA" : "BREACH"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 space-y-4">
          <h2 className="font-display text-xl">Fire-drill / ad-hoc (adaptability)</h2>
          <p className="text-sm text-[var(--muted)]">{data?.stress.note}</p>
          <p className="text-xs">
            Ready: {String(data?.stress.fire_drill_ready)} · Last drill: {data?.stress.last_fire_drill}
          </p>
          <div className="flex flex-wrap gap-2">
            {(data?.stress.scenarios || []).map((s) => (
              <button
                key={s.code}
                onClick={() => runDrill(s.code)}
                className="rounded-lg bg-[var(--ink)] text-white px-3 py-2 text-sm hover:bg-[var(--accent)]"
              >
                Run {s.code}
              </button>
            ))}
          </div>
          {drillMsg ? <p className="text-sm text-[var(--accent)]">{drillMsg}</p> : null}
          <ul className="text-sm space-y-1">
            {(data?.stress.scenarios || []).map((s) => (
              <li key={s.code}>
                <strong>{s.name}</strong> — {s.granularity}, SLA {s.sla_hours}h, last {s.last_result}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </AppShell>
  );
}
