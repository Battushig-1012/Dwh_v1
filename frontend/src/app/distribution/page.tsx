"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";

type Dist = {
  report_id: string;
  classification: string;
  recipients: string[];
  channel: string;
  last_delivered: string;
  ack_required: boolean;
  acks: string[];
};

export default function DistributionPage() {
  const router = useRouter();
  const [rows, setRows] = useState<Dist[]>([]);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Dist[]>("/api/bcbs/distribution").then(setRows);
  }, [router]);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-[var(--muted)]">BCBS P11</p>
          <h1 className="font-display text-4xl mt-1">Report Distribution</h1>
          <p className="mt-2 text-[var(--muted)]">
            Relevant recipients, confidentiality classification, delivery & acknowledgement.
          </p>
        </div>

        <div className="overflow-x-auto rounded-xl border border-[var(--line)] bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-[var(--ink)] text-white">
              <tr>
                <th className="text-left px-3 py-2">Report</th>
                <th className="text-left px-3 py-2">Class</th>
                <th className="text-left px-3 py-2">Recipients</th>
                <th className="text-left px-3 py-2">Channel</th>
                <th className="text-left px-3 py-2">Delivered</th>
                <th className="text-left px-3 py-2">Ack</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.report_id} className="border-t border-[var(--line)] align-top">
                  <td className="px-3 py-2 font-mono text-xs">{r.report_id}</td>
                  <td className="px-3 py-2">{r.classification}</td>
                  <td className="px-3 py-2">{r.recipients.join(", ")}</td>
                  <td className="px-3 py-2">{r.channel}</td>
                  <td className="px-3 py-2 text-xs">{new Date(r.last_delivered).toLocaleString()}</td>
                  <td className="px-3 py-2 text-xs">
                    {r.ack_required ? (r.acks.length ? r.acks.join(", ") : "Pending") : "Not required"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
