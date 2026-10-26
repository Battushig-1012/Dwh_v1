"use client";

import { useEffect, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  Edge,
  MarkerType,
  Node,
  Position,
} from "reactflow";
import "reactflow/dist/style.css";
import AppShell from "@/components/AppShell";
import { api, getToken } from "@/lib/api";
import { useRouter } from "next/navigation";

type Graph = {
  nodes: {
    id: string;
    type: string;
    label: string;
    schema_name?: string;
    table_name?: string;
    description?: string;
  }[];
  edges: { source: string; target: string; transform_type: string; transform_logic?: string }[];
};

const typeColor: Record<string, string> = {
  source: "#163a4a",
  staging: "#5a6a75",
  core: "#0f6e56",
  mart: "#c45c26",
  report: "#7a3e6b",
};

const layers = ["source", "staging", "core", "mart", "report"];

export default function LineagePage() {
  const router = useRouter();
  const [graph, setGraph] = useState<Graph | null>(null);
  const [selected, setSelected] = useState<string>("");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<Graph>("/api/lineage/graph").then(setGraph);
  }, [router]);

  const { nodes, edges } = useMemo(() => {
    if (!graph) return { nodes: [] as Node[], edges: [] as Edge[] };
    const byType: Record<string, typeof graph.nodes> = {};
    for (const n of graph.nodes) {
      byType[n.type] = byType[n.type] || [];
      byType[n.type].push(n);
    }
    const flowNodes: Node[] = [];
    layers.forEach((layer, xi) => {
      (byType[layer] || []).forEach((n, yi) => {
        flowNodes.push({
          id: n.id,
          position: { x: xi * 240, y: yi * 110 },
          data: { label: n.label },
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          style: {
            background: typeColor[n.type] || "#333",
            color: "#fff",
            border: "none",
            borderRadius: 10,
            padding: 10,
            width: 180,
            fontSize: 12,
          },
        });
      });
    });
    const flowEdges: Edge[] = graph.edges.map((e, i) => ({
      id: `e-${i}`,
      source: e.source,
      target: e.target,
      label: e.transform_type,
      markerEnd: { type: MarkerType.ArrowClosed },
      style: { stroke: "#8a8074" },
      labelStyle: { fontSize: 10, fill: "#5a6a75" },
    }));
    return { nodes: flowNodes, edges: flowEdges };
  }, [graph]);

  const detail = graph?.nodes.find((n) => n.id === selected);
  const edgeDetail = graph?.edges.filter((e) => e.source === selected || e.target === selected);

  return (
    <AppShell>
      <div className="space-y-4">
        <div>
          <h1 className="font-display text-4xl">Data Lineage</h1>
          <p className="mt-2 text-[var(--muted)]">
            Эх систем → Staging → DWH Core → Mart → Тайлан (BCBS 239)
          </p>
        </div>
        <div className="h-[520px] rounded-xl border border-[var(--line)] bg-white overflow-hidden">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            fitView
            onNodeClick={(_, n) => setSelected(n.id)}
          >
            <Background gap={18} color="#e6e1d8" />
            <Controls />
          </ReactFlow>
        </div>
        {detail ? (
          <div className="rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 text-sm">
            <p className="font-display text-lg">{detail.label}</p>
            <p className="text-[var(--muted)] mt-1">
              {detail.type}
              {detail.schema_name ? ` · ${detail.schema_name}.${detail.table_name}` : ""}
            </p>
            <p className="mt-2">{detail.description}</p>
            <ul className="mt-3 space-y-1 text-[var(--muted)]">
              {(edgeDetail || []).map((e, i) => (
                <li key={i}>
                  {e.source} → {e.target}: {e.transform_logic || e.transform_type}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </AppShell>
  );
}
