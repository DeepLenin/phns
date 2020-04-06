import academictorrents as at
import numpy as np
import os
from glob import glob

import sys
sys.path.append('../phns')
import phns

root = os.path.expanduser("~/.academictorrents-datastore/TIMIT")

if not os.path.exists(root):
    from zipfile import ZipFile
    with ZipFile(at.get("34e2b78745138186976cbc27939b1b34d18bd5b3")) as zipped:
        zipped.extractall(root)

data = []
for text_path in glob(root + "/data/lisa/data/timit/raw/TIMIT/*/*/*/*.TXT"):
    phns_path = text_path.replace(".TXT", ".PHN")

    data.append(dict(
        text = open(text_path).read().split(" ", 2)[-1],
        phns = [phn.split(" ")[-1] for phn in open(phns_path).read().split("\n") if phn]
    ))


cers = []
for item in data:
    calculated_phns = phns.from_text(item["text"])
    if not calculated_phns:
        continue

    comparison = phns.compare(item["phns"], calculated_phns)
    cers.append(comparison["cer"])
    # comparison["diff"]
    # analyze error types

cers = np.array(cers)
# print({ 'cers.percentile
