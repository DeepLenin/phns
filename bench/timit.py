import os
import pickle

import numpy as np
from tqdm import tqdm

import phns

DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../data/"

print(f"Loading data from {DATA_PATH}")
with open(DATA_PATH + "timit_bench.pkl", "rb") as f:
    data = pickle.load(f)


# missing words:
#    exceptions = [
#        "motorists'",
#        "morphophonemic",
#        "nihilistic",
#        "radiosterilization",
#        "exhusband",
#        "somebody'll",
#        "smolderingly",
#        "geocentricism",
#        "unmagnified",
#        "stirrin",
#        "utopianism",
#        "infuriation",
#        "preprepared",
#        "understandingly",
#        "eventualities",
#        "micrometeorites",
#        "herdin'",
#        "responsively",
#        "demineralization",
#        "unwaveringly",
#        "cap'n",
#        "mournfully",
#        "andrei's",
#        "autofluorescence",
#        "fasciculations",
#        "weatherstrip",
#        "nonsystematic",
#        "traditionalism",
#        "chorused",
#        "micrometeorite",
#        "reupholstering",
#        "castorbeans"
#    ]

cers = []
skipped = 0
for item in tqdm(data):
    # Preprocessing data
    _phns = phns.utils.timit_to_cmu(item["phns"])
    _phns = [phns.Phn(phn) for phn in _phns if phn != "sil"]

    # TODO: Convert TIMIT 64 to our cmu phonemes
    # TODO: Think about stressed phonemes - how we compare stressed with nonstressed
    # TODO: Run bench

    try:
        graph = phns.from_text(item["text"], apply_heuristics=True)
        if graph:
            result = phns.closest(_phns, graph)
            cers.append(result["cer"])
            if result["cer"] > 0.2 and False:
                print(item["text"])
                print("phns", item["phns"])
                print("_phns", [phn.val for phn in _phns])
                print("targt", [phn.val for phn in result["target"]])
                print("match", [graph.nodes[m].value.val for m in result["match"]])
                print(result)
                import ipdb

                ipdb.set_trace()
        else:
            skipped += 1
    except Exception as err:
        import ipdb

        ipdb.set_trace()
        graph = phns.from_text(item["text"], apply_heuristics=True)
        phns.closest(_phns, graph)
        raise err


print("skipped: ", skipped)
print(
    {
        "25%": np.percentile(cers, 25),
        "50%": np.percentile(cers, 50),
        "75%": np.percentile(cers, 75),
        "95%": np.percentile(cers, 95),
    }
)
