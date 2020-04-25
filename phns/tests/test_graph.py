import phns.text

graph = phns.text.from_text('hello world, my best friend, i love to breath air, what about you?', apply_heuristics=False)
dot = graph.to_graphviz()
dot.view()
