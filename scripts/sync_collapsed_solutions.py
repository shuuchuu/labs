"""Keep Colab's `collapsed_sections` metadata in sync with `# Solution` headings.

Colab persists which sections are collapsed in `metadata.colab.collapsed_sections`
(a list of markdown heading cell ids). Run this after adding, removing or moving a
"Solution" heading so it stays collapsed when the notebook is opened in Colab.
"""

import json
import secrets
import string
import sys
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
ID_ALPHABET = string.ascii_letters + string.digits + "-_"


def make_cell_id() -> str:
    return "".join(secrets.choice(ID_ALPHABET) for _ in range(12))


def heading_text(cell: dict) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    source = "".join(cell.get("source", []))
    stripped = source.strip()
    if not stripped:
        return None
    first_line = stripped.splitlines()[0]
    if not first_line.lstrip().startswith("#"):
        return None
    return first_line.lstrip("#").strip()


def sync_notebook(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    indented = raw.startswith("{\n")
    nb = json.loads(raw)

    solution_ids = []
    for cell in nb["cells"]:
        if (heading_text(cell) or "").lower() != "solution":
            continue
        metadata = cell.setdefault("metadata", {})
        cell_id = metadata.get("id")
        if not cell_id:
            cell_id = make_cell_id()
            metadata["id"] = cell_id
        solution_ids.append(cell_id)

    if not solution_ids:
        return False

    all_cell_ids = {cell.get("metadata", {}).get("id") for cell in nb["cells"]}
    colab_meta = nb.setdefault("metadata", {}).setdefault("colab", {})
    existing = colab_meta.get("collapsed_sections", [])
    kept = [cell_id for cell_id in existing if cell_id in all_cell_ids]
    new_collapsed = kept + [cell_id for cell_id in solution_ids if cell_id not in kept]

    if new_collapsed == existing:
        return False

    colab_meta["collapsed_sections"] = new_collapsed

    dump = (
        json.dumps(nb, indent=1, sort_keys=True, ensure_ascii=False)
        if indented
        else json.dumps(nb, separators=(",", ":"), ensure_ascii=False)
    )
    if raw.endswith("\n"):
        dump += "\n"
    path.write_text(dump, encoding="utf-8")
    return True


def main() -> None:
    changed = [
        path
        for path in sorted(NOTEBOOKS_DIR.rglob("*.ipynb"))
        if sync_notebook(path)
    ]
    for path in changed:
        print(f"synced {path.relative_to(NOTEBOOKS_DIR.parent)}")
    print(f"{len(changed)} notebook(s) updated")


if __name__ == "__main__":
    sys.exit(main())
