import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.loader import build_world, inject_axiom, IRI_REGISTRY, ONTO_DIR
from core.reasoner import check_coherence
from core.stratify import (
    build_golem_signature_only,
    summarize_stripped,
    extract_axiom_groups,
    build_golem_variant,
    bisect_group,
    group_domain_range_by_property,
    group_domain_range_by_target_class,
)

from rdflib import Graph, RDFS


# ==================================================
# CONFIG
# ==================================================

BRIDGE = "crm:E28_Conceptual_Object rdfs:subClassOf dlp_extDnS:social-object ."

REFERENCE_STACK = [
    "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ModalDescriptions.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/CommonSenseMapping.owl",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl",
    "http://erlangen-crm.org/240307/",
]

LRMOO_STAGE = REFERENCE_STACK + [
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/",
    "https://cidoc-crm.org/extensions/lrmoo/owl/",
]

GOLEM_PATH = ONTO_DIR / "golem.ttl"

# Order is a default reporting convention, not an assumption about
# where the problem lives — every category is tested independently.
AXIOM_TYPOLOGY_ORDER = ["disjoint", "equivalent", "restriction_subclass", "domain_range"]


# ==================================================
# ENGINE
# ==================================================

class StratifiedEngine:

    def __init__(self):
        # Extracted once; re-extract with self.refresh_groups() if
        # golem.ttl changes mid-session.
        self.groups = extract_axiom_groups(GOLEM_PATH)

    def refresh_groups(self):
        self.groups = extract_axiom_groups(GOLEM_PATH)

    # -------------------------
    def run(self, stack):
        world = build_world(stack)
        inject_axiom(world, BRIDGE)
        return check_coherence(world)

    # -------------------------
    def stage_1(self):
        print("\n=== STAGE 1 ===")
        return self.run(REFERENCE_STACK)

    def stage_2(self):
        print("\n=== STAGE 2 ===")
        return self.run(LRMOO_STAGE)

    def stage_3_signature(self):
        print("\n=== STAGE 3 ===")

        sig_path = build_golem_signature_only(GOLEM_PATH)
        IRI_REGISTRY["golem:signature"] = sig_path

        return self.run(LRMOO_STAGE + ["golem:signature"])

    # -------------------------
    def extract_domain_range(self):
        g = Graph()
        g.parse(str(GOLEM_PATH), format="turtle")

        domain, range_ = [], []

        for s, p, o in g:
            if p == RDFS.domain:
                domain.append((s, p, o))
            elif p == RDFS.range:
                range_.append((s, p, o))

        return domain, range_

    # -------------------------
    def test_variant(self, triples, tag):
        variant = build_golem_variant(GOLEM_PATH, triples, tag)
        iri = f"golem:{tag}"
        IRI_REGISTRY[iri] = variant
        return self.run(LRMOO_STAGE + [iri])

    # -------------------------
    def test_group(self, category):
        """Test one axiom category (from self.groups) for coherence."""
        if category not in self.groups:
            raise ValueError(
                f"Unknown category '{category}'. "
                f"Available: {', '.join(self.groups.keys())}"
            )
        return self.test_variant(self.groups[category], category)

    # -------------------------
    def bisect(self, name, triples):
        return bisect_group(
            name,
            triples,
            lambda s, t: self.test_variant(s, t),
        )

    def bisect_group_by_name(self, category):
        if category not in self.groups:
            raise ValueError(
                f"Unknown category '{category}'. "
                f"Available: {', '.join(self.groups.keys())}"
            )
        return self.bisect(category, self.groups[category])

    # -------------------------
    def run_axiom_typology_checks(self, stop_on_incoherent=False):
        print("\n=== AXIOM TYPOLOGY CHECKS ===")
        results = {}

        for category in AXIOM_TYPOLOGY_ORDER:
            triples = self.groups.get(category, [])
            print(f"\n--- {category} ({len(triples)} axioms) ---")

            if not triples:
                print("  (no axioms in this group, skipping)")
                results[category] = []
                continue

            unsat = self.test_variant(triples, category)
            results[category] = unsat

            if unsat:
                print(f"  \u22a5 INCOHERENT — {len(unsat)} unsatisfiable class(es)")
                for iri in unsat:
                    print("   -", iri)
                if stop_on_incoherent:
                    break
            else:
                print("  \u22a4 COHERENT")

        print("\n=== SUMMARY ===")
        for category in AXIOM_TYPOLOGY_ORDER:
            if category not in results:
                continue
            status = "\u22a5" if results[category] else "\u22a4"
            print(f"  {category:22s} {status}")

        return results


# ==================================================
# GENERIC INTERACTIVE MODE
# ==================================================

def print_groups(engine):
    print("\n=== AXIOM CATEGORIES ===")
    for cat, triples in engine.groups.items():
        print(f"  {cat:22s} {len(triples)} axioms")
    print()


MODE_HELP_TEXT = """
Each command runs one reasoner pass over: reference stack + LRMoo/CIDOC
+ GOLEM signature-only, plus whatever that command adds on top. No
category is assumed to be the culprit — test or bisect any of them.

  groups                 List axiom categories and how many axioms each has.
  test(<category>)       Add ALL axioms of that category, run the reasoner,
                          report unsatisfiable class count.
  bisect(<category>)     Binary-search that category's axiom set to isolate
                          the smallest subset that still causes incoherence.
  sig                     Sanity check: signature only, no axioms at all.
                          Should always be coherent — if not, the problem
                          is upstream of GOLEM's own axioms.
  props                   (domain_range only) breakdown by property.
  targets                 (domain_range only) breakdown by target class.
  help                    Show this list again.
  exit                    Leave interactive mode.

Categories currently available: {categories}
"""


def print_help(engine):
    print(MODE_HELP_TEXT.format(categories=", ".join(engine.groups.keys())))


def _parse_call(cmd, name):
    """Parse 'name(arg)' -> arg, or None if cmd doesn't match name(...)."""
    prefix, suffix = f"{name}(", ")"
    if cmd.startswith(prefix) and cmd.endswith(suffix):
        return cmd[len(prefix):-len(suffix)].strip()
    return None


def interactive(engine):
    print_help(engine)

    domain, range_ = engine.extract_domain_range()
    props = group_domain_range_by_property(GOLEM_PATH)
    targets = group_domain_range_by_target_class(GOLEM_PATH)

    while True:
        cmd = input("mode-c> ").strip()

        if cmd == "exit":
            break

        elif cmd == "help":
            print_help(engine)

        elif cmd == "groups":
            print_groups(engine)

        elif cmd == "sig":
            unsat = engine.stage_3_signature()
            if unsat:
                print(f"\u22a5 INCOHERENT — {len(unsat)} unsatisfiable class(es):")
                for iri in unsat:
                    print("  -", iri)
            else:
                print("\u22a4 COHERENT — signature alone introduces no incoherence.")

        elif cmd == "props":
            print("\n=== DOMAIN/RANGE BY PROPERTY ===")
            print("(property IRI -> number of domain/range triples asserted on it)\n")
            for p, triples in props.items():
                print(len(triples), p)

        elif cmd == "targets":
            print("\n=== DOMAIN/RANGE BY TARGET CLASS ===")
            print("(target class IRI -> number of domain/range triples pointing at it)\n")
            for t, triples in targets.items():
                print(len(triples), t)

        elif (category := _parse_call(cmd, "test")) is not None:
            try:
                unsat = engine.test_group(category)
                status = "\u22a4 coherent" if not unsat else "\u22a5 incoherent"
                print(f"Unsat: {len(unsat)} ({status})")
            except ValueError as e:
                print(e)

        elif (category := _parse_call(cmd, "bisect")) is not None:
            try:
                engine.bisect_group_by_name(category)
            except ValueError as e:
                print(e)

        else:
            print(f"Unknown command '{cmd}'. Type 'help' to see available commands.")


def axiom_typology_mode(engine):
    print("\nMODE B — axiom typology checks")
    print("Runs reference stack + LRMoo/CIDOC + GOLEM signature + ALL axioms of one "
          "type, one type at a time, in this order:\n")
    for cat in AXIOM_TYPOLOGY_ORDER:
        print(f"  - {cat}")
    print()

    results = engine.run_axiom_typology_checks()

    incoherent = [cat for cat, unsat in results.items() if unsat]
    if not incoherent:
        print("\nAll axiom types coherent — nothing to bisect.")
        return

    for cat in incoherent:
        choice = input(
            f"\n'{cat}' came back incoherent. Bisect it to find the minimal "
            f"culprit subset? (y/n) "
        ).strip().lower()
        if choice == "y":
            engine.bisect_group_by_name(cat)


# ==================================================
# MAIN
# ==================================================

MODE_HELP = [
    ("A", "Sanity staging: reference stack alone, then + LRMoo/CIDOC, then + GOLEM "
          "signature-only. Confirms the base stack is coherent before any GOLEM axioms "
          "are added."),
    ("B", "Batch axiom typology check: test every category in one pass, then offer to "
          "bisect whichever ones come back incoherent."),
    ("C", "Interactive investigation: test or bisect any single axiom category on "
          "demand, in any order."),
]


def print_mode_help():
    print("\nSelect a mode:")
    for m, desc in MODE_HELP:
        print(f"  {m}) {desc}")


def main():
    print_mode_help()
    mode = input("\nMode (A/B/C): ").strip().upper()
    engine = StratifiedEngine()

    if mode == "A":
        if engine.stage_1(): return
        if engine.stage_2(): return
        if engine.stage_3_signature(): return

        print("\nCLEAN STAGES 1–3")

    elif mode == "B":
        axiom_typology_mode(engine)

    elif mode == "C":
        interactive(engine)

    else:
        print(f"Unknown mode '{mode}'.")


if __name__ == "__main__":
    main()