# GOLEM Serialization Build

This directory contains the scripts used to generate and validate the RDF serializations of the ontology, using .ttl file as source of truth.

## Requirements

* Python 3
* Bash

The build script automatically creates a temporary Python virtual environment and installs the latest available version of [RDFLib](https://rdflib.readthedocs.io/).

The virtual environment is removed automatically after the build.

## Usage

From the repository root, run:

```bash
./scripts/serializer/build.sh <ontology.ttl>
```

The script automatically resolves the release directory from the Turtle filename according to the GOLEM release naming convention.

For example:

```bash
./scripts/serializer/build.sh golem_v2-0.ttl
```

This resolves the source file to:

`releases/v2-0/golem_v2-0.ttl`

## What the script does

The build process:

1. Creates a temporary `.venv` environment.
2. Installs the latest version of RDFLib.
3. Parses the canonical Turtle ontology.
4. Generates an RDF/XML serialization (`.owl`).
5. Generates a JSON-LD serialization (`.jsonld`).
6. Parses the generated serializations.
7. Compares the Turtle, RDF/XML, and JSON-LD graphs.
8. Verifies that all three graphs are isomorphic.
9. Removes the temporary virtual environment.

The Turtle file is therefore treated as the **canonical source**, while RDF/XML and JSON-LD are generated artifacts.

## Expected output

For:

```text
golem_v2-0.ttl
```

the script generates:

```text
releases/v2-0/
├── golem_v2-0.ttl
├── golem_v2-0.owl
└── golem_v2-0.jsonld
```

The build fails if the generated RDF/XML or JSON-LD cannot be parsed or if either serialization is not graph-isomorphic to the canonical Turtle source.

## After a successful build

Do not manually edit the generated `.owl` or `.jsonld` files. If the Turtle source changes, regenerate the serializations using the build script.
