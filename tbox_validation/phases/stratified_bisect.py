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
    "http://erlangen-crm.org/240307/ecrm_240307.owl",
]

LRMOO_STAGE = REFERENCE_STACK + [
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/",
    "http://erlangen-crm.org/240307/",
    "http://iflastandards.info/ns/lrm/lrmoo/LRMoo_v1.1.1.owl",
    "https://cidoc-crm.org/extensions/lrmoo/owl/",
]

GOLEM_PATH = ONTO_DIR / "golem.ttl"


# ==================================================
# ENGINE
# ==================================================

class StratifiedEngine:

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

        # print("\nDOMAIN:", len(domain))
        # print("RANGE :", len(range_))

        return domain, range_

    # -------------------------
    def test_variant(self, triples, tag):
        variant = build_golem_variant(GOLEM_PATH, triples, tag)
        iri = f"golem:{tag}"
        IRI_REGISTRY[iri] = variant
        return self.run(LRMOO_STAGE + [iri])

    # -------------------------
    def bisect(self, name, triples):
        return bisect_group(
            name,
            triples,
            lambda s, t: self.test_variant(s, t),
        )


# ==================================================
# INTERACTIVE MODE (FIXED)
# ==================================================

def interactive(engine):
    print("\nMODE C")
    print("commands: props, test(domain), test(range), bisect(domain), sig, exit")

    domain, range_ = engine.extract_domain_range()

    # ✅ FIX: define props properly
    props = group_domain_range_by_property(GOLEM_PATH)

    while True:
        cmd = input("mode-c> ").strip()

        if cmd == "exit":
            break

        elif cmd == "props":
            print("\n=== DOMAIN/RANGE BY PROPERTY ===")
            for p, triples in props.items():
                print(len(triples), p)

        elif cmd == "sig":
            print(engine.stage_3_signature())

        elif cmd == "test(domain)":
            print("Unsat:", len(engine.test_variant(domain, "domain")))

        elif cmd == "test(range)":
            print("Unsat:", len(engine.test_variant(range_, "range")))

        elif cmd == "bisect(domain)":
            engine.bisect("domain", domain)

        elif cmd == "bisect(range)":
            engine.bisect("range", range_)

# ==================================================
# MAIN
# ==================================================

def main():
    mode = input("Select mode (A/C): ").strip().upper()
    engine = StratifiedEngine()

    if mode == "A":
        if engine.stage_1(): return
        if engine.stage_2(): return
        if engine.stage_3_signature(): return

        print("\nCLEAN STAGES 1–3")

    elif mode == "C":
        interactive(engine)


if __name__ == "__main__":
    main()