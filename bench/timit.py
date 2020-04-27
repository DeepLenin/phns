import numpy as np
import os
from tqdm import tqdm
import pickle

import sys
sys.path.append('../phns')
import phns


DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../data/"

print(f"Loading data from {DATA_PATH}")
with open(DATA_PATH + "timit_bench.pkl", "rb") as f:
    data = pickle.load(f)


cers = []
for item in tqdm(data):
    # Preprocessing data
    _phns = phns.utils.timit_to_cmu(item["phns"])
    _phns = [phn for phn in _phns if phn != "sil"]

    try:
        # if item['text'] == 'Princes and factions clashed in the open street and died on the open scaffold.\n':
        #     import ipdb
        #     ipdb.set_trace()
        calculated_phns_variants = phns.from_text(item["text"], apply_heuristics=False)
    except:
        print(item)
        raise

    # if not calculated_phns_variants:
    #     continue

    # best = phns.closest(_phns, calculated_phns_variants)
    # cers.append(best["cer"])

# print(cers)
print({
    '25%': np.percentile(cers, 25),
    '50%': np.percentile(cers, 50),
    '75%': np.percentile(cers, 75),
    '95%': np.percentile(cers, 95)
})
