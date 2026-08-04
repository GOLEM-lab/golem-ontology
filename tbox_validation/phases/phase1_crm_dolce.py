import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

from core.runner import run_phase



PHASE = "phase1"

BASE_DIR = Path(__file__).parent.parent
ALIGNMENTS_DIR = BASE_DIR / "ontologies" / "alignments" / PHASE

ALIGNMENT_FILE = ALIGNMENTS_DIR / "phase1_crm_dolce.ttl"
FAILED_FILE = ALIGNMENTS_DIR / "failed_axioms.txt"

PHASE1_STACK = [
    "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl",
    "http://erlangen-crm.org/240307/ecrm_240307.owl",
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/",
    "http://iflastandards.info/ns/lrm/lrmoo/LRMoo_v1.1.1.owl",
]

CANDIDATES = [
    (
        "E28_Conceptual_Object rdf-schema#subClassOf ExtendedDnS.owl#SocialObject",
        "crm:E28_Conceptual_Object rdfs:subClassOf dlp_extDnS:social-object ."
    ),
]



def main():
    run_phase(
        phase_name="phase1",
        base_state=BASE_DIR / "ontologies/state/O0_base.owl",
        output_state=BASE_DIR / "ontologies/state/O1_phase1.owl",
        stack=PHASE1_STACK,
        candidates=CANDIDATES,
        alignment_file=ALIGNMENT_FILE,
        failed_file=FAILED_FILE,
    )

if __name__ == "__main__":
    main()