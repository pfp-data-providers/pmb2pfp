import os
import pickle
import requests

from acdh_cidoc_pyutils import tei_relation_to_SRPC3_in_social_relation
from acdh_tei_pyutils.tei import TeiReader
from rdflib import Graph

index_file = "pmb-person-person.xml"
rdf_dir = "./datasets"
os.makedirs(rdf_dir, exist_ok=True)

print("check if source file exists")
if os.path.exists(index_file):
    pass
else:
    url = "https://pmb.acdh.oeaw.ac.at/network/tei/?edge_kind=personperson"
    print(f"fetching {index_file} from {url}")
    response = requests.get(url, timeout=180)
    with open(index_file, "wb") as file:
        file.write(response.content)

lookup_dict = requests.get(
    "https://acdh-oeaw.github.io/pfp-schema/mappings/person-person.json"
).json()
doc = TeiReader(index_file)
g = Graph()
g.parse("https://acdh-oeaw.github.io/pfp-schema/types/person-person/person-person.ttl")
for x in doc.any_xpath(".//tei:relation"):
    g += tei_relation_to_SRPC3_in_social_relation(
        x,
        domain="https://pmb.acdh.oeaw.ac.at/",
        lookup_dict=lookup_dict,
        verbose=True,
        entity_prefix="person__",
    )

save_path = os.path.join(rdf_dir, "pmb_person-person-relations.pickle")
print(f"saving graph as {save_path}")
with open(save_path, "wb") as f:
    pickle.dump(g, f)
