import itertools

class Node:
    def __init__(self, node_type=None):
        self.type = node_type
        self.in_edges = []
        self.out_edges = []


class Edge:
    def __init__(self, value, from_node, to_node):
        self.value = value
        self.from_node = from_node
        self.to_node = to_node
        from_node.out_edges.append(self)
        to_node.in_edges.append(self)


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
                self.last_node = self.__add_phn__(pronunciations[0][i])

            prev_last_node = self.last_node
            self.last_node = Node()

            for pronunciation in pronunciations:
                node = prev_last_node
                for phn in pronunciation[i_diff_forward:i_diff_reverse]:
                    node = self.__add_phn__(phn, node)

                if len(pronunciation) - i_diff_forward >= -i_diff_reverse:
                    phn = pronunciation[i_diff_reverse]
                else:
                    phn = None

                self.__add_phn__(phn, node, next_node=self.last_node)


            for i in range(i_diff_reverse+1, 0):
                self.last_node = self.__add_phn__(pronunciations[0][i])
        else:
            for phn in pronunciations[0]:
                self.last_node = self.__add_phn__(phn)

        self.last_node.type = "<WORD>"


    def __add_phn__(self, phn, node=None, next_node=None):
        if not node:
            node = self.last_node
        if not next_node:
            next_node = Node()
        Edge(phn, from_node=node, to_node=next_node)
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

    
    def edges(self):
        for node in self:
            for edge in node.out_edges:
                yield edge


    def to_graphviz(self):
        import graphviz

        dot = graphviz.Digraph()
        for node in self:
            dot.node(str(id(node)), node.type or "")

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


    def triples(self):
        for edge in self.edges():
            if not edge.value:
                continue
            in_edges = self.__fetch_edges__(edge, "in") or [None]
            out_edges = self.__fetch_edges__(edge, "out") or [None]
            for triple in itertools.product(in_edges, [edge], out_edges):
                yield list(triple)


    def __fetch_edges__(self, edge, direction):
        node_type = direction == "in" and "from_node" or "to_node"
        node = getattr(edge, node_type)
        edges = getattr(node, direction + "_edges")

        result = []
        for edge in edges:
            if edge.value:
                result.append(edge)
            else:
                result.extend(self.__fetch_edges__(edge, direction))
        return result




def __find_index_of_first_diff__(seqs):
    i = 0
    cardinality = len(seqs)

    for i_items in itertools.zip_longest(*seqs):
        if i_items.count(i_items[0]) == cardinality:
            i += 1
        else:
            return i
