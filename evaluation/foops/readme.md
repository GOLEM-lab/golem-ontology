# FOOPS Evaluation Report for GOLEM Ontology

This document summarizes the FAIRness evaluation of the **GOLEM Ontology**  using the [FOOPS!](https://github.com/oeg-upm/fair_ontologies) framework.

- **Evaluation Score**: `0.8958` (as of latest test on 09-07-2025)

---

## Achieved

The following aspects passed all relevant FOOPS! checks:

- **F1**: Ontology URI is a persistent W3ID URI and resolves correctly (`application/rdf+xml`)
- **F2**: Minimum metadata present (title, description, license, version IRI, creator, creation date, namespace)
- **F3**: Prefix declaration exists (`golem`)
- **F4**: Prefix correctly registered and resolvable via [prefix.cc](https://prefix.cc)
- **A1**: Content negotiation functional (RDF & HTML views)
- **A1.1**: Open protocol (HTTPS)
- **I1**: RDF serialization available
- **I2**: Vocabulary reuse confirmed (DCTERMS, VANN, ODPs, DUL)
- **R1**:
  - HTML documentation available
  - Labels and descriptions for all ontology terms
- **R1.1**: License is present and resolvable
- **R1.2**: Provenance metadata (creator, date, publisher, issued) complete
- **Version IRI** present, distinct from ontology IRI, and resolvable

---

## Pending External Registry Update


 - **[LOV](https://lov.linkeddata.es/dataset/lov) registration:**  
  FOOPS! reports that the ontology is **not yet listed in a public registry (LOV)**. This will resolve once the ontology is submitted and indexed.

---

## Optional or Missing Metadata 

- `foaf:logo` or equivalent visual identity
- `dcterms:contributor`
- `dcterms:modified`, `backwardCompatibility`, `previousVersion`
- More formalized `term_status` and project lifecycle metadata (`status`, `release notes`, etc.)

---

## Summary

| Status  | Category      | Notes                                                     |
|---------|---------------|-----------------------------------------------------------|
| OK      | Findable       | URI, prefix, version, and minimum metadata compliant     |
| Partial | Findable       | Not yet listed in LOV (public registry check failing)    |
| OK      | Accessible     | Content negotiation and open protocol functional         |
| OK      | Interoperable  | Metadata and ontology vocabularies properly reused       |
| OK      | Reusable       | Labels, definitions, license, and provenance present     |
| Partial | Reusable       | Some detailed metadata fields (e.g., logo, contributor) missing |

---
