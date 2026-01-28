import os
import pickle

import requests
from acdh_cidoc_pyutils import check_for_hash
from acdh_cidoc_pyutils.namespaces import CIDOC
from acdh_tei_pyutils.tei import TeiReader
from config import PU
from lxml.etree import Element
from rdflib import RDF, RDFS, Graph, Literal, URIRef


def p143_person_org_joining(
    node: Element,
    domain: URIRef,
    prefix_subject="",
    prefix_object="",
    mapping={},
    label_lang="de",
    default_type="https://pfp-schema.acdh.oeaw.ac.at/types/person-institution/#Person-institution-relation",
) -> Graph:
    """Converts a tei:node like
    <relation name="arbeitet-fur" active="#12692" passive="#39689" from-iso="1957-01-01"
    n="Schnitzler, Heinrich — arbeitet für — Theater in der Josefstadt"
    type="personinstitution"/> of a typed person-group relation into a CIDOC CRM RDF graph like:
    <crm:E21> crm:P143i_was_joined_by <crm:E85_Joining> .
    <crm:E85_Joining> crm:P01i_is_domain_of <crm:PC144_joined_with> .
    <crm:PC144_joined_with> P02_has_range <crm:E55_Type> .
    <crm:PC144_joined_with> P144_1_kind_of_member <crm:E74_Group>

    Args:
        node (Element): A tei:relation node.
        domain (URIRef): A domain to create the institutions URI.
        prefix_subject (str, optional): A prefix needed to create the E21 person's URI. Defaults to ""
        prefix_object (str, optional): A prefix needed to create the E74 group's URI. Defaults to "".
        mapping (dict, optional): A mapping from local terms to a normalized vocabulary. Defaults to {}.
        label_lang(str, optional): The lang code for the E85_Joining. Defaults to en.
        default_type(str, optional): A default for <crm:PC144_joined_with> P144_1_kind_of_member <crm:E55_Type>

    Returns:
        Graph: The graph
    """
    g = Graph()

    subj_id = check_for_hash(node.attrib["active"])
    obj_id = check_for_hash(node.attrib["passive"])
    subj = URIRef(f"{domain}{prefix_subject}{subj_id}")
    obj = URIRef(f"{domain}{prefix_object}{obj_id}")
    joining_uri = URIRef(f"{subj}/E85_Joining/{obj_id}")
    joined_with_uri = URIRef(f"{joining_uri}/PC144_joined_with")
    g.add((joined_with_uri, RDF.type, CIDOC["PC144_joined_with"]))
    g.add((subj, CIDOC["P143i_was_joined_by"], joining_uri))
    g.add((joining_uri, RDF.type, CIDOC["E85_Joining"]))
    g.add((joining_uri, RDFS.label, Literal(node.attrib["n"], lang=label_lang)))
    g.add((joining_uri, CIDOC["P01i_is_domain_of"], joined_with_uri))
    g.add((joined_with_uri, CIDOC["P02_has_range"], obj))
    relation_name = node.attrib["name"]
    try:
        default_type = mapping[relation_name]
    except KeyError:
        print(f"no mapping for {relation_name} found")
    g.add((joined_with_uri, CIDOC["P144_1_kind_of_member"], URIRef(default_type)))
    g.add((URIRef(default_type), RDF.type, CIDOC["E55_Type"]))
    return g


index_file = "https://pmb.acdh.oeaw.ac.at/network/tei/?source_kind=person&target_kind=institution&columns=end_date&sort=end_date"  # noqa:
# index_file = "person-org.xml"
rdf_dir = "./datasets"
os.makedirs(rdf_dir, exist_ok=True)


lookup_dict = requests.get(
    "https://pfp-schema.acdh.oeaw.ac.at/mappings/person-institution.json"
).json()
doc = TeiReader(index_file)
doc.tree_to_file("person-org.xml")
g = Graph()
g.parse(
    "https://pfp-schema.acdh.oeaw.ac.at/types/person-institution/person-institution.ttl"
)
for x in doc.any_xpath(".//tei:relation"):
    g += p143_person_org_joining(
        x, PU, prefix_subject="person__", prefix_object="org__", mapping=lookup_dict
    )
save_path = os.path.join(rdf_dir, "pmb_person-org-relations.pickle")
print(f"saving graph as {save_path}")
with open(save_path, "wb") as f:
    pickle.dump(g, f)
g.serialize("foo.nt", format="nt", encoding="utf-8")
