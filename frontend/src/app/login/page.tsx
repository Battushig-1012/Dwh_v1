"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, setSession } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("risk");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await api<{ access_token: string; role: string; full_name: string }>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      setSession(res.access_token, res.role, res.full_name);
      router.push("/dashboard");
    } catch {
      setError("Нэвтрэх нэр эсвэл нууц үг буруу байна.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      <section className="relative overflow-hidden px-8 py-16 lg:px-16 flex flex-col justify-end">
        <div
          className="absolute inset-0 opacity-90"
          style={{
            background:
              "linear-gradient(145deg, #0d3b32 0%, #163a4a 45%, #1b2a33 100%)",
          }}
        />
        <div className="absolute inset-0 opacity-30"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 20%, rgba(255,255,255,0.25), transparent 35%), radial-gradient(circle at 80% 60%, rgba(196,92,38,0.35), transparent 40%)",
          }}
        />
        <div className="relative z-10 text-white max-w-lg">
          <p className="font-display text-5xl leading-tight tracking-tight">ББСБ</p>
          <h1 className="mt-4 font-display text-2xl leading-snug text-white/95">
            Нэгдсэн Дата Засаглал & Тайлагналын Платформ
          </h1>
          <p className="mt-4 text-white/75 text-base leading-relaxed">
            SREP · BCBS 239 · DAMA-DMBOK — PostgreSQL DWH дээр суурилсан custom enterprise платформ.
          </p>
        </div>
      </section>

      <section className="flex items-center justify-center px-6 py-12">
        <form onSubmit={onSubmit} className="w-full max-w-md space-y-5">
          <div>
            <h2 className="font-display text-3xl text-[var(--ink)]">Нэвтрэх</h2>
            <p className="mt-2 text-sm text-[var(--muted)]">
              MVP Demo горим — risk / ChangeMe123! (ceo, report, auditor, admin)
            </p>
          </div>
          <label className="block space-y-1.5">
            <span className="text-sm text-[var(--muted)]">Хэрэглэгч</span>
            <input
              className="w-full rounded-lg border border-[var(--line)] bg-white px-3 py-2.5 outline-none focus:ring-2 focus:ring-[var(--accent)]/40"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>
          <label className="block space-y-1.5">
            <span className="text-sm text-[var(--muted)]">Нууц үг</span>
            <input
              type="password"
              className="w-full rounded-lg border border-[var(--line)] bg-white px-3 py-2.5 outline-none focus:ring-2 focus:ring-[var(--accent)]/40"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          {error ? <p className="text-sm text-rose-700">{error}</p> : null}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-[var(--ink)] text-white py-2.5 font-medium hover:bg-[var(--accent)] transition disabled:opacity-60"
          >
            {loading ? "Шалгаж байна..." : "Системд нэвтрэх"}
          </button>
        </form>
      </section>
    </div>
  );
}
