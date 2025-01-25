import glob
import pickle
import os
from rdflib import Graph

from utils import upload_files_to_owncloud

user = os.environ["OWNCLOUD_USER"]
pw = os.environ["OWNCLOUD_PW"]

prefix = "pmb"

files = glob.glob(f"./datasets/{prefix}_*.pickle")

if len(files) != 4:
    print("there is a least on file missing! Stopping script")
else:
    out_file = os.path.join("datasets", f"{prefix}.nt")
    g = Graph()
    for x in files:
        with open(x, "rb") as f:
            g += pickle.load(f)
        os.unlink(x)
    print(f"serializing graph to {out_file}")
    g.serialize(out_file, format="nt", encoding="utf-8")

files = glob.glob("./datasets/*.nt")
upload = upload_files_to_owncloud(files, user, pw, folder="pfp-data")
print(upload)
