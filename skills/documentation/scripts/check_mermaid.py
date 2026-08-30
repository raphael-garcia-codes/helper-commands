#!/usr/bin/env python3
"""
check_mermaid.py - Conferencia rapida dos .mmd gerados, sem dependencias.

Nao substitui o parser oficial do Mermaid, mas pega os erros que de fato
acontecem: participante usado sem declarar, aspas desbalanceadas, caractere
reservado solto no rotulo e no de fluxo sem declaracao.

Uso:
    python check_mermaid.py diagrams/*.mmd
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MSG = re.compile(r"^\s*(\w+)\s*(-?->>?|--?>>?|-x|--x)\s*(\w+)\s*:")
PARTICIPANT = re.compile(r"^\s*(participant|actor)\s+(\w+)")
NODE_DECL = re.compile(r"^\s*(\w+)\s*[\[\(\{]")
EDGE = re.compile(r"^\s*(\w+)\s*[-.=]{1,3}[->ox]{1,2}\s*(?:\|[^|]*\|)?\s*(\w+)")


def check(path: Path):
    problems = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return ["arquivo vazio"]
    header = lines[0].strip()
    kind = ("sequence" if header.startswith("sequenceDiagram")
            else "flow" if header.startswith(("flowchart", "graph")) else None)
    if kind is None:
        problems.append(f"linha 1 deveria abrir com sequenceDiagram ou flowchart: {header!r}")

    declared = set()
    for i, line in enumerate(lines, 1):
        if line.count('"') % 2:
            problems.append(f"linha {i}: numero impar de aspas -> {line.strip()[:70]}")
        m = PARTICIPANT.match(line)
        if m:
            declared.add(m.group(2))
            continue
        m = NODE_DECL.match(line)
        if m and kind == "flow":
            declared.add(m.group(1))

    if kind == "sequence":
        declared |= {"Client"}
        for i, line in enumerate(lines, 1):
            m = MSG.match(line)
            if not m:
                continue
            for who in (m.group(1), m.group(3)):
                if who not in declared:
                    problems.append(f"linha {i}: participante '{who}' usado sem declarar")
    elif kind == "flow":
        for i, line in enumerate(lines, 1):
            if line.strip().startswith(("subgraph", "end", "classDef", "class ",
                                        "flowchart", "graph", "%%", "direction")):
                continue
            m = EDGE.match(line)
            if m:
                for who in (m.group(1), m.group(2)):
                    if who not in declared and not who.startswith("EP"):
                        problems.append(f"linha {i}: no '{who}' usado sem declarar")

    for i, line in enumerate(lines, 1):
        if line.strip().startswith(("classDef", "class ", "style", "%%", "linkStyle")):
            continue
        body = re.sub(r'"[^"]*"', "", line)
        if "#" in body or ";" in body:
            problems.append(f"linha {i}: caractere reservado fora de aspas -> {line.strip()[:70]}")
        if kind == "flow":
            m = re.match(r"^\s*\S+\s*[-.=]{1,3}[->ox]{1,2}\|([^|]*)\|", line)
            if m:
                label = m.group(1)
                quoted = label.startswith('"') and label.endswith('"')
                if not quoted and re.search(r"[{}()\[\]]", label):
                    problems.append(f"linha {i}: rotulo de aresta com {{}}/()/[] fora de aspas -> {line.strip()[:70]}")
    return problems


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    failed = 0
    for a in args:
        p = Path(a)
        probs = check(p)
        if probs:
            failed += 1
            print(f"[FALHA] {p}")
            for x in probs[:15]:
                print(f"   - {x}")
        else:
            print(f"[ok] {p}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
