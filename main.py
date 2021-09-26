from re import findall


class Graph(object):
    MAX_WEIGHT = 100

    def __init__(self, data, vertexes):
        self.all_weight = []
        self.data = data
        self.size = len(self.data)
        self.positive = self.is_positive()
        self.check()
        self.vertexes = findall(r'\d+', vertexes)

    def check(self):  # проверка на заполненность матрицы
        for i in range(len(self.data)):
            if len(self.data) != len(self.data[i]):
                raise Exception('input matrix is not correct')

    def is_positive(self):  # проверка наличие отрицательных элементов в матрице
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = int(self.data[i][j])
                if self.data[i][j] < 0:
                    return False
        return True

    def connections_from(self, minimum):
        return [(self.vertexes[col_num], self.data[minimum][col_num]) for col_num in range(self.size) if
                self.data[minimum][col_num] != 0]

    # def dijkstra(self, start_point):
    #     distance = [None] * self.size
    #     for i in range(len(distance)):
    #         distance[i] = [float("inf")]
    #         distance[i].append([self.vertexes[start_point]])
    #     distance[start_point][0] = 0
    #     queue = [i for i in range(self.size)]
    #     seen = set()
    #     while len(queue) > 0:
    #         min_distance = float("inf")
    #         for n in queue:
    #             if distance[n][0] < min_distance and n not in seen:
    #                 min_node = n
    #         queue.remove(min_node)
    #         seen.add(min_node)
    #         connections = self.connections_from(min_node)
    #         for (vertex, weight) in connections:
    #             total_distance = weight + min_distance
    #             if total_distance < distance[int(vertex)][0]:
    #                 distance[int(vertex)][0] = total_distance
    #                 distance[int(vertex)][1] = list(distance[min_node][1])
    #                 distance[int(vertex)][1].append(vertex)
    #     return distance
    def dijkstra(self, start_point):            #надо понять :(
        dist = [None] * self.size
        for i in range(len(dist)):
            dist[i] = [float("inf")]
            dist[i].append([self.vertexes[start_point]])
        dist[start_point][0] = 0
        queue = [i for i in range(self.size)]
        seen = set()
        while len(queue) > 0:
            min_dist = float("inf")
            min_node = None
            for n in queue:
                if dist[n][0] < min_dist and n not in seen:
                    min_dist = dist[n][0]
                    min_node = n
            queue.remove(min_node)
            seen.add(min_node)
            connections = self.connections_from(min_node)
            for (mount, weight) in connections:
                tot_dist = weight + min_dist
                if tot_dist < dist[int(mount)][0]:
                    dist[int(mount)][0] = tot_dist
                    dist[int(mount)][1] = list(dist[min_node][1])
                    dist[int(mount)][1].append(mount)
        return dist

    def shortest_ways(self, certain=False):  # сама функция нахождения путей
        if type(certain) == int:
            if self.positive:
                self.all_weight.append(self.dijkstra(certain))  # вызов функции Дийкстры
                return self.all_weight
            else:
                self.originalFloydWarshall()
        else:
            if self.positive:
                for i in self.vertexes:
                    self.all_weight.append(self.dijkstra(int(i)))  # вызов функции Дийкстры
                return self.all_weight
            else:
                return self.originalFloydWarshall()

    def originalFloydWarshall(self):
        self.vertexes = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.vertexes[i][j] = j
        for i in range(self.size):
            self.data[i][i] = 0
            self.vertexes[i][i] = i
        for k in range(self.size):
            for i in range(self.size):
                for j in range(self.size):
                    if int(self.data[i][j]) > int(self.data[i][k]) + int(self.data[k][j]):
                        self.data[i][j] = int(self.data[i][k]) + int(self.data[k][j])
                        self.vertexes[i][j] = self.vertexes[i][k]
        dist = [[] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                dist[i].append(self.path(i, j))
        return dist

    def path(self, u, v):
        if self.vertexes[u][v] is None:
            return
        path = [0, [str(u)]]
        while u != v:
            u = self.vertexes[u][v]
            path[0] += int(self.data[u][v])
            path[1].append(str(u))
        return path


def main():
    with open('input.txt', 'r', encoding='utf-8') as matrix:  # открытие файла и создание экземпляра класса
        first_matrix = []
        second_matrix = []
        for stroke in matrix:
            first_matrix.append(stroke)
        for i in range(1, len(first_matrix)):
            second_matrix.append(findall(r'-?\d+', first_matrix[i][2:] if i < 10 else first_matrix[i][3:]))
        graph = Graph(second_matrix, first_matrix[0])

    variable = graph.shortest_ways()

    with open('output.txt', 'w', encoding='utf-8') as m:  # запись результата
        for i in range(len(variable)):
            for j in range(len(variable[i])):
                way = ' - '.join(variable[i][j][1])
                m.write(f'Из {variable[i][1][1][0]} в {variable[i][j][-1][-1]}; длина: {variable[i][j][0]}; путь: {way}\n')
            m.write("\n")

if __name__ == '__main__':
    main()
