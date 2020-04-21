import numpy as np
import os
from tqdm import tqdm
import pickle
from multiprocessing import Pool

import sys
sys.path.append('../phns')
import phns


DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../data/"

print(f"Loading data from {DATA_PATH}")
with open(DATA_PATH + "timit_bench.pkl", "rb") as f:
    data = pickle.load(f)


def process_item(item):
    pbar.update()
    # Preprocessing data
    _phns = phns.utils.timit_to_cmu(item["phns"])
    _phns = [phn for phn in _phns if phn != "sil"]

    try:
        # if item['text'] == 'Princes and factions clashed in the open street and died on the open scaffold.\n':
        #     import ipdb
        #     ipdb.set_trace()
        calculated_phns_variants = phns.from_text(item["text"], apply_heuristics=True)
    except:
        print(item)
        raise

    if not calculated_phns_variants:
        return

    best = phns.closest(_phns, calculated_phns_variants)
    return best["cer"]

pbar = tqdm(total=int(len(data)/6))

pool = Pool(6)
cers = pool.map(process_item, data)
cers = [cer for cer in cers if cer]

#cers.append(best["cer"])
#for item in tqdm(data):
#    cers.append(process_item(item))

# print(cers)
print({
    '25%': np.percentile(cers, 25),
    '50%': np.percentile(cers, 50),
    '75%': np.percentile(cers, 75),
    '95%': np.percentile(cers, 95)
})
