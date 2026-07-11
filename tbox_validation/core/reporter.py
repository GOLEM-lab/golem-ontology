from pathlib import Path
from rdflib import Graph
from core.prefixes import PREFIXES, with_prefixes


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
ALIGNMENTS_DIR = PROJECT_ROOT / "ontologies" / "alignments"



def persist_axiom(path: Path, turtle_snippet: str) -> bool:
    path = Path(path)  # ensure Path even if str passed
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(PREFIXES, encoding="utf-8")

    existing = Graph()
    existing.parse(str(path), format="turtle")

    candidate = Graph()
    candidate.parse(data=with_prefixes(turtle_snippet), format="turtle")

    if all(t in existing for t in candidate):
        return False

    for t in candidate:
        existing.add(t)

    existing.serialize(destination=str(path), format="turtle")
    return True



# def persist_axiom(filename: str, turtle_snippet: str) -> bool:
#     path = ALIGNMENTS_DIR / filename

#     if not path.exists():
#         path.write_text(PREFIXES, encoding="utf-8")

#     existing = Graph()
#     existing.parse(str(path), format="turtle")

#     candidate = Graph()
#     candidate.parse(data=with_prefixes(turtle_snippet), format="turtle")

#     if all(t in existing for t in candidate):
#         return False

#     for t in candidate:
#         existing.add(t)

#     existing.serialize(destination=str(path), format="turtle")
#     return True    



def failed_axiom(out_path, label, snippet, unsatisfiable=None):
    from pathlib import Path

    out_path = Path(out_path)

    if not out_path.is_absolute():
        out_path = ALIGNMENTS_DIR / out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"TEST: {label}\n\n")
        f.write(snippet.strip() + "\n\n")

        if unsatisfiable:
            f.write("UNSATISFIABLE CLASSES:\n")
            for c in unsatisfiable:
                f.write(f"  - {c}\n")
            f.write("\n")