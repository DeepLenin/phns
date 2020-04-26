import itertools

class Node:
    def __init__(self, node_type=None):
        self.type = node_type
        self.out_edges = []

class Edge:
    def __init__(self, value, to_node):
        self.value = value
        self.to_node = to_node

class Graph:
    def __init__(self):
        self.root = Node("<ROOT>")
        self.last_node = self.root

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

            # if len(pronunciations[0]) == 2:
            #     import ipdb
            #     ipdb.set_trace()

            i_diff_forward = __find_index_of_first_diff__(pronunciations)
            reversed_pronunciations = [list(reversed(p)) for p in pronunciations]
            i_diff_reverse = -__find_index_of_first_diff__(reversed_pronunciations)-1

            for i in range(i_diff_forward):
                self.last_node = self.add_phn(pronunciations[0][i])

            prev_last_node = self.last_node
            self.last_node = Node()

            for pronunciation in pronunciations:
                node = prev_last_node
                for phn in pronunciation[i_diff_forward:i_diff_reverse]:
                    node = self.add_phn(phn, node)

                if len(pronunciation) - i_diff_forward >= -i_diff_reverse:
                    phn = pronunciation[i_diff_reverse]
                else:
                    phn = None

                self.add_phn(phn, node, next_node=self.last_node)


            for i in range(i_diff_reverse+1, 0):
                self.last_node = self.add_phn(pronunciations[0][i])
        else:
            for phn in pronunciations[0]:
                self.last_node = self.add_phn(phn)

        self.last_node.type = "<WORD>"


    def add_phn(self, phn, node=None, next_node=None):
        if not node:
            node = self.last_node
        if not next_node:
            next_node = Node()
        new_edge = Edge(phn, to_node=next_node)
        node.out_edges.append(new_edge)
        return next_node


    def __iter__(self):
        nodes = [self.root]
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
            dot.node(str(id(node)), node.type or '')

        for node in self:
            for edge in node.out_edges:
                dot.edge(str(id(node)), str(id(edge.to_node)), label=str(edge.value))
        return dot


    def to_list(self):
        return self.__traverse__(self.root, [])

    def __traverse__(self, node, prefix):
        result = []
        for edge in node.out_edges:
            new_prefix = prefix.copy()
            if edge.value:
                new_prefix.append(edge.value)
            result.extend(self.__traverse__(edge.to_node, new_prefix))
        return result or [prefix]



def __find_index_of_first_diff__(seqs):
    i = 0
    cardinality = len(seqs)

    for i_items in itertools.zip_longest(*seqs):
        if i_items.count(i_items[0]) == cardinality:
            i += 1
        else:
            return i
