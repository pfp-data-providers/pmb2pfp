import os

from rdflib import Namespace

prefix = "pmb"
domain = "https://pmb.acdh.oeaw.ac.at/"
PU = Namespace(domain)


if os.environ.get("NO_LIMIT"):
    LIMIT = False
    print("no limit")
else:
    LIMIT = 1000
