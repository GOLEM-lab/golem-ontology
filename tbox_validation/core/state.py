from pathlib import Path
import owlready2
from rdflib import Graph, URIRef, RDF, OWL, RDFS



STATE_DIR = Path(__file__).parent.parent / "ontologies" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_world(path: Path):
    world = owlready2.World()
    world.get_ontology(f"file://{path.resolve()}").load()
    return world


def _fix_property_hierarchy(g: Graph) -> Graph:
    """
    owlready2 serializes property subPropertyOf as rdf:type triples.
    Detect and convert them back to rdfs:subPropertyOf.
    """
    all_properties = set()
    for s in g.subjects(RDF.type, OWL.ObjectProperty):
        all_properties.add(s)
    for s in g.subjects(RDF.type, OWL.DatatypeProperty):
        all_properties.add(s)

    to_add = []
    to_remove = []

    for prop in all_properties:
        for _, _, o in g.triples((prop, RDF.type, None)):
            # if the object is itself a known property, it's a subPropertyOf
            if o in all_properties and o != OWL.ObjectProperty and o != OWL.DatatypeProperty:
                to_remove.append((prop, RDF.type, o))
                to_add.append((prop, RDFS.subPropertyOf, o))

    for triple in to_remove:
        g.remove(triple)
    for triple in to_add:
        g.add(triple)

    return g    


def _fix_class_hierarchy(g: Graph) -> Graph:
    """
    owlready2 also serializes class subClassOf as rdf:type triples.
    Detect and convert them back to rdfs:subClassOf.
    """
    all_classes = set(g.subjects(RDF.type, OWL.Class))

    to_add = []
    to_remove = []

    for cls in all_classes:
        for _, _, o in g.triples((cls, RDF.type, None)):
            if (o in all_classes
                and o != OWL.Class
                and o != OWL.Thing
                and str(o) != "http://www.w3.org/2002/07/owl#Class"):
                to_remove.append((cls, RDF.type, o))
                to_add.append((cls, RDFS.subClassOf, o))

    for triple in to_remove:
        g.remove(triple)
    for triple in to_add:
        g.add(triple)

    return g    


# def save_world(world, path: Path):
#     path.parent.mkdir(parents=True, exist_ok=True)
#     world.save(file=str(path))    


# def save_world(world: owlready2.World, path: Path) -> None:
#     path.parent.mkdir(parents=True, exist_ok=True)
#     world.save(file=str(path))
    
#     # Strip temp/internal ontology declarations from output
#     from rdflib import Graph, URIRef, RDF, OWL
#     g = Graph()
#     g.parse(str(path), format="xml")
    
#     SKIP_PREFIXES = ("file:///tmp", "file:////tmp")
#     SKIP_EXACT = {
#         URIRef("http://inferrences/"),
#         URIRef("http://anonymous/"),
#     }
    
#     to_remove = []
#     for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
#         iri = str(s)
#         if any(iri.startswith(p) for p in SKIP_PREFIXES) or s in SKIP_EXACT:
#             to_remove.append(s)
    
#     for subject in to_remove:
#         for triple in list(g.triples((subject, None, None))):
#             g.remove(triple)
    
#     g.serialize(destination=str(path), format="xml")



# def save_world(world: owlready2.World, path: Path, stack_iris: list[str] = None) -> None:
#     path.parent.mkdir(parents=True, exist_ok=True)
#     world.save(file=str(path))

#     # Post-process: strip noise and inject proper owl:imports
#     from rdflib import Graph, URIRef, RDF, OWL, Literal
#     from rdflib.namespace import RDFS

#     g = Graph()
#     g.parse(str(path), format="xml")

#     # Strip temp/internal ontology declarations
#     SKIP_PREFIXES = ("file:///tmp", "file:////tmp")
#     SKIP_EXACT = {URIRef("http://inferrences/"), URIRef("http://anonymous/")}

#     to_remove = []
#     for s in g.subjects(RDF.type, OWL.Ontology):
#         iri = str(s)
#         if any(iri.startswith(p) for p in SKIP_PREFIXES) or s in SKIP_EXACT:
#             to_remove.append(s)

#     for subject in to_remove:
#         for triple in list(g.triples((subject, None, None))):
#             g.remove(triple)

#     # Add a root ontology node with owl:imports for each stack IRI
#     if stack_iris:
#         root = URIRef(str(path.resolve().as_uri()))
#         g.add((root, RDF.type, OWL.Ontology))
#         for iri in stack_iris:
#             g.add((root, OWL.imports, URIRef(iri)))

#     g.serialize(destination=str(path), format="xml")




# def save_world(world: owlready2.World, path: Path, stack_iris: list[str] = None) -> None:
#     path.parent.mkdir(parents=True, exist_ok=True)
#     world.save(file=str(path))

#     from rdflib import Graph, URIRef, RDF, OWL, RDFS

#     g = Graph()
#     g.parse(str(path), format="xml")

#     # Strip temp/internal ontology declarations
#     SKIP_PREFIXES = ("file:///tmp", "file:////tmp")
#     SKIP_EXACT = {
#     URIRef("http://inferrences/"),
#     URIRef("http://anonymous/"),
#     URIRef("http://inferrences"),   
#     URIRef("http://anonymous"),     
#     }

#     to_remove = []
#     for s in g.subjects(RDF.type, OWL.Ontology):
#         iri = str(s)
#         if any(iri.startswith(p) for p in SKIP_PREFIXES) or s in SKIP_EXACT:
#             to_remove.append(s)
#     for subject in to_remove:
#         for triple in list(g.triples((subject, None, None))):
#             g.remove(triple)

#     # Fix property and class hierarchies serialization
#     g = _fix_property_hierarchy(g)
#     g = _fix_class_hierarchy(g)

#     # Add root ontology with imports
#     if stack_iris:
#         root = URIRef(path.resolve().as_uri())
#         g.add((root, RDF.type, OWL.Ontology))
#         for iri in stack_iris:
#             g.add((root, OWL.imports, URIRef(iri)))

#     g.serialize(destination=str(path), format="xml")





def save_world(world: owlready2.World, path: Path, stack_iris: list[str] = None, state_iri: str = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    world.save(file=str(path))

    g = Graph()
    g.parse(str(path), format="xml")

    # Strip ALL existing owl:Ontology declarations
    to_remove = []
    for s in g.subjects(RDF.type, OWL.Ontology):
        to_remove.append(s)
    for subject in to_remove:
        for triple in list(g.triples((subject, None, None))):
            g.remove(triple)

    # Fix hierarchies
    g = _fix_property_hierarchy(g)
    g = _fix_class_hierarchy(g)

    # Add a single root ontology with a clean, unambiguous IRI
    root_iri = state_iri or f"https://w3id.org/golem/validation/state/{path.stem}"
    root = URIRef(root_iri)
    g.add((root, RDF.type, OWL.Ontology))
    if stack_iris:
        for iri in stack_iris:
            g.add((root, OWL.imports, URIRef(iri)))

    g.serialize(destination=str(path), format="xml")

