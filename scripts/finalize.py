import glob
import os
import pickle

from config import prefix
from rdflib import Graph
from tqdm import tqdm

# from utils import upload_files_to_owncloud

# user = os.environ["OWNCLOUD_USER"]
# pw = os.environ["OWNCLOUD_PW"]


files = glob.glob(f"./datasets/{prefix}_*.pickle")
print(files)


out_file = os.path.join("datasets", f"{prefix}.nt")
print(out_file)
g = Graph()
for x in tqdm(files, total=len(files)):
    with open(x, "rb") as f:
        g += pickle.load(f)
print(f"serializing graph to {out_file}")
g.serialize(out_file, format="nt", encoding="utf-8")

# files = glob.glob("./datasets/*.nt")
# upload = upload_files_to_owncloud(files, user, pw, folder="pfp-data")
# print(upload)
