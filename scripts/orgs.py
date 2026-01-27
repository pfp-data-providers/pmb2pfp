import os
import pickle

import requests
from acdh_cidoc_pyutils import (
    make_appellations,
    make_e42_identifiers,
)
from acdh_cidoc_pyutils.namespaces import CIDOC
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP
from config import LIMIT, PU
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from tqdm import tqdm

entity_type = "org"
g = Graph()

rdf_dir = "./datasets"
os.makedirs(rdf_dir, exist_ok=True)

index_file = f"./list{entity_type}.xml"


print("check if source file exists")
if os.path.exists(index_file):
    pass
else:
    url = f"https://pmb.acdh.oeaw.ac.at/media/{index_file}"
    print(f"fetching {index_file} from {url}")
    response = requests.get(url)
    with open(index_file, "wb") as file:
        file.write(response.content)


doc = TeiReader(index_file)
items = doc.any_xpath(f".//tei:{entity_type}[@xml:id]")
if LIMIT:
    items = items[:LIMIT]

for x in tqdm(items, total=len(items)):
    xml_id = get_xmlid(x)
    item_id = f"{PU}{xml_id}"
    subj = URIRef(item_id)
    g.add((subj, RDF.type, CIDOC["E74_Group"]))

    # ids
    g += make_e42_identifiers(
        subj,
        x,
        type_domain="https://pfp-custom-types",
        default_lang="de",
    )

    # names
    g += make_appellations(
        subj, x, type_domain="https://pfp-custom-types", default_lang="de"
    )

    # located
    for y in x.xpath(
        ".//tei:location[@type='located_in_place']/tei:placeName/@key", namespaces=NSMAP
    ):
        g.add((subj, CIDOC["P74_has_current_or_former_residence"], URIRef(f"{PU}{y}")))

save_path = os.path.join(rdf_dir, f"pmb_{entity_type}.pickle")
print(f"saving graph as {save_path}")
with open(save_path, "wb") as f:
    pickle.dump(g, f)
