import sys
from collections import defaultdict
import heapq  # 우선순위 큐 사용으로 더 효율적인 다익스트라 구현


class DynamicGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # 인접 리스트로 그래프 관리

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # 무방향 그래프일 경우

    def remove_node(self, node):
        if node in self.graph:
            # 해당 노드 제거
            del self.graph[node]
            # 다른 노드들의 연결도 제거
            for u in list(self.graph):
                self.graph[u] = [(v, w) for v, w in self.graph[u] if v != node]

    def dijkstra(self, start, end):
        distance = {node: sys.maxsize for node in self.graph}
        previous = {node: None for node in self.graph}
        distance[start] = 0

        priority_queue = [(0, start)]  # (거리, 노드)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # 현재 노드가 최단 거리로 이미 처리된 경우 스킵
            if current_distance > distance[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                new_distance = current_distance + weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        # 경로 추적
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return distance[end], path

    @classmethod
    def array_to_adjacency_list(cls, array_graph):
        dynamic_graph = cls()
        for i in range(len(array_graph)):
            for j in range(len(array_graph[i])):
                if array_graph[i][j] != 0:  # 0이 아닌 경우에만 간선 추가
                    dynamic_graph.add_edge(i, j, array_graph[i][j])
        return dynamic_graph

array_graph = [
#   0   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ,24
    [0, 0, 4, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#0
    [0, 0, 8, 0, 0, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],#1
    [4, 8, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#2
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],#3
    [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#4
    [6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],#5
    [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],#6
    [0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#7
    [0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],#8
    [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],#9
    [0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],#10
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],#11
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],#12
    [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#13
    [0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#14
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#15
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#16
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#17
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#18
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#19
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#20
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#21
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#22
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#23
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]#24



def main():
    # 배열을 리스트로 변환
    graph = DynamicGraph.array_to_adjacency_list(array_graph)

    # 최단 거리 및 경로 확인
    start_node = 8
    end_node = 0
    shortest_distance, path = graph.dijkstra(start_node, end_node)
    print(f"Shortest distance from node {start_node} to node {end_node} is {shortest_distance}")
    print(f"Path: {' -> '.join(map(str, path))}")

    # 노드 제거
    print("\nRemoving node 4...")
    graph.remove_node(4)

    # 노드 제거 후 다시 계산
    shortest_distance, path = graph.dijkstra(start_node, end_node)
    print(f"Shortest distance from node {start_node} to node {end_node} after removing node 4 is {shortest_distance}")
    print(f"Path: {' -> '.join(map(str, path))}")
    print(path[1])


if __name__ == "__main__":
    main()