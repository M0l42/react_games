from math import sqrt


class Node:
    def __init__(self, x, y, direction, cost, node=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.node = node
        self.node_list = list()
        self.cost = cost


class PathAlgorithms:
    def __init__(self, snake, apple):
        self.apple = apple
        self.snake = snake
        self.new_map = None
        self.init_map()
        self.load_map()

    def init_map(self):
        n = 30
        m = 30
        self.new_map = [0] * n
        for i in range(n):
            self.new_map[i] = [0] * m

    def load_map(self):
        index = 0
        for x, y in self.snake.body:
            if index < len(self.snake.body) - 1:
                self.new_map[x][y] = -1
            index += 1

    def find_path(self, nodes):
        pass

    def check_box(self, x, y, direction, snake_x, snake_y, nodes):
        pass

    def test(self):
        pass


class DijkstraAlgorithm(PathAlgorithms):
    def find_path(self, nodes):
        new_node = list()
        target_x, target_y = self.apple.x, self.apple.y
        snake_x, snake_y = self.snake.body[-1]
        new_node.append(self.check_box(nodes.x, nodes.y - 1, 3, snake_x, snake_y, nodes))
        new_node.append(self.check_box(nodes.x, nodes.y + 1, 2, snake_x, snake_y, nodes))
        new_node.append(self.check_box(nodes.x + 1, nodes.y, 1, snake_x, snake_y, nodes))
        new_node.append(self.check_box(nodes.x - 1, nodes.y, 0, snake_x, snake_y, nodes))
        for val in new_node:
            if val:
                nodes.node_list.append(val)
        for node in nodes.node_list:
            if node.x == target_x and target_y == node.y:
                self.new_map[node.x][node.y] = 42
                return node
        return None

    def check_box(self, x, y, direction, snake_x, snake_y, nodes):
        if 0 <= x < 30 and 0 <= y < 30:
            if x != snake_x or y != snake_y:
                if self.new_map[x][y] == 0:
                    node = Node(x, y, direction, nodes.cost + 1, nodes)
                    self.new_map[x][y] = node.cost
                    return node

    def test(self):
        target_not_found = True
        nodes = list()
        snake_x, snake_y = self.snake.body[-1]
        nodes.append([Node(snake_x, snake_y, 0, 0)])
        self.find_path(nodes[0][0])
        nodes.append(nodes[0][0].node_list)
        while target_not_found:
            nodes.append(list())
            for node in nodes[-2]:
                target = self.find_path(node)
                if target:
                    print("found !")
                    target_not_found = False
                    break
                else:
                    nodes[-1].extend(node.node_list)

        path = list()
        while True:
            path.append(target.direction)
            target = target.node
            if target == nodes[0][0]:
                break
        return path


class AStar(DijkstraAlgorithm):
    def check_box(self, x, y, direction, snake_x, snake_y, nodes):
        if 0 <= x < 30 and 0 <= y < 30:
            if x != snake_x or y != snake_y:
                if self.new_map[x][y] == 0:
                    cost = sqrt((x - self.apple.x) ** 2 + (y - self.apple.y) ** 2)
                    node = Node(x, y, direction, cost, nodes)
                    self.new_map[x][y] = node.cost
                    return node

    def nodes_sorting(self, nodes, result):
        if len(nodes):
            min_cost = nodes[0].cost
            closest_node = nodes[0]
            for node in nodes:
                if node.cost < min_cost:
                    min_cost = node.cost
                    closest_node = node
            result.append(closest_node)
            nodes.remove(closest_node)
            result = self.nodes_sorting(nodes, result)
        return result

    def test(self):
        nodes = list()
        snake_x, snake_y = self.snake.body[-1]
        initial_node = Node(snake_x, snake_y, 0, 0)
        nodes.append(initial_node)
        self.find_path(nodes[0])
        nodes.extend(nodes[0].node_list)
        while True:
            result = list()
            nodes = self.nodes_sorting(nodes, result)
            target = self.find_path(nodes[0])
            if target:
                print("found !")
                break
            else:
                nodes.extend(nodes[0].node_list)
                nodes.pop(0)

        path = list()
        while True:
            path.append(target.direction)
            target = target.node
            if target == initial_node:
                break
        return path
