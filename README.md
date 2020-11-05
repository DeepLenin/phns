# phns

A friendly, lightweight, graph-based transcriber and scorer for deep Lening (but
not only) applications. Based on
[cmudict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) and English heuristics.

* **Lightweight**. Depending only on `numpy` and `scipy`.
* **Fast**. Because of graph-nature of algorithm - it can produce transcription
  variants much faster than through straight combinatory
* **Smart**. Includes viterbi algorithm to find best way through your
  predictions.

```python
import phns

graph = phns.from_text("Hello world!")
for pronounciation in graph.to_list():
    print("-".join([str(phn) for phn in pronounciation]))

# =>
# hh-eh-l-ow-w-er-l-d
# hh-ah-l-ow-w-er-l-d
# hh-l-ow-w-er-l-d
```

# Work still in progress
