# Changelog

All notable changes to the GOLEM Ontology will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - TBD

Major release. GOLEM v2.0 refactors the import architecture, the feature model and
a large part of the ontology's axioms. Vocabulary names are preserved, but the
formal semantics change, so entailments differ from v1.1 and backward compatibility
is **not** guaranteed (see *Semantic Versioning* above).

### Added

- Import of the DUL Region ontology design pattern
  (`http://www.ontologydesignpatterns.org/cp/owl/region.owl`), with the dedicated prefix `dul_region`.
- Ontology header: `owl:priorVersion` pointing to the archived v1.1 Zenodo record
  (`https://doi.org/10.5281/zenodo.14911393`), `owl:versionInfo "2.0.0"` and
  `dcterms:modified "2026-08-24"^^xsd:date`.
- `golem:GP0i_is_feature_of` is now a subproperty of `dul_region:isRegionFor`.
- Explicit disjointness for `golem:G0_Character-Stoff` with `golem:G1_Character`,
  `golem:G9_Narrative_Unit` and `lrmoo:F1_Work`, so that `golem:G0_Character-Stoff`
  cannot receive features.
- New disjointness axioms:
  `golem:G13_Narrative_Location` with `dlp_csm:non-physical-place`;
  `golem:G5_Narrative_Event` with `golem:G3_Psychological_State`;
  `golem:G9_Narrative_Unit` with `golem:G5_Narrative_Event`;
  `golem:G16_Object` with `golem:G1_Character`;
  `golem:G15_Fandom` with `golem:G14_Narrative-Stoff`.
- One `owl:AllDisjointClasses` axiom over the GOLEM subclasses of `dlp_extDnS:role`:
  `golem:G6_Relationship_Role`, `golem:G10_Narrative_Function`,
  `golem:G11_Narrative_Role` and `golem:G13_Narrative_Location`.
- Universal restriction on `golem:G4_Social_Relationship`: `dlp_extDnS:d-uses`
  `owl:allValuesFrom` `golem:G6_Relationship_Role`.
- Local alignment of the reused LRMoo constructs to Erlangen CRM, with the original
  LRMoo namespace preserved (e.g. `lrmoo:R5_has_component` as subproperty of
  `ecrm:P148_has_component`, with `lrmoo:R5i_is_component_of` as its inverse and
  subproperty of `ecrm:P148i_is_component_of`).

### Changed

- **Import architecture.** Erlangen CRM OWL (`http://erlangen-crm.org/240307/`, prefix `ecrm`)
  is now the CRM foundation, replacing the canonical CIDOC CRM OWL.
  The underlying CRM version remains CIDOC CRM 7.1.3 (official ISO version).
  Selected LRMoo constructs are redeclared locally (namespace preserved,
  subclass/subproperty relations recreated against Erlangen CRM) instead of
  importing LRMoo and CIDOC CRM.
- **Feature model.** `golem:G2_Feature` is now a subclass of `dul_region:Region`
  (was `dul:Region`) and `golem:GP0_has_feature` a subproperty of
  `dul_region:hasRegion` (was `dul:hasRegion`).
- **`golem:GP0_has_feature` domain** narrowed from `ecrm:E70_Thing` to the union of
  `ecrm:E89_Propositional_Object` and `golem:G1_Character`. The range stays
  `golem:G2_Feature`. The domain restriction is paired with the disjointness
  axioms listed above.
- **`golem:GP0i_is_feature_of` range** narrowed from `ecrm:E70_Thing` to
  `ecrm:E28_Conceptual_Object`.
- **`golem:G1_Character` restrictions.** Existential restrictions
  (`owl:someValuesFrom`) on `dol:participant-in`, `dlp_extDnS:involved-in`,
  `dlp_extDnS:plays` (both `golem:G11_Narrative_Role` and `golem:G6_Relationship_Role`)
  and `dlp_extDnS:uses` were removed, so a character is no longer required to
  participate in events, relationships, roles or object use.
  The restriction on `dlp_extDnS:setting` changed from existential to universal
  (`owl:allValuesFrom golem:G12_Setting`).
- **`golem:G7_Narrative_Sequence`** is now a subclass of `dlp_extDnS:course`
  (was `dlp_extDnS:concept`).
- **`golem:G16_Object` scope note** reworded: an object is a persistent item with
  narrative significance that, although it may also play narrative roles, is
  distinct from a character. Objects are not forced to play a narrative role.
- **Disjointness axioms restructured** following an OntoClean-based audit
  (Guarino & Welty, 2001). `owl:disjointWith` triples went from 122 to 12, plus
  the new `owl:AllDisjointClasses` axiom. Redundant axioms, i.e. those already
  entailed by other declared pairs and subsumptions, were removed. Disjointness
  with the GOLEM subclasses of `dlp_extDnS:course` and `dlp_extDnS:situation` now sits
  on `golem:G7_Narrative_Sequence` and `golem:G12_Setting`, and the axioms
  previously asserted on imported DLP classes no longer strengthen the upper ontology.
- **Redeclarations of imported entities slimmed down.** v1.1 restated domains,
  ranges, inverses and labels of CIDOC CRM and DOLCE-Lite-Plus terms; v2.0
  keeps only the GOLEM-specific annotations (scope notes and examples) for the
  terms it actually uses.
- **Ontology header.** `owl:versionIRI` now `<https://w3id.org/golem/ontology/v2.0>`;
  `dcterms:hasVersion` `"1.1.0"` → `"2.0.0"`; `dcterms:identifier` Zenodo record
  `14911396` → `14911392`; `dc:license` now points to the CC BY 4.0 legal code;
  `rdfs:comment` rewritten to describe v2.0 major changes.

### Removed

- `owl:imports` of `DUL.owl` and of the LRMoo OWL serialization
  (`https://cidoc-crm.org/extensions/lrmoo/owl/`).
  This also removes CIDOC CRM OWL from the import closure.
- `dol:generically-dependent-on` and its inverse `dol:generic-dependent`, together
  with the restriction on `golem:G4_Social_Relationship` that used them
  (`owl:someValuesFrom golem:G5_Narrative_Event`). The dependency is left to
  provenance mechanisms.
- Redundant `owl:disjointWith` axioms and the disjointness axioms asserted on
  imported DLP classes (see *Changed*).
- Local redeclarations of imported Erlangen CRM and DOLCE-Lite-Plus entities that
  GOLEM no longer needs to restate, e.g. `ecrm:E1_CRM_Entity`, `ecrm:E70_Thing`,
  `dol:endurant`, `dol:perdurant`.
- `dcterms:source` from the ontology header.

### Fixed

- `golem:G0_Character-Stoff` (a subclass of `ecrm:E28_Conceptual_Object`, sibling of
  `golem:G1_Character`) is no longer admitted as the subject of `golem:GP0_has_feature`:
  it is outside the narrowed domain, and its disjointness with `golem:G1_Character`,
  `lrmoo:F1_Work` and `golem:G9_Narrative_Unit` prevents it from being inferred into it.

## [1.1.0] - 2024-10-10 [LEGACY]

Baseline for this changelog. v1.1 is superseded by 2.0.0 and is not recommended for
new work, because of the structural modeling issues addressed in 2.0.0. It is not part
of the formal version history, and its IRI is no longer served through w3id content
negotiation. The archived Turtle file, documentation and Zenodo record remain available:
[Turtle](https://ontology.golemlab.eu/releases/v1-1/golem_v1-1.ttl),
[documentation](https://ontology.golemlab.eu/releases/v1-1/golem_v1-1.html),
[Zenodo](https://doi.org/10.5281/zenodo.14911393).

[Unreleased]: https://w3id.org/golem/ontology/v2.0
[2.0.0]: https://w3id.org/golem/ontology/v2.0
[1.1.0]: https://doi.org/10.5281/zenodo.14911393