import os
import pickle

import requests
from acdh_cidoc_pyutils import tei_relation_to_SRPC3_in_social_relation
from acdh_tei_pyutils.tei import TeiReader
from rdflib import Graph

index_file = "https://pmb.acdh.oeaw.ac.at/network/tei/?source_kind=person&target_kind=institution"
rdf_dir = "./datasets"
os.makedirs(rdf_dir, exist_ok=True)


lookup_dict = requests.get(
    "https://pfp-schema.acdh.oeaw.ac.at/mappings/person-person.json"
).json()
doc = TeiReader(index_file)
g = Graph()
g.parse("https://pfp-schema.acdh.oeaw.ac.at/types/person-person/person-person.ttl")
for x in doc.any_xpath(".//tei:relation"):
    g += tei_relation_to_SRPC3_in_social_relation(
        x,
        domain="https://pmb.acdh.oeaw.ac.at/",
        lookup_dict=lookup_dict,
        verbose=True,
        entity_prefix="person__",
    )

save_path = os.path.join(rdf_dir, "pmb_person-place-relations.pickle")
print(f"saving graph as {save_path}")
with open(save_path, "wb") as f:
    pickle.dump(g, f)

g.serialize("foo.nt", format="nt", encoding="utf-8")
