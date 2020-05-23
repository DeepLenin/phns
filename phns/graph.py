import itertools

import numpy as np
from scipy.sparse.csgraph import shortest_path


class Node:
    def __init__(self, value, index, meta={}):
        self.in_edges = []
        self.out_edges = []
        self.value = value
        self.index = index
        self.meta = meta

    def __repr__(self):
        return f'Node("{self.value}")'

    @property
    def in_nodes(self):
        return [edge.from_node for edge in self.in_edges]

    @property
    def out_nodes(self):
        return [edge.to_node for edge in self.out_edges]


class Edge:
    def __init__(self, from_node, to_node, meta={}):
        self.from_node = from_node
        self.to_node = to_node
        self.meta = meta
        from_node.out_edges.append(self)
        to_node.in_edges.append(self)

    def __repr__(self):
        return f"Edge({self.from_node}->{self.to_node})"


class Graph:
    def __init__(self):
        self.roots = []
        self.tails = []
        self.nodes = []
        self.max_length = 0
        self._shortest_paths = None
        self._distance_matrix = None
        self._transition_matrix = None
        self._final_transitions = None
        self._initial_transitions = None

    @property
    def distance_matrix(self):
        if self._distance_matrix is None:
            mat = np.zeros((len(self.nodes), len(self.nodes)))
            for node in self.nodes:
                for out in node.out_nodes:
                    mat[node.index, out.index] = 1
            self._distance_matrix, self._shortest_paths = shortest_path(
                mat, method="FW", return_predecessors=True
            )
            self._distance_matrix[self._distance_matrix == np.inf] = 0
        return self._distance_matrix

    @property
    def shortest_paths(self):
        if self._shortest_paths is None:
            self.distance_matrix
        return self._shortest_paths

    @property
    def transition_matrix(self):
        if self._transition_matrix is None:
            mat = np.exp2(-self.distance_matrix + 1)
            mat[self.distance_matrix == 0] = 0
            np.fill_diagonal(mat, 1)
            self._transition_matrix = mat
        return self._transition_matrix

    @property
    def initial_transitions(self):
        if self._initial_transitions is None:
            idxs = [it.index for it in self.roots]
            transitions = self.transition_matrix[idxs].max(axis=0) / 2
            transitions[idxs] = 1
            self._initial_transitions = transitions
        return self._initial_transitions

    @property
    def final_transitions(self):
        if self._final_transitions is None:
            idxs = [it.index for it in self.tails]
            transitions = self.transition_matrix[:, idxs].max(axis=1) / 2
            transitions[idxs] = 1
            self._final_transitions = transitions
        return self._final_transitions

    def attach(self, pronunciations, word=None):
        self.max_length += max([len(p) for p in pronunciations])
        first_pronunciation = list(pronunciations)[0]
        is_dict = isinstance(pronunciations, dict)

        if len(pronunciations) > 1:
            # h e l l o
            # h e w l o
            # h a l o
            # 1. zip вперед и находим первый разный элемент - с этого элемента
            #   наши ноды расходятся
            # 2. zip с конца с подсчетом индекса в отрицательном виде
            #   (-1, -2...) - находим первый разный элемент с конца - это место где
            #   наши ветки объединяются
            # 3. Создаем начальную общую ветку
            # 4. Создаем все разные средние ветки
            # 5. Объединяем все ветки в одну, даже если это просто нода конца слова.

            i_diff_forward = __find_index_of_first_diff__(pronunciations)
            reversed_pronunciations = [list(reversed(p)) for p in pronunciations]
            i_diff_reverse = -__find_index_of_first_diff__(reversed_pronunciations) - 1

            for i in range(i_diff_forward):
                self.tails = [
                    self.__add_phn__(first_pronunciation[i], meta={"word": word})
                ]

            new_tails = []

            if not self.roots and not i_diff_forward:
                least_len = min([len(pr) for pr in pronunciations])
                if least_len - i_diff_forward < -i_diff_reverse:
                    i_diff_reverse += 1

            for pronunciation in pronunciations:
                prev_nodes = self.tails

                meta = {"word": word}
                if is_dict:
                    meta["variant"] = pronunciations[pronunciation]

                for phn in pronunciation[i_diff_forward:i_diff_reverse]:
                    node = self.__add_phn__(phn, prev_nodes, meta=meta)
                    prev_nodes = [node]

                if len(pronunciation) - i_diff_forward >= -i_diff_reverse:
                    phn = pronunciation[i_diff_reverse]
                    node = self.__add_phn__(phn, prev_nodes, meta=meta)
                    prev_nodes = [node]

                new_tails.extend(prev_nodes)

            self.tails = new_tails

            for i in range(i_diff_reverse + 1, 0):
                self.tails = [
                    self.__add_phn__(first_pronunciation[i], meta={"word": word})
                ]
        else:
            for phn in first_pronunciation:
                self.tails = [self.__add_phn__(phn, meta={"word": word})]

        return self

    def __create_node__(self, phn, meta):
        node = Node(phn, len(self.nodes), meta=meta)
        self.nodes.append(node)
        return node

    def __add_phn__(self, phn, prev_nodes=None, meta={}):
        node = self.__create_node__(phn, meta=meta)
        if not self.tails and not prev_nodes:
            self.roots.append(node)
        if prev_nodes is None:
            prev_nodes = self.tails
        for prev_node in prev_nodes:
            Edge(from_node=prev_node, to_node=node)
        return node

    def to_graphviz(self):
        import graphviz

        dot = graphviz.Digraph()
        for node in self.nodes:
            dot.node(str(id(node)), str(node.value))

        for node in self.nodes:
            for edge in node.out_edges:
                dot.edge(str(id(node)), str(id(edge.to_node)))
        return dot

    def to_list(self):
        result = []
        for root in self.roots:
            for node in self.__traverse__(root, []):
                if node not in result:
                    result.append(node)
        return result

    def __traverse__(self, node, prefix):
        result = []
        new_prefix = prefix.copy()
        new_prefix.append(node.value)
        for next_node in node.out_nodes:
            result.extend(self.__traverse__(next_node, new_prefix))
        return result or [new_prefix]

    def triples(self):
        result = []
        for node in self.nodes:
            result += self.__fetch_triples__(node)
        return result

    def __fetch_triples__(self, node):
        return itertools.product(
            node.in_nodes or [None], [node], node.out_nodes or [None]
        )

    def create_edge(self, from_node, to_node, meta={}):
        if to_node in from_node.out_nodes:
            return []

        if from_node.value == to_node.value:
            triples = []
            if to_node.out_nodes:
                for node in to_node.out_nodes:
                    triples += self.create_edge(from_node, node)
            elif from_node.in_nodes:
                for node in from_node.in_nodes:
                    triples += self.create_edge(node, to_node)
            return triples

        Edge(from_node, to_node)

        new_triples_before_edge = itertools.product(
            from_node.in_nodes or [None], [from_node], [to_node]
        )
        new_triples_after_edge = itertools.product(
            [from_node], [to_node], to_node.out_nodes or [None]
        )

        return list(new_triples_before_edge) + list(new_triples_after_edge)

    def create_node_between(self, phn, from_node, to_node, meta={}):
        if to_node and to_node.value == phn:
            return self.create_edge(from_node, to_node)

        node = self.__create_node__(phn, meta=meta)
        new_triples = self.create_edge(from_node, node)
        if to_node:
            new_triples += self.create_edge(node, to_node)
        else:
            self.tails.append(Node)

        new_triples += self.__fetch_triples__(node)
        return new_triples


def __find_index_of_first_diff__(seqs):
    i = 0
    cardinality = len(seqs)

    for i_items in itertools.zip_longest(*seqs):
        if i_items.count(i_items[0]) == cardinality:
            i += 1
        else:
            return i

    raise Exception
