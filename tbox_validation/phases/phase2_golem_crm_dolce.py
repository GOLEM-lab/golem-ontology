import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.loader import build_world, inject_axiom
from core.reasoner import check_coherence
from core.reporter import failed_axiom
from core.state import save_world


PHASE = "phase2"

BASE_DIR = Path(__file__).parent.parent
ALIGNMENTS_DIR = BASE_DIR / "ontologies" / "alignments" / PHASE
FAILED_FILE = ALIGNMENTS_DIR / "failed_axioms.txt"
OUTPUT_STATE = BASE_DIR / "ontologies/state/O2_phase2.owl"


PHASE2_STACK = [
    "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ModalDescriptions.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/CommonSenseMapping.owl",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl",
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/",
    "http://erlangen-crm.org/240307/",
    "https://cidoc-crm.org/extensions/lrmoo/owl/",
    "https://w3id.org/golem/ontology/golem.ttl",
]

# phase1's accepted bridge axiom, replayed directly rather than loading
# O1_phase1.owl as base_state — base_state loading bypasses `stack`
# entirely in run_phase, which would silently drop golem.ttl and LRMoo
# from the world. Re-injecting the one phase1 axiom here keeps this
# script self-contained and correct.
PHASE1_BRIDGE = "crm:E28_Conceptual_Object rdfs:subClassOf dlp_extDnS:social-object ."


def main():
    print(f"\n=== {PHASE} ===")

    world = build_world(PHASE2_STACK)
    inject_axiom(world, PHASE1_BRIDGE)

    unsatisfiable = check_coherence(world)

    if not unsatisfiable:
        print("  ✔ COHERENT: full stack (DUL + DLP + CRM + LRMoo + golem.ttl) "
              "with phase1 bridge axiom")
        save_world(world, OUTPUT_STATE, stack_iris=PHASE2_STACK)
        print(f"\nSaved state → {OUTPUT_STATE}")
    else:
        print(f"  ✘ INCOHERENT: {len(unsatisfiable)} unsatisfiable class(es)")
        failed_axiom(
            FAILED_FILE,
            label="phase2 full-stack coherence check",
            snippet=PHASE1_BRIDGE,
            unsatisfiable=unsatisfiable,
        )
        print(f"Details written to {FAILED_FILE}")
        print("No output state saved — resolve the conflict before proceeding.")


if __name__ == "__main__":
    main()