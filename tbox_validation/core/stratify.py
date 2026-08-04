from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, BNode
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
CONVERTED_DIR = BASE_DIR / "converted"


# ==================================================
# SIGNATURE EXTRACTION
# ==================================================

def build_golem_signature_only(golem_ttl_path: Path) -> Path:
    CONVERTED_DIR.mkdir(exist_ok=True)
    out_path = CONVERTED_DIR / "golem_signature_only.rdf"

    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    sig = Graph()
    for pfx, ns in src.namespaces():
        sig.bind(pfx, ns)

    KEEP_TYPES = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty}
    KEEP_EDGES = {RDFS.subClassOf, RDFS.subPropertyOf}
    KEEP_ANN = {RDFS.label, RDFS.comment}

    for s, p, o in src:
        if p == RDF.type and o in KEEP_TYPES:
            sig.add((s, p, o))
        elif p in KEEP_EDGES and not isinstance(o, BNode):
            sig.add((s, p, o))
        elif p in KEEP_ANN:
            sig.add((s, p, o))

    sig.serialize(destination=str(out_path), format="xml")
    return out_path


# ==================================================
# AXIOM GROUPS (GLOBAL)
# ==================================================

def extract_axiom_groups(golem_ttl_path: Path) -> dict:
    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    groups = {
        "equivalent": [],
        "disjoint": [],
        "restriction_subclass": [],
        "domain_range": [],
    }

    for s, p, o in src:
        if p == OWL.equivalentClass:
            groups["equivalent"].append((s, p, o))
        elif p == OWL.disjointWith:
            groups["disjoint"].append((s, p, o))
        elif p == RDFS.subClassOf and isinstance(o, BNode):
            groups["restriction_subclass"].append((s, p, o))
        elif p in (RDFS.domain, RDFS.range):
            groups["domain_range"].append((s, p, o))

    return groups


# ==================================================
# DOMAIN/RANGE GROUPING (FIXED CORE FEATURE)
# ==================================================

def group_domain_range_by_property(golem_ttl_path: Path):
    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    groups = defaultdict(list)

    for s, p, o in src:
        if p in (RDFS.domain, RDFS.range):
            groups[s].append((s, p, o))

    return dict(groups)


# ==================================================
# TARGET-CLASS GROUPING (IMPORTANT FOR YOUR CASE)
# ==================================================

def group_domain_range_by_target_class(golem_ttl_path: Path):
    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    groups = defaultdict(list)

    for s, p, o in src:
        if p in (RDFS.domain, RDFS.range):
            groups[o].append((s, p, o))

    return dict(groups)


# ==================================================
# VARIANT BUILDING
# ==================================================

def _collect_closure(src: Graph, triple, seen=None):
    if seen is None:
        seen = set()

    s, p, o = triple
    closure = {triple}

    frontier = [o] if isinstance(o, BNode) else []

    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)

        for sp, so in src.predicate_objects(node):
            closure.add((node, sp, so))
            if isinstance(so, BNode):
                frontier.append(so)

    return closure


def build_golem_variant(golem_ttl_path: Path, extra_triples: list, tag: str) -> Path:
    CONVERTED_DIR.mkdir(exist_ok=True)
    out_path = CONVERTED_DIR / f"golem_variant_{tag}.rdf"

    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    sig = Graph()
    for pfx, ns in src.namespaces():
        sig.bind(pfx, ns)

    KEEP_TYPES = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty}
    KEEP_EDGES = {RDFS.subClassOf, RDFS.subPropertyOf}
    KEEP_ANN = {RDFS.label, RDFS.comment}

    for s, p, o in src:
        if p == RDF.type and o in KEEP_TYPES:
            sig.add((s, p, o))
        elif p in KEEP_EDGES and not isinstance(o, BNode):
            sig.add((s, p, o))
        elif p in KEEP_ANN:
            sig.add((s, p, o))

    for t in extra_triples:
        for ct in _collect_closure(src, t):
            sig.add(ct)

    sig.serialize(destination=str(out_path), format="xml")
    return out_path


# ==================================================
# BISECTION
# ==================================================

def bisect_group(name: str, triples: list, test_fn, max_leaf: int = 4):
    print(f"\n--- bisecting group '{name}' ({len(triples)}) ---")

    def _bisect(subset, tag):
        if len(subset) <= max_leaf:
            print(f"[{tag}] leaf size={len(subset)}")
            for t in subset:
                print(" ", t)
            return subset

        mid = len(subset) // 2
        left, right = subset[:mid], subset[mid:]

        if test_fn(left, tag + "L"):
            return _bisect(left, tag + "L")

        if test_fn(right, tag + "R"):
            return _bisect(right, tag + "R")

        print(f"[{tag}] interaction case")
        return subset

    return _bisect(triples, "root")


# ==================================================
# SUMMARY
# ==================================================

def summarize_stripped(golem_ttl_path: Path) -> dict:
    src = Graph()
    src.parse(str(golem_ttl_path), format="turtle")

    return {
        "disjoint": len(list(src.triples((None, OWL.disjointWith, None)))),
        "equivalent": len(list(src.triples((None, OWL.equivalentClass, None)))),
        "restriction_subclass": sum(
            1 for s, p, o in src.triples((None, RDFS.subClassOf, None))
            if isinstance(o, BNode)
        ),
    }