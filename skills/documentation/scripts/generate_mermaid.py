#!/usr/bin/env python3
"""
generate_mermaid.py - Converte o inventario gerado por scan_endpoints.py em
dois arquivos Mermaid:

  1. <prefix>-sequence.mmd  -> sequenceDiagram, um bloco por endpoint
  2. <prefix>-flow.mmd      -> flowchart com endpoints e suas fronteiras

Uso:
    python generate_mermaid.py inventory.json --out-dir ./diagrams
    python generate_mermaid.py inventory.json --flow-style summary
    python generate_mermaid.py inventory.json --split-sequence   # 1 arquivo por tag
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SHAPE = {
    "database": ("[(", ")]"),   # cilindro
    "cache": ("[(", ")]"),
    "queue": ("[/", "/]"),      # paralelogramo
    "storage": ("[(", ")]"),
    "external_api": ("[", "]"),
}

ARROW = {"database": "->>", "cache": "->>", "queue": "->>",
         "external_api": "->>", "storage": "->>"}


def ident(text, prefix=""):
    """ID seguro para Mermaid."""
    s = re.sub(r"[^0-9a-zA-Z]+", "_", text).strip("_")
    if not s:
        s = "n"
    if s[0].isdigit():
        s = "n" + s
    return prefix + s


def esc(text):
    """Rotulo entre aspas (flowchart). Preserva {param} do path."""
    return (str(text).replace('"', "&quot;").replace("\n", " ")
            .replace("#", "num ").strip())


def esc_msg(text):
    """Mensagem de sequenceDiagram: nao vai entre aspas, entao ; e # quebram."""
    return (str(text).replace("\n", " ").replace(";", ",")
            .replace("#", "num ").replace('"', "'").strip())


def sequence_diagram(inv, endpoints, autonumber=False, response=None):
    app_id = "API"
    lines = ["sequenceDiagram"]
    if autonumber:
        lines.append("    autonumber")
    lines.append(f'    participant Client as Client')
    lines.append(f'    participant {app_id} as {esc(inv["app_name"])}')

    used = []
    for ep in endpoints:
        for st in ep["steps"]:
            if st["system"] not in used:
                used.append(st["system"])
    for sysname in used:
        meta = inv["systems"].get(sysname, {"label": sysname})
        lines.append(f'    participant {ident(sysname)} as {esc(meta["label"])}')
    lines.append("")

    for ep in endpoints:
        title = f'{ep["method"]} {ep["path"]}'
        lines.append(f'    Note over Client,{app_id}: {esc_msg(title)}')
        lines.append(f'    Client->>{app_id}: {esc_msg(title)}')
        for st in ep["steps"]:
            sid = ident(st["system"])
            arrow = ARROW.get(st["kind"], "->>")
            lines.append(f'    {app_id}{arrow}{sid}: {esc_msg(st["operation"])}')
            if st["kind"] in {"database", "cache", "external_api", "storage"}:
                lines.append(f'    {sid}-->>{app_id}: resposta')
        resp = response or default_response(ep)
        lines.append(f'    {app_id}-->>Client: {esc_msg(resp)}')
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def default_response(ep):
    if ep["method"] == "POST":
        return "201 Created"
    if ep["method"] == "DELETE":
        return "204 No Content"
    if ep["method"] == "MSG":
        return "ack"
    return "200 OK"


def flow_endpoint_style(inv, endpoints, direction="LR"):
    lines = [f"flowchart {direction}", "    Client([Client])", ""]
    lines.append(f'    subgraph APP["{esc(inv["app_name"])}"]')
    lines.append("        direction TB")
    for i, ep in enumerate(endpoints, 1):
        eid = f"EP{i}"
        lines.append(f'        {eid}["{esc(ep["method"] + " " + ep["path"])}"]')
    lines.append("    end")
    lines.append("")

    for sysname, meta in inv["systems"].items():
        o, c = SHAPE.get(meta["kind"], ("[", "]"))
        lines.append(f'    {ident(sysname)}{o}"{esc(meta["label"])}"{c}')
    lines.append("")

    for i, ep in enumerate(endpoints, 1):
        eid = f"EP{i}"
        lines.append(f"    Client --> {eid}")
        seen = set()
        for st in ep["steps"]:
            key = (st["system"], st["operation"])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f'    {eid} -->|"{esc(st["operation"])}"| {ident(st["system"])}')
    lines.append("")
    lines.append("    classDef db fill:#e8f4ea,stroke:#4a7c59;")
    lines.append("    classDef queue fill:#fdf3e0,stroke:#b8860b;")
    lines.append("    classDef api fill:#eef2fb,stroke:#4a5fa5;")
    for kind, cls in (("database", "db"), ("cache", "db"), ("storage", "db"),
                      ("queue", "queue"), ("external_api", "api")):
        ids = [ident(s) for s, m in inv["systems"].items() if m["kind"] == kind]
        if ids:
            lines.append(f"    class {','.join(ids)} {cls};")
    return "\n".join(lines).rstrip() + "\n"


def flow_summary_style(inv, endpoints, direction="LR"):
    """Visao macro: uma caixa da API ligada a cada fronteira (estilo do exemplo 2)."""
    lines = [f"flowchart {direction}", f'    APP["{esc(inv["app_name"])}"]', ""]
    counts = {}
    for ep in endpoints:
        for st in ep["steps"]:
            counts.setdefault(st["system"], set()).add(f'{ep["method"]} {ep["path"]}')
    for sysname, eps in counts.items():
        meta = inv["systems"].get(sysname, {"label": sysname, "kind": "external_api"})
        o, c = SHAPE.get(meta["kind"], ("[", "]"))
        lines.append(f'    {ident(sysname)}{o}"{esc(meta["label"])}"{c}')
    lines.append("")
    for sysname, eps in counts.items():
        label = f"{len(eps)} endpoint" + ("s" if len(eps) > 1 else "")
        lines.append(f'    APP -->|"{esc(label)}"| {ident(sysname)}')
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inventory", help="JSON gerado por scan_endpoints.py")
    ap.add_argument("--out-dir", default=".", help="diretorio de saida")
    ap.add_argument("--prefix", default=None, help="prefixo dos arquivos")
    ap.add_argument("--flow-style", choices=["endpoint", "summary"],
                    default="endpoint")
    ap.add_argument("--direction", default="LR", choices=["LR", "TB", "RL", "BT"])
    ap.add_argument("--autonumber", action="store_true")
    ap.add_argument("--max-endpoints-per-file", type=int, default=25,
                    help="acima disso o diagrama de sequencia e dividido em partes")
    args = ap.parse_args()

    inv = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    eps = inv["endpoints"]
    if not eps:
        sys.exit("Nenhum endpoint no inventario - revise a varredura antes de gerar.")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or ident(inv["app_name"]).lower().strip("_") or "api"

    written = []
    chunk = args.max_endpoints_per_file
    if len(eps) > chunk:
        for i in range(0, len(eps), chunk):
            part = eps[i:i + chunk]
            n = i // chunk + 1
            p = out / f"{prefix}-sequence-{n}.mmd"
            p.write_text(sequence_diagram(inv, part, args.autonumber), encoding="utf-8")
            written.append(p)
    else:
        p = out / f"{prefix}-sequence.mmd"
        p.write_text(sequence_diagram(inv, eps, args.autonumber), encoding="utf-8")
        written.append(p)

    flow = (flow_summary_style if args.flow_style == "summary"
            else flow_endpoint_style)(inv, eps, args.direction)
    p = out / f"{prefix}-flow.mmd"
    p.write_text(flow, encoding="utf-8")
    written.append(p)

    for w in written:
        print(f"gerado: {w}")


if __name__ == "__main__":
    main()
