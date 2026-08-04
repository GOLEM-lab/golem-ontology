from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS, OWL


GOLEM_FILE = (
    Path(__file__).parent.parent
    / "ontologies"
    / "golem.ttl"
)


ALIGNMENT_PREDICATES = {
    RDFS.subClassOf,
    RDFS.subPropertyOf,
    OWL.equivalentClass,
    OWL.equivalentProperty,
}


NAMESPACES = {
    "crm": "http://erlangen-crm.org/240307/",
    "dul": "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
    "dlp_extDnS": "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl#",
}


def generate_candidates(source_prefix: str, target_prefix: str):

    g = Graph()
    g.parse(GOLEM_FILE, format="turtle")

    # IMPORTANT: bind prefixes for clean n3()
    for prefix, ns in NAMESPACES.items():
        g.bind(prefix, ns)

    src_ns = NAMESPACES[source_prefix]
    tgt_ns = NAMESPACES[target_prefix]

    seen = set()
    candidates = []

    for s, p, o in g:

        if p not in ALIGNMENT_PREDICATES:
            continue

        if not isinstance(s, URIRef) or not isinstance(o, URIRef):
            continue

        s_str, o_str = str(s), str(o)

        if not s_str.startswith(src_ns):
            continue
        if not o_str.startswith(tgt_ns):
            continue

        key = (s_str, str(p), o_str)
        if key in seen:
            continue
        seen.add(key)

        label = f"{s.split('/')[-1]} {p.split('/')[-1]} {o.split('/')[-1]}"

        snippet = f"{s.n3(g.namespace_manager)} {p.n3(g.namespace_manager)} {o.n3(g.namespace_manager)} ."

        candidates.append((label, snippet))

    return sorted(candidates, key=lambda x: x[0])



# --------------------------------------------------
# 
# --------------------------------------------------
if __name__ == "__main__":
    result = generate_candidates("crm", "dlp_extDnS")
    for r in result:
        print(r)    