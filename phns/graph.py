class Node:
    def __init__(self, node_type):
        self.node_type = node_type
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
        else:
            pronunciation = pronunciations[0]
            p_len = len(pronunciation)
            for i in range(p_len):
                if i == p_len - 1:
                    next_node = Node("<WORD>")
                else:
                    next_node = Node("<PHN>")

                phn = pronunciation[i]
                new_edge = Edge(phn, to_node=next_node)

                self.last_node.out_edges.append(new_edge)
                self.last_node = next_node
