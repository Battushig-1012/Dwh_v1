"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import AppShell from "@/components/AppShell";
import KpiCard from "@/components/KpiCard";
import { api, getToken } from "@/lib/api";

type Overview = {
  standard: string;
  as_of: string;
  scorecard: { title: string; status: string; evidence: string }[];
  proportionality: { applied: boolean; criteria: string[]; note: string };
  open_coi: number;
  committee_count: number;
  control_functions: number;
};

type Tab = "overview" | "body" | "org" | "conduct" | "controls" | "bcm";

function statusTone(s: string) {
  if (s === "APPLIED" || s === "ADEQUATE" || s === "MITIGATED") return "text-emerald-700 bg-emerald-50";
  if (s === "LINKED" || s === "DOCUMENTED" || s === "APPROVED_WITH_CONDITIONS") return "text-sky-800 bg-sky-50";
  return "text-amber-800 bg-amber-50";
}

export default function GovernancePage() {
  const router = useRouter();
  const [ov, setOv] = useState<Overview | null>(null);
  const [body, setBody] = useState<any>(null);
  const [org, setOrg] = useState<any>(null);
  const [conduct, setConduct] = useState<any>(null);
  const [controls, setControls] = useState<any>(null);
  const [bcm, setBcm] = useState<any>(null);
  const [tab, setTab] = useState<Tab>("overview");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([
      api<Overview>("/api/governance/overview"),
      api("/api/governance/management-body"),
      api("/api/governance/organisation"),
      api("/api/governance/conduct"),
      api("/api/governance/controls"),
      api("/api/governance/bcm-transparency"),
    ]).then(([a, b, c, d, e, f]) => {
      setOv(a);
      setBody(b);
      setOrg(c);
      setConduct(d);
      setControls(e);
      setBcm(f);
    });
  }, [router]);

  const mb = body?.management_body;
  const tabs: [Tab, string][] = [
    ["overview", "I–VII Scorecard"],
    ["body", "II Body & committees"],
    ["org", "III Organisation"],
    ["conduct", "IV Conduct / CoI"],
    ["controls", "V 3LOD / NPAC"],
    ["bcm", "VI–VII BCM & transparency"],
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">EBA/GL/2021/05 · CRD</p>
          <h1 className="font-display text-4xl mt-1">Internal Governance</h1>
          <p className="mt-2 text-[var(--muted)] max-w-3xl">
            {ov?.standard || "Guidelines on internal governance under Directive 2013/36/EU"} — Titles I–VII
            (proportionality, management body, know-your-structure, risk culture, 3LOD, BCM, transparency).
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard title="As of" value={ov?.as_of || "—"} hint="Assessment date" />
          <KpiCard
            title="Proportionality"
            value={ov?.proportionality.applied ? "ON" : "OFF"}
            hint={ov?.proportionality.note}
            tone={ov?.proportionality.applied ? "ok" : "warn"}
          />
          <KpiCard title="Committees" value={String(ov?.committee_count ?? "—")} hint="Supervisory function" />
          <KpiCard
            title="Open CoI"
            value={String(ov?.open_coi ?? "—")}
            hint={`${ov?.control_functions ?? "—"} control functions`}
            tone={(ov?.open_coi ?? 0) > 0 ? "warn" : "ok"}
          />
        </div>

        <div className="flex gap-1 flex-wrap">
          {tabs.map(([id, label]) => (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`px-3 py-1.5 text-xs rounded-md ${tab === id ? "bg-[var(--ink)] text-white" : "bg-black/5 text-[var(--muted)]"}`}
            >
              {label}
            </button>
          ))}
        </div>

        {tab === "overview" && (
          <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-black/[0.03] text-left text-xs text-[var(--muted)]">
                <tr>
                  <th className="px-4 py-2 font-medium">Title</th>
                  <th className="px-4 py-2 font-medium">Status</th>
                  <th className="px-4 py-2 font-medium">Evidence on platform</th>
                </tr>
              </thead>
              <tbody>
                {ov?.scorecard.map((row) => (
                  <tr key={row.title} className="border-t border-[var(--line)]">
                    <td className="px-4 py-3 font-medium">{row.title}</td>
                    <td className="px-4 py-3">
                      <span className={`text-[10px] uppercase tracking-wide px-2 py-0.5 rounded ${statusTone(row.status)}`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-[var(--muted)]">{row.evidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="px-4 py-3 text-xs text-[var(--muted)] border-t border-[var(--line)]">
              Criteria: {(ov?.proportionality.criteria || []).join(" · ")}. RDARR / ICT / DPM modules remain authoritative for
              data, ICT security and reporting taxonomy — this pack covers CRD Art. 74/88 governance arrangements.
            </div>
          </section>
        )}

        {tab === "body" && mb && (
          <div className="space-y-4">
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
              <h2 className="font-display text-xl">Management body</h2>
              <p className="text-sm text-[var(--muted)] mt-1">
                Structure: {mb.structure} · Chair: {mb.chair.name} ({mb.chair.role})
              </p>
              <div className="mt-4 grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <h3 className="text-xs uppercase tracking-wider text-[var(--muted)] mb-2">Management function</h3>
                  <ul className="space-y-1">
                    {mb.management_function.map((p: any) => (
                      <li key={p.username} className="flex justify-between gap-2 border-b border-[var(--line)] py-1.5">
                        <span>{p.name}</span>
                        <span className="text-[var(--muted)] text-xs">{p.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xs uppercase tracking-wider text-[var(--muted)] mb-2">Supervisory function</h3>
                  <ul className="space-y-1">
                    {mb.supervisory_function.map((p: any) => (
                      <li key={p.name} className="flex justify-between gap-2 border-b border-[var(--line)] py-1.5">
                        <span>{p.name}</span>
                        <span className="text-[var(--muted)] text-xs">{p.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="mt-4 rounded-lg bg-black/[0.03] p-3 text-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium">Collective suitability</span>
                  <span className={`text-[10px] uppercase px-2 py-0.5 rounded ${statusTone(mb.collective_suitability.status)}`}>
                    {mb.collective_suitability.status}
                  </span>
                  <span className="text-xs text-[var(--muted)]">last {mb.collective_suitability.last_assessment}</span>
                </div>
                <p className="text-xs text-[var(--muted)] mt-1">{mb.collective_suitability.covers.join(" · ")}</p>
              </div>
              <ul className="mt-3 text-sm text-[var(--muted)] list-disc pl-5 space-y-1">
                {mb.responsibilities_highlights.map((r: string) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
            </section>

            {(body.committees || []).map((c: any) => (
              <section key={c.code} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
                <div className="flex flex-wrap justify-between gap-2">
                  <h2 className="font-display text-xl">{c.name}</h2>
                  <span className="text-xs text-[var(--muted)]">
                    {c.meeting_frequency} · last {c.last_meeting} · next {c.next_meeting}
                  </span>
                </div>
                <p className="text-sm mt-1">
                  Chair: {c.chair} · Members: {c.members.join(", ")}
                </p>
                <ul className="mt-3 text-sm list-disc pl-5 space-y-1 text-[var(--muted)]">
                  {c.mandate.map((m: string) => (
                    <li key={m}>{m}</li>
                  ))}
                </ul>
              </section>
            ))}

            {body.meeting_pack && (
              <section className="rounded-xl border border-[var(--line)] bg-white p-5 text-sm">
                <h3 className="font-medium">Committee pack (demo)</h3>
                <p className="text-xs text-[var(--muted)] mt-1">
                  For {body.meeting_pack.for_committee} · as of {body.meeting_pack.as_of}
                </p>
                <ul className="mt-2 list-disc pl-5 space-y-1 text-[var(--muted)]">
                  {body.meeting_pack.agenda_items.map((a: string) => (
                    <li key={a}>{a}</li>
                  ))}
                </ul>
              </section>
            )}
          </div>
        )}

        {tab === "org" && org && (
          <div className="space-y-4">
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5">
              <h2 className="font-display text-xl">Know-your-structure</h2>
              <div className="mt-3 overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="text-xs text-[var(--muted)] text-left">
                    <tr>
                      <th className="py-1 pr-3">Code</th>
                      <th className="py-1 pr-3">Entity</th>
                      <th className="py-1 pr-3">Jurisdiction</th>
                      <th className="py-1 pr-3">Activity</th>
                      <th className="py-1">Booked</th>
                    </tr>
                  </thead>
                  <tbody>
                    {org.structure.legal_entities.map((e: any) => (
                      <tr key={e.code} className="border-t border-[var(--line)]">
                        <td className="py-2 pr-3 font-mono text-xs">{e.code}</td>
                        <td className="py-2 pr-3">{e.name}</td>
                        <td className="py-2 pr-3">{e.jurisdiction}</td>
                        <td className="py-2 pr-3 text-[var(--muted)]">{e.activity}</td>
                        <td className="py-2">{e.booked ? "Yes" : "No"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-sm mt-3">
                <span className="font-medium">Business lines:</span> {org.structure.business_lines.join(" · ")}
              </p>
              <p className="text-sm mt-1">
                <span className="font-medium">Key functions:</span> {org.structure.key_functions.join(" · ")}
              </p>
              <p className="text-xs text-[var(--muted)] mt-3">{org.structure.complex_structures.note}</p>
              <p className="text-xs text-[var(--muted)] mt-1">{org.structure.group_context.note}</p>
            </section>
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h3 className="font-medium">Outsourcing policy (GL §8)</h3>
              <p className="text-[var(--muted)] mt-1">
                Exists: {org.structure.outsourcing_policy.exists ? "Yes" : "No"} · last review{" "}
                {org.structure.outsourcing_policy.last_review}
              </p>
              <p className="mt-2">Critical: {org.structure.outsourcing_policy.critical_outsourced.join("; ")}</p>
              <p className="text-xs text-[var(--muted)] mt-2">
                {org.structure.outsourcing_policy.link} →{" "}
                <Link href="/ict" className="text-[var(--accent)] hover:underline">
                  ICT module
                </Link>
              </p>
            </section>
          </div>
        )}

        {tab === "conduct" && conduct && (
          <div className="space-y-4">
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h2 className="font-display text-xl">Risk culture</h2>
              <p className="mt-2 text-[var(--muted)]">{conduct.risk_culture.tone_from_top}</p>
              <p className="mt-2 text-xs uppercase tracking-wider text-[var(--muted)]">
                {conduct.risk_culture.principles.join(" · ")}
              </p>
              <div className="mt-4 rounded-lg bg-black/[0.03] p-3">
                <div className="font-medium">
                  Code of conduct v{conduct.risk_culture.code_of_conduct.version}
                </div>
                <p className="text-xs text-[var(--muted)] mt-1">
                  Approved {conduct.risk_culture.code_of_conduct.approved_at} · attestation{" "}
                  {conduct.risk_culture.code_of_conduct.last_attestation_pct}%
                </p>
                <p className="text-xs mt-1">{conduct.risk_culture.code_of_conduct.topics.join(" · ")}</p>
              </div>
            </section>

            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] overflow-hidden">
              <div className="px-5 py-3 border-b border-[var(--line)] font-medium text-sm">Conflicts of interest</div>
              <table className="w-full text-sm">
                <thead className="text-xs text-[var(--muted)] text-left bg-black/[0.03]">
                  <tr>
                    <th className="px-4 py-2">Case</th>
                    <th className="px-4 py-2">Type</th>
                    <th className="px-4 py-2">Status</th>
                    <th className="px-4 py-2">Control</th>
                  </tr>
                </thead>
                <tbody>
                  {conduct.conflicts_of_interest.map((c: any) => (
                    <tr key={c.case_id} className="border-t border-[var(--line)]">
                      <td className="px-4 py-3">
                        <div className="font-mono text-xs">{c.case_id}</div>
                        <div className="text-[var(--muted)] text-xs mt-0.5">{c.party}</div>
                      </td>
                      <td className="px-4 py-3 text-xs">{c.type}</td>
                      <td className="px-4 py-3">
                        <span className={`text-[10px] uppercase px-2 py-0.5 rounded ${statusTone(c.status)}`}>
                          {c.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-[var(--muted)] text-xs">{c.control}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h3 className="font-medium">Whistleblowing (GL §14)</h3>
              <p className="mt-2 text-[var(--muted)]">
                Channels: {conduct.whistleblowing.internal_alert_channels.join(" · ")}
              </p>
              <p className="mt-1 text-xs text-[var(--muted)]">
                Protection: {conduct.whistleblowing.protects_whistleblowers ? "Yes" : "No"} · training{" "}
                {conduct.whistleblowing.training_last}
              </p>
              <p className="mt-2 text-xs">{conduct.whistleblowing.reporting_to_authority}</p>
            </section>
          </div>
        )}

        {tab === "controls" && controls && (
          <div className="space-y-4">
            <div className="grid md:grid-cols-3 gap-3">
              {controls.three_lines.map((l: any) => (
                <section key={l.line} className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 text-sm">
                  <div className="text-xs uppercase tracking-wider text-[var(--muted)]">{l.line}</div>
                  <h3 className="font-medium mt-1">{l.name}</h3>
                  <p className="text-xs text-[var(--muted)] mt-2">{l.units.join(" · ")}</p>
                  <p className="mt-2 text-[var(--muted)]">{l.duty}</p>
                </section>
              ))}
            </div>

            {controls.control_functions.map((f: any) => (
              <section key={f.function} className="rounded-xl border border-[var(--line)] bg-white p-5 text-sm">
                <div className="flex flex-wrap justify-between gap-2">
                  <h3 className="font-medium">{f.function}</h3>
                  <span className="text-xs text-[var(--muted)]">
                    {f.head} → {f.reports_to}
                  </span>
                </div>
                <p className="text-xs text-[var(--muted)] mt-1">
                  Independent: {f.independent ? "Yes" : "No"} · {f.resources}
                </p>
                <ul className="mt-2 list-disc pl-5 space-y-1 text-[var(--muted)]">
                  {f.key_duties.map((d: string) => (
                    <li key={d}>{d}</li>
                  ))}
                </ul>
              </section>
            ))}

            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h3 className="font-medium">New product approval (GL §18)</h3>
              <p className="text-[var(--muted)] mt-1">{controls.new_products.process}</p>
              {(controls.new_products.recent || []).map((p: any) => (
                <div key={p.id} className="mt-3 flex flex-wrap items-center gap-2 border-t border-[var(--line)] pt-3">
                  <span className="font-mono text-xs">{p.id}</span>
                  <span>{p.product}</span>
                  <span className={`text-[10px] uppercase px-2 py-0.5 rounded ${statusTone(p.status)}`}>{p.status}</span>
                  <span className="text-xs text-[var(--muted)]">{p.risk_opinion}</span>
                </div>
              ))}
            </section>
          </div>
        )}

        {tab === "bcm" && bcm && (
          <div className="space-y-4">
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h2 className="font-display text-xl">Title VI — Business continuity</h2>
              <p className="mt-2">Owned by: {bcm.bcm.owned_by}</p>
              <p className="text-[var(--muted)] mt-1">
                Policy approved: {bcm.bcm.policy_approved ? "Yes" : "No"} · Detail: {bcm.bcm.detail_module}
              </p>
              <p className="mt-3">
                <Link href="/ict" className="text-[var(--accent)] hover:underline">
                  Open ICT BCM
                </Link>
                {" · "}
                <Link href="/bcbs" className="text-[var(--accent)] hover:underline">
                  BCBS BCP
                </Link>
              </p>
            </section>
            <section className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5 text-sm">
              <h2 className="font-display text-xl">Title VII — Transparency</h2>
              <div className="grid md:grid-cols-2 gap-4 mt-3">
                <div>
                  <h3 className="text-xs uppercase tracking-wider text-[var(--muted)]">Internal</h3>
                  <ul className="mt-2 list-disc pl-5 space-y-1 text-[var(--muted)]">
                    {bcm.transparency.internal.map((x: string) => (
                      <li key={x}>{x}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xs uppercase tracking-wider text-[var(--muted)]">External</h3>
                  <ul className="mt-2 list-disc pl-5 space-y-1 text-[var(--muted)]">
                    {bcm.transparency.external.map((x: string) => (
                      <li key={x}>{x}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <p className="text-xs text-[var(--muted)] mt-4">{bcm.transparency.website_governance_summary}</p>
            </section>
          </div>
        )}
      </div>
    </AppShell>
  );
}
