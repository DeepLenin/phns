import os
import pickle

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

    # import ipdb
    # ipdb.set_trace()
    # try:
    graph = phns.from_text(item["text"], apply_heuristics=True)
    if graph:
        phns.closest(_phns, graph)
    else:
        skipped += 1
    # except:
    #     import ipdb
    #     ipdb.set_trace()
    #     graph = phns.from_text(item["text"], apply_heuristics=True)
    #     print(item)
    #     raise

    # if not calculated_phns_variants:
    #     continue

    # best = phns.closest(_phns, calculated_phns_variants)
    # cers.append(best["cer"])

print("skipped: ", skipped)
# print(cers)
# print({
#     '25%': np.percentile(cers, 25),
#     '50%': np.percentile(cers, 50),
#     '75%': np.percentile(cers, 75),
#     '95%': np.percentile(cers, 95)
# })
