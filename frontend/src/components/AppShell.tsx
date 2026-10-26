"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { clearSession } from "@/lib/api";

type NavItem = { href: string; label: string; hint?: string };

type NavGroup = {
  id: string;
  title: string;
  subtitle: string;
  items: NavItem[];
};

/**
 * Grouped by why the screen exists (not by acronym):
 * - Oversight: risk / supervisory numbers & report outputs
 * - Frameworks: regulatory arrangement packs & programme
 * - Data controls: DWH quality, lineage, taxonomy, distribution
 */
const NAV_GROUPS: NavGroup[] = [
  {
    id: "oversight",
    title: "Эрсдэл & тайлан",
    subtitle: "Бизнесийн тоо · supervisory view",
    items: [
      { href: "/dashboard", label: "SREP", hint: "Executive dashboard" },
      { href: "/risk-report", label: "Risk Report", hint: "Comprehensive risk" },
      { href: "/concentrations", label: "Concentrations", hint: "P4 · P6" },
      { href: "/kri", label: "KRI", hint: "Risk appetite" },
      { href: "/ops-reports", label: "Ops Reports", hint: "PRPT · Core · завсар" },
      { href: "/reports", label: "Reg Reports", hint: "M1 · SREP export" },
    ],
  },
  {
    id: "frameworks",
    title: "Засаглал & стандарт",
    subtitle: "Regulatory frameworks",
    items: [
      { href: "/rdarr", label: "RDARR Pack", hint: "SSM management pack" },
      { href: "/bcbs", label: "BCBS 239", hint: "Principles" },
      { href: "/ict", label: "ICT Security", hint: "EBA/GL/2019/04" },
      { href: "/governance", label: "Governance", hint: "EBA/GL/2021/05" },
      { href: "/programme", label: "Programme", hint: "Implementation" },
    ],
  },
  {
    id: "data",
    title: "DWH хяналт",
    subtitle: "Data quality · lineage · taxonomy",
    items: [
      { href: "/scope", label: "Scope", hint: "CDE · models" },
      { href: "/lineage", label: "Lineage", hint: "Source → mart" },
      { href: "/quality", label: "DQ", hint: "Quality KPIs" },
      { href: "/timeliness", label: "Timeliness", hint: "SLA · stress" },
      { href: "/distribution", label: "Distribution", hint: "Recipients" },
      { href: "/dictionary", label: "Dictionary", hint: "Metadata" },
      { href: "/dpm", label: "DPM", hint: "Data Point Model" },
    ],
  },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setName(localStorage.getItem("bbsb_name") || "");
    setRole(localStorage.getItem("bbsb_role") || "");
  }, []);

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  function pathActive(href: string) {
    return pathname === href || pathname.startsWith(`${href}/`);
  }

  const activeGroupId = useMemo(() => {
    for (const g of NAV_GROUPS) {
      if (g.items.some((i) => pathname === i.href || pathname.startsWith(`${i.href}/`))) return g.id;
    }
    return NAV_GROUPS[0].id;
  }, [pathname]);

  function toggleGroup(id: string) {
    setCollapsed((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  function isGroupOpen(id: string) {
    if (collapsed[id] === undefined) return true;
    return !collapsed[id];
  }

  const sidebar = (
    <div className="flex h-full flex-col">
      <div className="px-4 pt-5 pb-4 border-b border-[var(--line)]">
        <Link href="/dashboard" className="block group" onClick={() => setMobileOpen(false)}>
          <span className="font-display text-2xl tracking-tight text-[var(--ink)] group-hover:text-[var(--accent)] transition-colors">
            DWH<span className="text-[var(--accent)]">_v1</span>
          </span>
          <p className="mt-1 text-[11px] leading-snug text-[var(--muted)]">
            Дата засаглал & тайлагналын платформ
          </p>
        </Link>
        <div className="mt-3 flex items-center gap-2">
          <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-900">
            SSM Demo
          </span>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-1">
        {NAV_GROUPS.map((group) => {
          const open = isGroupOpen(group.id);
          const groupActive = activeGroupId === group.id;
          return (
            <div key={group.id} className="pb-2">
              <button
                type="button"
                onClick={() => toggleGroup(group.id)}
                className={`w-full flex items-start justify-between gap-2 rounded-lg px-2.5 py-2 text-left transition ${
                  groupActive ? "bg-black/[0.04]" : "hover:bg-black/[0.03]"
                }`}
              >
                <span>
                  <span
                    className={`block text-[11px] font-semibold uppercase tracking-[0.12em] ${
                      groupActive ? "text-[var(--accent)]" : "text-[var(--muted)]"
                    }`}
                  >
                    {group.title}
                  </span>
                  <span className="block text-[10px] text-[var(--muted)]/80 mt-0.5">{group.subtitle}</span>
                </span>
                <span className="text-[var(--muted)] text-xs mt-0.5 shrink-0" aria-hidden>
                  {open ? "−" : "+"}
                </span>
              </button>

              {open && (
                <ul className="mt-0.5 space-y-0.5 ml-1 border-l border-[var(--line)] pl-2">
                  {group.items.map((item) => {
                    const active = pathActive(item.href);
                    return (
                      <li key={item.href}>
                        <Link
                          href={item.href}
                          onClick={() => setMobileOpen(false)}
                          className={`block rounded-md px-2.5 py-1.5 transition ${
                            active
                              ? "bg-[var(--ink)] text-white shadow-sm"
                              : "text-[var(--ink)]/85 hover:bg-black/[0.05]"
                          }`}
                        >
                          <span className="block text-[13px] leading-tight">{item.label}</span>
                          {item.hint ? (
                            <span
                              className={`block text-[10px] mt-0.5 leading-tight ${
                                active ? "text-white/70" : "text-[var(--muted)]"
                              }`}
                            >
                              {item.hint}
                            </span>
                          ) : null}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          );
        })}
      </nav>

      <div className="border-t border-[var(--line)] p-3 space-y-2">
        <div className="px-1">
          <p className="text-sm text-[var(--ink)] truncate">{name || "—"}</p>
          <p className="text-[11px] uppercase tracking-wider text-[var(--muted)]">{role || "—"}</p>
        </div>
        <button
          type="button"
          className="w-full rounded-md border border-[var(--line)] bg-white/70 px-3 py-2 text-xs text-[var(--accent)] hover:bg-white transition"
          onClick={() => {
            clearSession();
            router.push("/login");
          }}
        >
          Гарах
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen lg:flex">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex lg:w-[260px] xl:w-[280px] shrink-0 flex-col border-r border-[var(--line)] bg-[var(--surface)]/95 backdrop-blur-md sticky top-0 h-screen">
        {sidebar}
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <button
            type="button"
            className="absolute inset-0 bg-[var(--ink)]/40"
            aria-label="Close menu"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="absolute left-0 top-0 h-full w-[min(88vw,300px)] bg-[var(--surface)] shadow-xl border-r border-[var(--line)]">
            {sidebar}
          </aside>
        </div>
      )}

      <div className="flex-1 min-w-0 flex flex-col min-h-screen">
        <header className="lg:hidden sticky top-0 z-40 border-b border-[var(--line)] bg-[var(--surface)]/95 backdrop-blur-md">
          <div className="flex items-center justify-between gap-3 px-4 py-3">
            <button
              type="button"
              onClick={() => setMobileOpen(true)}
              className="rounded-md border border-[var(--line)] bg-white/80 px-2.5 py-1.5 text-xs text-[var(--ink)]"
              aria-label="Open menu"
            >
              Цэс
            </button>
            <Link href="/dashboard" className="font-display text-lg tracking-tight">
              DWH<span className="text-[var(--accent)]">_v1</span>
            </Link>
            <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-900">
              Demo
            </span>
          </div>
        </header>

        <main className="flex-1 mx-auto w-full max-w-[1400px] px-4 sm:px-6 py-6 sm:py-8">{children}</main>
      </div>
    </div>
  );
}
