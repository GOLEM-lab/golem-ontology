
## DOLCE

- [x] Normalize DOLCE-based URIs from `loa-cnr.it/ontologies` to `ontologydesignpatterns.org` because it is the current canonical location for these ontologies (official registries like BARTOC and LOV use it as the homepage/current URI). The CNR domain belongs to the old WonderWeb project (2002–2004),  while the ODP portal was created under the follow-up NeOn project (2006–2010) as the new canonical location.

## Namespace use for indirect DLP Design Pattern import

- [x] Create prefix for "http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl#" --> "dlp_spat"
- [x] Create prefix for "http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl#" --> "dlp_temp"
- [x] Create prefix for "http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl" --> "dlp_funct"
- [x] Create prefix for "http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl" --> "dlp_extDnS"
- [x] Create prefix for "http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl" --> "dol"


## CIDOC & LRMoo

- [x] **Verify Erlangen-CRM URI** – confirm `http://erlangen-crm.org/240307/` is the correct and dereferenceable IRI for the intended version; check whether a stable OWL file is actually served at that address
- [x] Same for **LRMoo**
## CURIES 

- [x] **Add `@prefix dul:` declaration** – add `@prefix dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#> .` and normalize all DUL references throughout the file to use it consistently (currently `GP0_has_feature`, `G2_Feature`)

## Blank node 

- [x] **Remove floating blank node** – delete or reattach the detached `[ rdfs:comment "G17 Narrative Physical Place"@en ] .` near the bottom of the file; if a `G17_Narrative_Physical_Place` class is planned, stub it out properly

## Redundancy 

- [x] **Remove redundant `rdfs:subPropertyOf owl:topObjectProperty`** on `crm:P67_refers_to` (and `crm:P67i_is_referred_to_by`) – subclassing into the universal top property is semantically vacuous; remove unless a specific tool requires it


