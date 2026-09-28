#!/usr/bin/env python3
"""Regenerate the endpoint tables in API_REFERENCE.md from spec/openapi.json.

Everything above the "## 2. Endpoint Index" heading (intro + auth section)
is preserved; the index and per-group tables are rebuilt from the spec.

    curl -s http://$FCM_HOST/apis/docs-json -o spec/openapi.json
    python3 scripts/gen_doc.py
"""
import json
import pathlib
from collections import OrderedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.json"
DOC = ROOT / "API_REFERENCE.md"
MARKER = "## 2. Endpoint Index"

spec = json.loads(SPEC.read_text())
schemas = spec.get("components", {}).get("schemas", {})


def ref_name(s):
    return s.get("$ref", "").split("/")[-1] if isinstance(s, dict) else ""


def body_fields(schema):
    if not schema:
        return ""
    arr = schema.get("type") == "array"
    if arr:
        schema = schema.get("items", {})
    name = ref_name(schema)
    s = schemas.get(name, schema)
    req = set(s.get("required", []))
    parts = []
    for k, v in s.get("properties", {}).items():
        t = v.get("type") or ref_name(v) or ("array" if "items" in v else "object")
        if t == "array":
            it = v.get("items", {})
            t = f"{it.get('type') or ref_name(it) or 'object'}[]"
        if "enum" in v:
            t += " (" + "|".join(map(str, v["enum"][:6])) + ("…" if len(v["enum"]) > 6 else "") + ")"
        parts.append(f"`{k}`{'*' if k in req else ''}: {t}")
    label = f"[{name or 'object'}]" if arr else (name or "object")
    return f"**{label}** — " + ", ".join(parts) if parts else f"**{label}**"


groups = OrderedDict()
total = 0
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        if method in ("get", "post", "put", "patch", "delete"):
            total += 1
            groups.setdefault((op.get("tags") or ["other"])[0], []).append((method.upper(), path, op))

out = [MARKER, "", "| Group | # |", "|---|---|"]
for tag, items in groups.items():
    out.append(f"| [{tag}](#{tag.lower().replace(' ', '-')}) | {len(items)} |")
out += ["", "## 3. Endpoints by Group", ""]
for tag, items in groups.items():
    out += [f"### {tag}", "", "| Method | Path | Description | Query / Body |", "|---|---|---|---|"]
    for method, path, op in items:
        desc = (op.get("summary") or op.get("description") or op.get("operationId", "")).replace("|", "\\|").strip()
        extra = []
        q = [p for p in op.get("parameters", []) if p.get("in") == "query"]
        if q:
            extra.append("?" + ", ".join(f"`{p['name']}`{'*' if p.get('required') else ''}" for p in q))
        rb = op.get("requestBody", {}).get("content", {})
        if rb:
            ct, c = next(iter(rb.items()))
            bf = body_fields(c.get("schema", {}))
            extra.append(bf if ct == "application/json" else f"({ct}) {bf}")
        cell = "<br>".join(extra).replace("|", "\\|") or "—"
        out.append(f"| `{method}` | `{path.replace('/apis/v1', '')}` | {desc} | {cell} |")
    out.append("")

head = DOC.read_text().split(MARKER)[0] if DOC.exists() else "# FCM API Reference\n\n"
DOC.write_text(head + "\n".join(out))
print(f"Wrote {DOC.name}: {total} endpoints in {len(groups)} groups")
