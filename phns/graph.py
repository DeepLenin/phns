import itertools

class Node:
    def __init__(self, value):
        self.in_edges = []
        self.out_edges = []
        self.value = value

    def __repr__(self):
        return f"Node(\"{self.value}\")"

    def in_nodes(self):
        return [edge.from_node for edge in self.in_edges]

    def out_nodes(self):
        return [edge.to_node for edge in self.out_edges]


class Edge:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        from_node.out_edges.append(self)
        to_node.in_edges.append(self)

    def __repr__(self):
        return f"Edge({self.from_node}->{self.to_node})"


class Graph:
    def __init__(self):
        self.roots = []
        self.tails = []

    def calculate_distances(self):
        self.distances = {}
        self.__distance__([self.root])

    def __distance__(self, prev_nodes):
        node = prev_nodes[-1]
        for edge in node.out_edges:
            next_node = edge.to_node

            for distance, prev_node in enumerate(reversed(prev_nodes)):
                self.distances[(prev_node, next_node)] = min(self.distances.get((prev_node, next_node), float("inf")), distance + 1)

            prev_nodes.append(next_node)
            self.__distance__(prev_nodes)
            prev_nodes.pop()

    def attach(self, pronunciations):
        if len(pronunciations) > 1:
            # h e l l o
            # h e w l o
            # h a l o
            # 1. zip вперед и находим первый разный элемент - с этого элемента наши ноды расходятся
            # 2. zip с конца с подсчетом индекса в отрицательном виде (-1, -2...) - находим первый разный элемент с конца - это место где наши ветки объединяются
            # 3. Создаем начальную общую ветку
            # 4. Создаем все разные средние ветки
            # 5. Объединяем все ветки в одну, даже если это просто нода конца слова.

            i_diff_forward = __find_index_of_first_diff__(pronunciations)
            reversed_pronunciations = [list(reversed(p)) for p in pronunciations]
            i_diff_reverse = -__find_index_of_first_diff__(reversed_pronunciations)-1

            for i in range(i_diff_forward):
                self.tails = [self.__add_phn__(pronunciations[0][i])]

            new_tails = []

            if not self.roots and not i_diff_forward:
                least_len = min([len(pronunciation) for pronunciation in pronunciations])
                if least_len - i_diff_forward < -i_diff_reverse:
                    i_diff_reverse += 1

            for pronunciation in pronunciations:
                prev_nodes = self.tails

                for phn in pronunciation[i_diff_forward:i_diff_reverse]:
                    node = self.__add_phn__(phn, prev_nodes)
                    prev_nodes = [node]

                if len(pronunciation) - i_diff_forward >= -i_diff_reverse:
                    phn = pronunciation[i_diff_reverse]
                    node = self.__add_phn__(phn, prev_nodes)
                    prev_nodes = [node]

                new_tails.extend(prev_nodes)

            self.tails = new_tails

            for i in range(i_diff_reverse+1, 0):
                self.tails = [self.__add_phn__(pronunciations[0][i])]
        else:
            for phn in pronunciations[0]:
                self.tails = [self.__add_phn__(phn)]

        return self


    def __add_phn__(self, phn, prev_nodes=None):
        node = Node(phn)
        if not self.tails and not prev_nodes:
            self.roots.append(node)
        if prev_nodes is None:
            prev_nodes = self.tails
        for prev_node in prev_nodes:
            Edge(from_node=prev_node, to_node=node)
        return node


    def __iter__(self):
        nodes = self.roots
        visited = set(nodes)
        while nodes:
            new_nodes = []
            for node in nodes:
                yield node
                visit_nodes = set(edge.to_node for edge in node.out_edges if edge.to_node not in visited)
                visited.update(visit_nodes)
                new_nodes.extend(visit_nodes)
            nodes = new_nodes


    def to_graphviz(self):
        import graphviz

        dot = graphviz.Digraph()
        for node in self:
            dot.node(str(id(node)), str(node.value))

        for node in self:
            for edge in node.out_edges:
                dot.edge(str(id(node)), str(id(edge.to_node)))
        return dot


    def to_list(self):
        result = []
        for root in self.roots:
            [result.append(it) for it in self.__traverse__(root, []) if it not in result]
        return result


    def __traverse__(self, node, prefix):
        result = []
        new_prefix = prefix.copy()
        new_prefix.append(node.value)
        for next_node in node.out_nodes():
            result.extend(self.__traverse__(next_node, new_prefix))
        return result or [new_prefix]


    def triples(self):
        result = []
        for node in self:
            result += self.__fetch_triples__(node)
        return result


    def __fetch_triples__(self, node):
        return itertools.product(node.in_nodes() or [None], [node], node.out_nodes() or [None])


    def create_edge(self, from_node, to_node):
        if to_node in from_node.out_nodes():
            return []

        Edge(from_node, to_node)

        new_triples_before_edge = itertools.product(from_node.in_nodes() or [None], [from_node], [to_node])
        new_triples_after_edge  = itertools.product([from_node], [to_node], to_node.out_nodes() or [None])

        return list(new_triples_before_edge) + list(new_triples_after_edge)


    def create_node_between(self, phn, from_node, to_node):
        if to_node and to_node.value == phn:
            return self.create_edge(from_node, to_node)

        node = Node(phn)
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
