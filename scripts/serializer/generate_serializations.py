#!/usr/bin/env python3

import sys
from pathlib import Path

import rdflib
from rdflib import Graph


def generate_serializations(ttl_path: Path) -> None:
    if not ttl_path.exists():
        raise FileNotFoundError(f"Input file not found: {ttl_path}")

    if ttl_path.suffix.lower() != ".ttl":
        raise ValueError(f"Input file must be a Turtle file: {ttl_path}")

    output_dir = ttl_path.parent
    stem = ttl_path.stem

    owl_path = output_dir / f"{stem}.owl"
    jsonld_path = output_dir / f"{stem}.jsonld"

    print(f"RDFLib version: {rdflib.__version__}")
    print()
    print(f"Release:   {stem}")
    print(f"Input:     {ttl_path}")
    print(f"RDF/XML:   {owl_path}")
    print(f"JSON-LD:   {jsonld_path}")
    print()

    # ------------------------------------------------------------------
    # Parse canonical Turtle source
    # ------------------------------------------------------------------

    source_graph = Graph()
    source_graph.parse(ttl_path, format="turtle")

    print(f"Parsed Turtle graph: {len(source_graph)} triples")

    # ------------------------------------------------------------------
    # Generate RDF/XML (.owl)
    # ------------------------------------------------------------------

    source_graph.serialize(
        destination=str(owl_path),
        format="xml",
        encoding="utf-8",
    )

    if not owl_path.exists():
        raise RuntimeError("Failed to create RDF/XML serialization")

    print(f"Generated RDF/XML: {owl_path}")

    # ------------------------------------------------------------------
    # Generate JSON-LD
    # ------------------------------------------------------------------

    source_graph.serialize(
        destination=str(jsonld_path),
        format="json-ld",
        encoding="utf-8",
        auto_compact=True,
    )

    if not jsonld_path.exists():
        raise RuntimeError("Failed to create JSON-LD serialization")

    print(f"Generated JSON-LD: {jsonld_path}")

    # ------------------------------------------------------------------
    # Validate generated serializations
    # ------------------------------------------------------------------

    owl_graph = Graph()
    owl_graph.parse(owl_path, format="xml")

    jsonld_graph = Graph()
    jsonld_graph.parse(jsonld_path, format="json-ld")

    print()
    print(f"Turtle triples:    {len(source_graph)}")
    print(f"RDF/XML triples:   {len(owl_graph)}")
    print(f"JSON-LD triples:   {len(jsonld_graph)}")

    ttl_owl_equal = source_graph.isomorphic(owl_graph)
    ttl_jsonld_equal = source_graph.isomorphic(jsonld_graph)
    owl_jsonld_equal = owl_graph.isomorphic(jsonld_graph)

    print()
    print(f"TTL == RDF/XML:        {ttl_owl_equal}")
    print(f"TTL == JSON-LD:        {ttl_jsonld_equal}")
    print(f"RDF/XML == JSON-LD:    {owl_jsonld_equal}")

    if not (
        ttl_owl_equal
        and ttl_jsonld_equal
        and owl_jsonld_equal
    ):
        raise RuntimeError(
            "Serialization validation failed: generated graphs "
            "are not mutually isomorphic."
        )

    print()
    print("✓ RDF/XML generated successfully")
    print("✓ JSON-LD generated successfully")
    print("✓ Graph isomorphism validation passed")
    print(f"✓ Triple count: {len(source_graph)}")


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "  python scripts/generate_serializations.py <ontology.ttl>"
        )
        sys.exit(1)

    ttl_path = Path(sys.argv[1])

    try:
        generate_serializations(ttl_path)
    except Exception as error:
        print(f"\nERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()