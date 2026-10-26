"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Prog = {
  programme: {
    name: string;
    sponsor: string;
    status: string;
    overall_progress_pct: number;
    milestones: { id: string; title: string; due: string; status: string; progress_pct: number }[];
  };
  bcbs239: { principle: string; ssm_ref: string; score: number; max: number; gap: string }[];
};

type Gov = {
  management_body: { rdarr_sponsors: { role: string; name: string }[] };
  roles: { function: string; line: string; name: string; duties: string[] }[];
};

export default function ProgrammePage() {
  const router = useRouter();
  const [prog, setProg] = useState<Prog | null>(null);
  const [gov, setGov] = useState<Gov | null>(null);
  const [issues, setIssues] = useState<
    { issue_id: string; title: string; severity: string; status: string; remediation_plan: string; due_at: string }[]
  >([]);
  const [workarounds, setWorkarounds] = useState<
    { id: string; name: string; status: string; controls: string[]; target_automation: string }[]
  >([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Prog>("/api/rdarr/programme"),
      api<Gov>("/api/rdarr/governance"),
      api<typeof issues>("/api/rdarr/dq-issues"),
      api<typeof workarounds>("/api/rdarr/workarounds"),
    ]).then(([p, g, i, w]) => {
      setProg(p);
      setGov(g);
      setIssues(i);
      setWorkarounds(w);
    });
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-8">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">SSM §3.3 / §3.5 / §3.7</p>
          <h1 className="font-display text-4xl mt-1">Governance & Implementation</h1>
          <p className="mt-2 text-[var(--muted)]">
            {prog?.programme.name} — Sponsor: {prog?.programme.sponsor} · {prog?.programme.overall_progress_pct}%
          </p>
        </div>

        <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
          <h2 className="font-display text-xl mb-3">Milestones (3.7)</h2>
          <div className="space-y-3">
            {(prog?.programme.milestones || []).map((m) => (
              <div key={m.id}>
                <div className="flex justify-between text-sm mb-1">
                  <span>
                    <strong>{m.id}</strong> {m.title}
                  </span>
                  <span className="text-[var(--muted)]">
                    {m.status} · due {m.due}
                  </span>
                </div>
                <div className="h-2 rounded bg-black/10 overflow-hidden">
                  <div className="h-full bg-[var(--accent)]" style={{ width: `${m.progress_pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-[var(--line)] bg-white p-5 overflow-x-auto">
          <h2 className="font-display text-xl mb-3">BCBS 239 self-assessment</h2>
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-[var(--muted)]">
                <th className="py-1">Principle</th>
                <th>SSM</th>
                <th>Score</th>
                <th>Gap</th>
              </tr>
            </thead>
            <tbody>
              {(prog?.bcbs239 || []).map((b) => (
                <tr key={b.principle} className="border-t border-[var(--line)] align-top">
                  <td className="py-1.5">{b.principle}</td>
                  <td>{b.ssm_ref}</td>
                  <td>
                    {b.score}/{b.max}
                  </td>
                  <td className="text-[var(--muted)]">{b.gap}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="grid lg:grid-cols-2 gap-6">
          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
            <h2 className="font-display text-xl mb-3">Three lines (3.3)</h2>
            <ul className="space-y-3 text-sm">
              {(gov?.roles || []).map((r) => (
                <li key={r.function}>
                  <div className="font-medium">
                    {r.function} <span className="text-xs text-[var(--muted)]">({r.line})</span>
                  </div>
                  <div className="text-[var(--muted)]">{r.name}</div>
                  <div className="text-xs mt-1">{r.duties.join(" · ")}</div>
                </li>
              ))}
            </ul>
          </div>

          <div className="space-y-4">
            <div className="rounded-xl border border-[var(--line)] bg-white p-5">
              <h2 className="font-display text-xl mb-3">DQ Issue Register (3.5)</h2>
              {(issues || []).map((i) => (
                <div key={i.issue_id} className="border-b border-[var(--line)] py-2 text-sm">
                  <div className="font-medium">
                    {i.issue_id} · {i.severity} · {i.status}
                  </div>
                  <div>{i.title}</div>
                  <div className="text-xs text-[var(--muted)] mt-1">
                    Due {i.due_at} — {i.remediation_plan}
                  </div>
                </div>
              ))}
            </div>
            <div className="rounded-xl border border-[var(--line)] bg-white p-5">
              <h2 className="font-display text-xl mb-3">EUC / Manual workarounds</h2>
              {(workarounds || []).map((w) => (
                <div key={w.id} className="border-b border-[var(--line)] py-2 text-sm">
                  <div className="font-medium">
                    {w.id} · {w.status}
                  </div>
                  <div>{w.name}</div>
                  <div className="text-xs text-[var(--muted)]">Controls: {w.controls.join(", ")}</div>
                  <div className="text-xs">Target: {w.target_automation}</div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
