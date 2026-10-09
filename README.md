![DOI](https://zenodo.org/badge/631064567.svg)

Cite as:

Pianzola, F., Pannach, F., Cheng, L., Yang, X, and Scotti, L. (2024). GOLEM Ontology for Narrative and Fiction. https://doi.org/10.5281/zenodo.14911392

# Golem Ontology for Narrative and Fiction

Ontology of fiction and narrative, developed as an extension of the [Erlangen CRM](http://erlangen-crm.org/) and aligned with the [DOLCE-Lite-Plus Ecosystem](https://www.w3.org/2001/sw/BestPractices/WNET/DLP3941_daml.html).

It adopts a [DOLCE+DnS Ultralite](https://akswnc7.informatik.uni-leipzig.de/dstreitmatter/archivo/ontologydesignpatterns.org/ont--dul--DUL--owl/2021.06.07-182648/ont--dul--DUL--owl_type=pyLodeDoc.html) design pattern for modelling textual and character attributes.

GOLEM also reuses selected constructs from [LRMoo](https://cidoc-crm.org/lrmoo/) while preserving their original namespace and introducing only the additional classes and relations required for its modelling purposes.

Narrative phenomena can be viewed as interconnected systems in which various components influence one another. Understanding the properties of narratives requires analyzing them in relation to each other and within their broader context, rather than in isolation ([Pianzola, 2018](https://golemlab.eu/publications/complexity/)). Formal ontologies provide a structured and systematic approach to representing the essential elements of storytelling. By capturing relevant concepts, constraints, and interrelationships among narrative elements, ontology ensures a consistent and explicit representation of the narrative domain.

In literary studies, traditional quantitative and probabilistic methods often struggle to account for the semantic richness and intensional qualities of texts ([Ciotti, 2016](https://impactum-journals.uc.pt/matlit/article/download/2182-8830_4-1_2/1932?inline=1)). In contrast, ontology modeling highlights the complexities of narrative structure, making these elements explicit and computable.

The GOLEM project developed an ontology that models narratives and fiction independently of their specific domains. To achieve this, the project seeks to identify a common ground that defines how key elements of narrative structure—such as events, characters, social relationships, and settings—interrelate. By employing a modularization approach, GOLEM will create a comprehensive library of modules that encapsulate these narrative components, including modules for characters, relationships, events, settings, and narrative inference.

GOLEM v2.0 introduces a major architectural and semantic refactoring of the ontology. The ontology now adopts Erlangen CRM as its CRM foundation and uses a lightweight reuse strategy for selected LRMoo constructs, avoiding the import of the full LRMoo and CRM OWL dependency chain. The feature model has been revised through the DUL Region pattern, with G2_Feature represented as a region and GP0_has_feature aligned with the corresponding region relation.

The v2.0 revision further removes the use of dol:generically-dependent-on, avoiding an unnecessary semantic commitment where the relevant dependencies can instead be addressed through provenance mechanisms.
These changes substantially reduce the ontology's import closure while preserving the intended semantics of the GOLEM conceptualization and improving computational tractability and maintainability.

The detailed description of each module can be read in the [GitHub](https://github.com/GOLEM-lab/golem-ontology/wiki).

Furthermore, the ontology contributes to comparative studies by providing a structured framework for analyzing narratives across different cultural contexts. It enhances our understanding of cumulative cultural evolution in narratives, allowing for a more nuanced exploration of how narratives evolve and grows cumulatively over time ([Pianzola et al., 2020](https://ceur-ws.org/Vol-2723/short8.pdf)).

- The detailed description of each module can be read in the [Wiki](https://github.com/GOLEM-lab/golem-ontology/wiki).

- The complete description of classes and properties can be read in the [formal documentation](https://ontology.golemlab.eu/).

The figure below is an overview of the main classes and their relationships.

![GOLEM Core](GOLEM_core.png)

### References

Ciotti, F. (2016). Toward a formal ontology for narrative. *MATLIT: Materialidades da Literatura*, 4(1), 29-44.

Pianzola, F. (2018). Looking at narrative as a complex system: The proteus principle. In *Narrating complexity* (pp. 101-122).

Pianzola, F., Acerbi, A., & Rebora, S. (2020). Cultural accumulation and improvement in online fan fiction. In *CEUR Workshop Proceedings* (Vol. 2723).

# Technical implementation

- Ontology development: Protégé 
- Diagrams: Lucidchart
- Documentation: PyLode + custom GitHub action to publish im HTML via GitHub Pages
- Evaluation: FOOPS! and Ontometrics

