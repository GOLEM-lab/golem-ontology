# FOOPS Evaluation Report for GOLEM Ontology

This document summarizes the FAIRness evaluation of the **GOLEM Ontology** ([https://w3id.org/golem/ontology](https://w3id.org/golem/ontology)) using the [FOOPS](https://github.com/oeg-upm/fair_ontologies) framework.

- **Evaluation Score**: `0.8125` (as of latest test on 28-06-2025)

---

## Achieved

The following aspects passed all relevant FOOPS checks:

- **F1**: Ontology URI is a persistent W3ID URI and resolves correctly (`application/rdf+xml`)
- **F2**: Minimum metadata present (title, version, license, creator, creation date, namespace)
- **F3**: Prefix declaration exists (`golem`)
- **F4**: Prefix correctly registered and resolvable via [prefix.cc](https://prefix.cc)
- **A1**: Content negotiation functional (RDF & HTML views)
- **A1.1**: Open protocol (HTTPS)
- **I1**: RDF serialization available
- **I2**: Vocabulary reuse confirmed (DCTERMS, VANN, CIDOC-CRM, ODPs)
- **R1**: 
  - HTML documentation available
  - Labels and descriptions for all ontology terms
- **R1.1**: License is present and resolvable
- **R1.2**: Provenance metadata (creator, date, publisher, issued) complete
- **Version IRI** present and correctly distinct from ontology IRI

---

## To Be Resolved Automatically After W3ID Merge

The following errors are expected to resolve **once the W3ID pull request is merged**:

- **Version IRI resolvability** (`https://w3id.org/golem/ontology/v1.0`)  
  *This URI currently does not resolve but will once W3ID redirects are live.*

- **Ontology ID consistency**  
  FOOPS currently reports a mismatch because the ontology is accessed from a non-W3ID mirror (`https://ontology.golemlab.eu/golem.ttl`). This will self-resolve post-W3ID publication.

---

## Pending External Registry Update

- **[LOV](https://lov.linkeddata.es/dataset/lov) registration**  
  FOOPS fails the public registry check because the ontology is **not yet discoverable in LOV**. Once LOV refreshes its dataset following the W3ID and metadata updates, this should pass.

---

## Optional or Missing Metadata (Non-blocking but Recommended)

- `foaf:logo` or equivalent visual identity
- `dcterms:contributor`
- `dcterms:modified`, `backwardCompatibility`, `previousVersion`
- More formalized `term_status` handling

These elements are **not strictly required** for FAIR compliance but are recommended to improve completeness and documentation quality.

---

## Summary

| Status     | Category         | Notes                                                                 |
|------------|------------------|-----------------------------------------------------------------------|
| OK       | Findable         | URI, prefix, and minimum metadata all compliant                      |
| Pending | Findable         | W3ID merge needed to fix ID and versionIRI resolution                |
| Missing | Findable         | LOV listing incomplete                                                |
| OK       | Accessible       | Content negotiation and open protocol implemented                    |
| OK       | Interoperable    | Metadata and ontological vocabularies properly reused                |
| OK       | Reusable         | Labels, definitions, license, and provenance metadata present        |
| Partial  | Reusable         | Some detailed metadata fields (e.g., logo, contributor) are missing |

---

