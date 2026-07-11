from pathlib import Path
import owlready2
from rdflib import Graph
from core.prefixes import with_prefixes

BASE_DIR = Path(__file__).parent.parent
ONTO_DIR = BASE_DIR / "ontologies"
CONVERTED_DIR = BASE_DIR / "converted"

# owlready2 auto-resolves any owl:imports it encounters INSIDE a loaded
# file (e.g. ExtendedDnS.owl's internal import of DOLCE-Lite.owl) by
# fetching it live, bypassing IRI_REGISTRY entirely since that registry
# is only consulted for the top-level IRIs passed into build_world().
# Registering this directory lets owlready2's own filename-matching
# fallback find local copies instead of hitting the network — important
# now that some of these hosts (e.g. ontologydesignpatterns.org) return
# 403 to non-browser requests.
owlready2.onto_path.append(str(ONTO_DIR))

IRI_REGISTRY = {
    "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl":
        ONTO_DIR / "DOLCE-Lite.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl":
        ONTO_DIR / "TemporalRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl":
        ONTO_DIR / "SpatialRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl":
        ONTO_DIR / "FunctionalParticipation.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl":
        ONTO_DIR / "ExtendedDnS.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ModalDescriptions.owl":
        ONTO_DIR / "ModalDescriptions.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/CommonSenseMapping.owl":
        ONTO_DIR / "CommonSenseMapping.owl",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl":
        ONTO_DIR / "DUL.owl",
    "http://erlangen-crm.org/240307/ecrm_240307.owl":
        ONTO_DIR / "ecrm_240307.owl",
    "http://www.cidoc-crm.org/cidoc-crm/CIDOC_CRM_v7.1.3.owl":
        ONTO_DIR / "CIDOC_CRM_v7.1.3.owl",
    "http://iflastandards.info/ns/lrm/lrmoo/LRMoo_v1.1.1.owl":
        ONTO_DIR / "LRMoo_v1.1.1.owl",
    "https://w3id.org/golem/ontology/golem.ttl":
        ONTO_DIR / "golem.ttl",
    # LRMoo_v1.1.1.owl carries an internal owl:imports pointing at this
    # exact versionIRI (not the CIDOC_CRM_v7.1.3.owl key above, and not
    # the base ontology IRI). Without registering it verbatim, owlready2
    # tries to fetch it live during LRMoo's own import resolution and
    # gets a 403 from cidoc-crm.org.
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/":
        ONTO_DIR / "CIDOC_CRM_v7.1.3.owl",
    # golem.ttl's own owl:imports uses these two bare/no-filename IRIs
    # for CRM and LRMoo (rather than the .../ecrm_240307.owl or
    # LRMoo_v1.1.1.owl keys above), so they need separate registrations
    # pointing at the same local files, loaded before golem.ttl.
    "http://erlangen-crm.org/240307/":
        ONTO_DIR / "ecrm_240307.owl",
    "https://cidoc-crm.org/extensions/lrmoo/owl/":
        ONTO_DIR / "LRMoo_v1.1.1.owl",
}

# Full dependency-ordered list — used as default and for reference
FULL_LOAD_ORDER = [
    "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/ModalDescriptions.owl",
    "http://www.ontologydesignpatterns.org/ont/dlp/CommonSenseMapping.owl",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl",
    "http://www.cidoc-crm.org/cidoc-crm/CIDOC_CRM_v7.1.3.owl",
    "http://www.cidoc-crm.org/cidoc-crm/owl/7.1.3/",
    "http://erlangen-crm.org/240307/ecrm_240307.owl",
    "http://erlangen-crm.org/240307/",
    "http://iflastandards.info/ns/lrm/lrmoo/LRMoo_v1.1.1.owl",
    "https://cidoc-crm.org/extensions/lrmoo/owl/",
    "https://w3id.org/golem/ontology/golem.ttl",
]

def _detect_format(path: Path) -> str | None:
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(b"@") or line.startswith(b"#"):
                return "turtle"
            if line.startswith(b"<"):
                return None
            break
    return None

# def _convert_to_rdfxml(ttl_path: Path) -> Path:
#     """Convert Turtle to RDF/XML via rdflib. Cached in converted/."""
#     CONVERTED_DIR.mkdir(exist_ok=True)
#     out_path = CONVERTED_DIR / (ttl_path.stem + ".rdf")
#     if not out_path.exists():
#         g = Graph()
#         g.parse(str(ttl_path), format="turtle")
#         g.serialize(destination=str(out_path), format="xml")
#     return out_path

def _convert_to_rdfxml(ttl_path: Path) -> Path:
    CONVERTED_DIR.mkdir(exist_ok=True)

    out_path = CONVERTED_DIR / f"{ttl_path.stem}.rdf"

    force_rebuild = ttl_path.name == "golem.ttl"

    needs_rebuild = (
        force_rebuild
        or not out_path.exists()
        or ttl_path.stat().st_mtime > out_path.stat().st_mtime
    )

    if needs_rebuild:
        print(f"[convert] {ttl_path.name}")

        g = Graph()
        g.parse(str(ttl_path), format="turtle")
        g.serialize(destination=str(out_path), format="xml")

    return out_path

def build_world(ontology_iris: list[str]) -> owlready2.World:
    """
    Load exactly the ontologies in ontology_iris, in the dependency
    order defined by FULL_LOAD_ORDER (preserving correct sequencing
    even if the caller supplies an unordered list). Turtle files are
    converted to RDF/XML via rdflib before loading.
    """
    world = owlready2.World()

    # Preserve dependency order: load only IRIs requested,
    # but in the order they appear in FULL_LOAD_ORDER
    ordered = [iri for iri in FULL_LOAD_ORDER if iri in ontology_iris]
    # Append any requested IRIs not in FULL_LOAD_ORDER at the end
    ordered += [iri for iri in ontology_iris if iri not in FULL_LOAD_ORDER]

    for iri in ordered:
        if iri not in IRI_REGISTRY:
            raise ValueError(f"Unknown IRI: {iri}. Add it to IRI_REGISTRY first.")
        local_path = IRI_REGISTRY[iri]
        fmt = _detect_format(local_path)
        if fmt == "turtle":
            local_path = _convert_to_rdfxml(local_path)
            fmt = None
        kwargs = {"format": fmt} if fmt else {}
        world.get_ontology(iri).load(fileobj=open(local_path, "rb"), **kwargs)

    return world

def inject_axiom(world: owlready2.World, turtle_snippet: str) -> owlready2.Ontology:
    """
    Inject a Turtle snippet into the world as a temporary ontology.
    Converted to RDF/XML via rdflib before loading.
    """
    import tempfile, os

    ttl = with_prefixes(turtle_snippet)

    with tempfile.NamedTemporaryFile(
        suffix=".ttl", delete=False, mode="w", encoding="utf-8"
    ) as f:
        f.write(ttl)
        ttl_path = f.name

    with tempfile.NamedTemporaryFile(
        suffix=".rdf", delete=False, mode="wb"
    ) as f:
        rdf_path = f.name

    try:
        g = Graph()
        g.parse(ttl_path, format="turtle")
        g.serialize(destination=rdf_path, format="xml")

        onto = world.get_ontology("file://" + rdf_path).load(
            fileobj=open(rdf_path, "rb")
        )
    finally:
        if os.path.exists(ttl_path):
            os.unlink(ttl_path)
        if os.path.exists(rdf_path):
            os.unlink(rdf_path)

    return onto