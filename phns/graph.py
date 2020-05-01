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

        return self


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
        result = []
        [result.append(it) for it in self.__traverse__(self.root, []) if it not in result]
        return result


    def __traverse__(self, node, prefix):
        result = []
        for edge in node.out_edges:
            new_prefix = prefix.copy()
            if edge.value:
                new_prefix.append(edge.value)
            result.extend(self.__traverse__(edge.to_node, new_prefix))
        return result or [prefix]


    def triples(self):
        result = []
        for edge in self.edges():
            if not edge.value:
                continue
            result += self.__fetch_triples__(edge)
        return result


    def __fetch_triples__(self, edge, in_edge=None, out_edge=None):
        if not edge.value:
            result = []
            if in_edge:
                for next_edge in edge.to_node.out_edges:
                    result += self.__fetch_triples__(next_edge, in_edge=in_edge)

            elif out_edge:
                for next_edge in edge.from_node.in_edges:
                    result += self.__fetch_triples__(next_edge, out_edge=out_edge)

            else:
                raise
            
            return result

        else:

            if in_edge and in_edge.value:
                in_edges = [in_edge]
            else:
                in_edges = self.__fetch_edges__(in_edge or edge, "in") or [None]

            if out_edge and out_edge.value:
                out_edges = [out_edge]
            else:
                out_edges = self.__fetch_edges__(out_edge or edge, "out") or [None]

            return [list(triple) for triple in itertools.product(in_edges, [edge], out_edges)]
    

    def __fetch_new_triples__(self, new_edge, in_edge=True, out_edge=True):
        result = []
        if new_edge.value:
            result += self.__fetch_triples__(new_edge)

        if out_edge:
            for out_edge in new_edge.to_node.out_edges:
                result += self.__fetch_triples__(out_edge, in_edge=new_edge)

        if in_edge:
            for in_edge in new_edge.from_node.in_edges:
                result += self.__fetch_triples__(in_edge, out_edge=new_edge)

        return result


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


    def create_edges(self, from_node, to_node, first_phn, second_phn=None):
        if first_phn == second_phn:
            second_phn = None

        for edge in from_node.out_edges:
            if edge.value == first_phn:
                if not second_phn:
                    if edge.to_node == to_node:
                        return []
                else:
                    for next_edge in edge.to_node.out_edges:
                        if next_edge.value == second_phn and next_edge.to_node == to_node:
                            return []

        if second_phn:
            new_node = Node()
            edge1 = Edge(first_phn, from_node, new_node)
            edge2 = Edge(second_phn, new_node, to_node)
            return self.__fetch_new_triples__(edge1, out_edge=False) + self.__fetch_new_triples__(edge2, in_edge=False)
        else:
            edge = Edge(first_phn, from_node, to_node)
            return self.__fetch_new_triples__(edge)



def __find_index_of_first_diff__(seqs):
    i = 0
    cardinality = len(seqs)

    for i_items in itertools.zip_longest(*seqs):
        if i_items.count(i_items[0]) == cardinality:
            i += 1
        else:
            return i
