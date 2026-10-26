"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Overview = {
  standard: string;
  as_of: string;
  open_incidents: number;
  open_audit_findings: number;
  critical_assets: number;
  strategy_approved_at: string;
  scorecard: { section: string; status: string; evidence: string }[];
};

export default function IctPage() {
  const router = useRouter();
  const [ov, setOv] = useState<Overview | null>(null);
  const [strategy, setStrategy] = useState<any>(null);
  const [assets, setAssets] = useState<any>(null);
  const [infosec, setInfosec] = useState<any>(null);
  const [ops, setOps] = useState<any>(null);
  const [chg, setChg] = useState<any>(null);
  const [bcm, setBcm] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [privLog, setPrivLog] = useState<any[]>([]);
  const [tab, setTab] = useState<"overview" | "assets" | "iam" | "ops" | "bcm" | "change">("overview");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Overview>("/api/ict/overview"),
      api("/api/ict/strategy"),
      api("/api/ict/assets"),
      api("/api/ict/information-security"),
      api("/api/ict/operations"),
      api("/api/ict/change"),
      api("/api/ict/bcm"),
      api("/api/ict/audit"),
    ]).then(([a, b, c, d, e, f, g, h]) => {
      setOv(a);
      setStrategy(b);
      setAssets(c);
      setInfosec(d);
      setOps(e);
      setChg(f);
      setBcm(g);
      setAudit(h);
    });
    api<any[]>("/api/ict/privileged-log")
      .then(setPrivLog)
      .catch(() => setPrivLog([]));
  }, [router]);

  const tabs = [
    { id: "overview", label: "Overview 3.1–3.2" },
    { id: "assets", label: "Assets & risks 3.3" },
    { id: "iam", label: "InfoSec / IAM 3.4" },
    { id: "ops", label: "Ops & incidents 3.5" },
    { id: "change", label: "Change 3.6" },
    { id: "bcm", label: "BCM 3.7" },
  ] as const;

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">EBA/GL/2019/04</p>
          <h1 className="font-display text-4xl mt-1">ICT & Security Risk Management</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">{ov?.standard}</p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="Critical assets" value={String(ov?.critical_assets ?? "—")} />
          <KpiCard title="Open incidents" value={String(ov?.open_incidents ?? "—")} tone={(ov?.open_incidents || 0) > 0 ? "warn" : "ok"} />
          <KpiCard title="Audit findings" value={String(ov?.open_audit_findings ?? "—")} tone={(ov?.open_audit_findings || 0) > 0 ? "warn" : "ok"} />
          <KpiCard title="Strategy approved" value={ov?.strategy_approved_at || "—"} />
        </div>

        <div className="flex flex-wrap gap-1">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`px-3 py-1.5 text-xs rounded-md ${tab === t.id ? "bg-[var(--ink)] text-white" : "bg-black/5 text-[var(--muted)]"}`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "overview" && (
          <section className="space-y-4">
            <Box title="Compliance scorecard">
              {(ov?.scorecard || []).map((s) => (
                <Row key={s.section} left={`${s.section} · ${s.status}`} right={s.evidence} />
              ))}
            </Box>
            <Box title="ICT strategy objectives (¶5–6)">
              <ul className="list-disc pl-5 text-sm space-y-1">
                {(strategy?.strategy?.objectives || []).map((o: string) => (
                  <li key={o}>{o}</li>
                ))}
              </ul>
              <h3 className="font-medium text-sm mt-4 mb-2">Action plans</h3>
              {(strategy?.strategy?.action_plans || []).map((a: any) => (
                <Row key={a.id} left={`${a.id} ${a.measure}`} right={`${a.status} · ${a.due}`} />
              ))}
            </Box>
            <Box title="Governance roles (¶2–4, ¶10–12)">
              {(strategy?.governance?.roles || []).map((r: any) => (
                <Row key={r.role} left={r.role} right={r.duty} />
              ))}
            </Box>
            <Box title="Open ICT audit findings (¶25–27)">
              {(audit?.open_findings || []).map((f: any) => (
                <Row key={f.id} left={`${f.id} · ${f.severity}`} right={`${f.title} · due ${f.due}`} />
              ))}
            </Box>
          </section>
        )}

        {tab === "assets" && (
          <section className="space-y-4">
            <Box title="ICT asset inventory (¶15–16, ¶53–55)">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-[var(--muted)]">
                    <th className="py-1">Asset</th>
                    <th>CIA</th>
                    <th>Criticality</th>
                    <th>Depends on</th>
                  </tr>
                </thead>
                <tbody>
                  {(assets?.assets || []).map((a: any) => (
                    <tr key={a.asset_id} className="border-t border-[var(--line)] align-top">
                      <td className="py-1.5">
                        <div className="font-mono text-xs">{a.asset_id}</div>
                        <div>{a.name}</div>
                      </td>
                      <td className="text-xs">
                        C:{a.cia.C} I:{a.cia.I} A:{a.cia.A}
                      </td>
                      <td>{a.criticality}</td>
                      <td className="text-xs text-[var(--muted)]">{(a.depends_on || []).join(", ") || "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Box>
            <Box title="ICT & security risk register (¶20–23)">
              {(assets?.risks || []).map((r: any) => (
                <div key={r.risk_id} className="text-sm border-b border-[var(--line)] py-2">
                  <strong>{r.risk_id}</strong> — {r.threat}
                  <div className="text-xs text-[var(--muted)]">
                    {r.asset} · L:{r.likelihood} I:{r.impact} residual:{r.residual}
                  </div>
                  <div className="text-xs mt-1">{r.mitigation}</div>
                </div>
              ))}
            </Box>
          </section>
        )}

        {tab === "iam" && (
          <section className="space-y-4">
            <Box title="Information security policy (¶28–30)">
              <p className="text-sm">
                v{infosec?.policy?.version} · approved {infosec?.policy?.approved_at} by {infosec?.policy?.approved_by}
              </p>
              <p className="text-xs text-[var(--muted)] mt-2">{infosec?.policy?.scope_note}</p>
              <div className="text-xs mt-2">Principles: {(infosec?.policy?.principles || []).join(", ")}</div>
            </Box>
            <Box title="Logical access / IAM (¶31)">
              <div className="text-xs text-[var(--muted)] mb-2">
                {(infosec?.logical_access?.principles || []).join(" · ")}
              </div>
              {(infosec?.logical_access?.roles_matrix || []).map((r: any) => (
                <Row
                  key={r.username}
                  left={`${r.username} (${r.role})${r.privileged ? " · PRIVILEGED" : ""}`}
                  right={r.systems.join(", ")}
                />
              ))}
              <p className="text-xs mt-3">
                Recertification: {infosec?.logical_access?.recertification?.frequency} · last{" "}
                {infosec?.logical_access?.recertification?.last_review} · next{" "}
                {infosec?.logical_access?.recertification?.next_review}
              </p>
            </Box>
            <Box title="Privileged / access activity log (¶31.d)">
              {privLog.length === 0 ? (
                <p className="text-sm text-[var(--muted)]">No events yet (or insufficient role to view).</p>
              ) : (
                privLog.slice(0, 15).map((e, i) => (
                  <Row key={i} left={`${e.ts} · ${e.username}/${e.role}`} right={`${e.action} ${e.detail || ""}`} />
                ))
              )}
            </Box>
            <Box title="Monitoring · Testing · Awareness">
              <p className="text-sm font-medium">Monitoring</p>
              <ul className="text-xs list-disc pl-5 mb-3">
                {(infosec?.monitoring?.capabilities || []).map((c: string) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
              <p className="text-sm font-medium">Tests</p>
              {(infosec?.testing?.tests || []).map((t: any) => (
                <Row key={t.id} left={`${t.id} ${t.type}`} right={`${t.date} · ${t.result}`} />
              ))}
              <p className="text-xs mt-3">
                Awareness coverage {infosec?.awareness?.coverage_pct}% · last {infosec?.awareness?.last_campaign}
              </p>
            </Box>
          </section>
        )}

        {tab === "ops" && (
          <section className="space-y-4">
            <Box title="Backup & capacity (¶56–58)">
              <Row
                left={`Backup ${ops?.operations?.backup?.frequency}`}
                right={`RTO ${ops?.operations?.backup?.rto_hours}h · RPO ${ops?.operations?.backup?.rpo_hours}h · restore test ${ops?.operations?.backup?.restore_test_result}`}
              />
              <Row
                left="Capacity"
                right={`CPU ${ops?.operations?.capacity?.cpu_pct}% · Disk ${ops?.operations?.capacity?.disk_pct}% · ${ops?.operations?.capacity?.status}`}
              />
            </Box>
            <Box title="Incidents (¶59–60)">
              {(ops?.incidents || []).map((inc: any) => (
                <div key={inc.incident_id} className="text-sm border-b border-[var(--line)] py-2">
                  <strong>
                    {inc.incident_id} · {inc.priority} · {inc.status}
                  </strong>
                  <div>{inc.title}</div>
                  <div className="text-xs text-[var(--muted)]">
                    {inc.category} · impact: {inc.impact}
                  </div>
                  <div className="text-xs">Root cause: {inc.root_cause}</div>
                </div>
              ))}
            </Box>
            <Box title="Third parties (¶7–9)">
              {(ops?.third_parties || []).map((t: any) => (
                <Row key={t.id} left={`${t.id} ${t.name}`} right={`${t.criticality} · ${t.assurance}`} />
              ))}
            </Box>
          </section>
        )}

        {tab === "change" && (
          <section className="space-y-4">
            <Box title="ICT projects (¶61–66)">
              {(chg?.projects || []).map((p: any) => (
                <Row
                  key={p.project_id}
                  left={`${p.project_id} ${p.name}`}
                  right={`${p.status} · security reqs: ${p.security_requirements_embedded}`}
                />
              ))}
            </Box>
            <Box title="Change management (¶75–76)">
              {(chg?.changes || []).map((c: any) => (
                <Row
                  key={c.change_id}
                  left={`${c.change_id} ${c.title}`}
                  right={`${c.status} · risk ${c.risk} · sec review ${c.security_review}`}
                />
              ))}
            </Box>
          </section>
        )}

        {tab === "bcm" && (
          <section className="space-y-4">
            <Box title="Business impact analysis (¶78–79)">
              {(bcm?.bia || []).map((b: any) => (
                <Row
                  key={b.function}
                  left={b.function}
                  right={`MTD ${b.max_tolerable_downtime_h}h · RTO ${b.rto_h}h · RPO ${b.rpo_h}h`}
                />
              ))}
            </Box>
            <Box title="BCP / crisis (¶80–91)">
              <p className="text-sm">
                Last test {bcm?.bcm?.last_bcp_test} · {bcm?.bcm?.bcp_test_result}
              </p>
              <p className="text-xs text-[var(--muted)] mt-2">Scenarios: {(bcm?.bcm?.scenarios || []).join(", ")}</p>
              <p className="text-xs mt-2">Comms: {(bcm?.bcm?.crisis_comms || []).join(" · ")}</p>
            </Box>
          </section>
        )}
      </div>
    </AppShell>
  );
}

function Box({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
      <h2 className="font-display text-xl mb-3">{title}</h2>
      {children}
    </section>
  );
}

function Row({ left, right }: { left: string; right: string }) {
  return (
    <div className="flex flex-col sm:flex-row sm:justify-between gap-1 text-sm border-b border-[var(--line)] py-1.5">
      <span>{left}</span>
      <span className="text-xs text-[var(--muted)] sm:text-right sm:max-w-[55%]">{right}</span>
    </div>
  );
}
