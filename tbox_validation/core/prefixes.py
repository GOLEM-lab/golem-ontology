# core/prefixes.py

PREFIXES = """
@prefix : <https://w3id.org/golem/ontology#> .
@prefix golem: <https://w3id.org/golem/ontology#> .

@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix vs: <http://www.w3.org/2003/06/sw-vocab-status/ns#> .

@prefix dlp_csm: <http://www.ontologydesignpatterns.org/ont/dlp/> .
@prefix dlp_temp: <http://www.ontologydesignpatterns.org/ont/dlp/TemporalRelations.owl#> .
@prefix dlp_spat: <http://www.ontologydesignpatterns.org/ont/dlp/SpatialRelations.owl#> .
@prefix dlp_funct: <http://www.ontologydesignpatterns.org/ont/dlp/FunctionalParticipation.owl#> .
@prefix dlp_extDnS: <http://www.ontologydesignpatterns.org/ont/dlp/ExtendedDnS.owl#> .
@prefix dlp_lite: <http://www.ontologydesignpatterns.org/ont/dlp/DOLCE-Lite.owl#> .

@prefix dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#> .
@prefix crm: <http://erlangen-crm.org/240307/> .
@prefix ecrm: <http://erlangen-crm.org/240307/> .

@prefix lrmoo: <http://iflastandards.info/ns/lrm/lrmoo/> .

@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

def with_prefixes(snippet: str) -> str:
    return PREFIXES + "\n" + snippet.strip()