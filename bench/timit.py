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
    calculated_phns_variants = phns.from_text(item["text"])
    if not calculated_phns_variants:
        continue

    best = phns.closest(item["phns"], calculated_phns_variants)
    cers.append(best["cer"])

print(cers)
print({
    '25%': np.percentile(cers, 25),
    '50%': np.percentile(cers, 50),
    '75%': np.percentile(cers, 75),
    '95%': np.percentile(cers, 95)
})
