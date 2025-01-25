import glob
import os
from rdflib import Graph

from utils import upload_files_to_owncloud

user = os.environ["OWNCLOUD_USER"]
pw = os.environ["OWNCLOUD_PW"]

prefix = "pmb"

files = glob.glob(f"./datasets/{prefix}_*.ttl")

if len(files) != 4:
    print("there is a least on file missing! Stopping script")
else:
    out_file = os.path.join("datasets", f"{prefix}.ttl")
    g = Graph()
    for x in files:
        g.parse(x)
        os.unlink(x)
    print(f"serializing graph to {out_file}")
    g.serialize(out_file)

files = glob.glob("./datasets/*.ttl")
upload = upload_files_to_owncloud(files, user, pw, folder="pfp-data")
print(upload)
