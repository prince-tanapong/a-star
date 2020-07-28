class Node(object):
    def __init__(self, label, h, parent=None, g=0):
        self.label = label
        self.h = int(h)
        self.parent = parent
        self.g = int(g)

        self.expanded = True

    @property
    def f(self):
        return self.g + self.h

    def __repr__(self):
        str_format = "{}.{}" if self.expanded else "({}.{})"
        return str_format.format(self.label, self.f)

    def __eq__(self, other):
        if not other:
            return False
        return self.label == other.label


class Astar(object):
    def __init__(self, file_name, start_node):
        # setup graph, start_node, goal_node
        self.graph, goal = self.construct_graph_and_goal(file_name)
        self.start_node = self.create_node(start_node)
        self.goal_node = self.create_node(goal)

        self.expanded_list = []
        self.priority_list = []

    def construct_graph_and_goal(self, file_name):
        with open(file_name) as open_file:
            lines = open_file.readlines()
            goal = None
            graph = []
            for count, line in enumerate(lines):
                line_value = line.strip()
                if count == 0:
                    goal = line_value
                else:
                    graph.append(line_value.split())
        return graph, goal

    def create_node(self, label, parent=None, g=0):
        for each in self.graph:
            if each[0] == label:
                return Node(label, each[1], parent=parent, g=g)

    def find_children(self, node):
        for each in self.graph:
            if node.label == each[0]:
                return each[2:]
        return []

    def valid_to_expand(self, node):
        same_expaneded_node = [each for each in self.expanded_list if each == node and each.expanded]
        if not same_expaneded_node:
            return True

        min_f = min([each.f for each in same_expaneded_node])
        if node.f >= min_f:
            return False
        return True

    def find_path(self, node):
        path = [node]
        while(True):
            node = node.parent
            if node is None:
                break
            path.append(node)
        path.reverse()
        return path

    def run(self):
        self.priority_list.append(self.start_node)

        count = 0
        while(len(self.priority_list) > 0):
            count += 1
            print()
            print("\tInteration {}".format(count))

            self.priority_list = sorted(self.priority_list, key=lambda x: x.f)
            print('priority list: ', self.priority_list)

            expanding_node = self.priority_list.pop(0)
            expanded_node = None

            if self.valid_to_expand(expanding_node):
                print('expanding node {}, valid.'.format(expanding_node))
                expanded_node = expanding_node
            else:
                print('expanding node {}, invalid, skip.'.format(expanding_node))
                expanding_node.expanded = False

            self.expanded_list.append(expanding_node)
            print('expanded list: ', self.expanded_list)

            if expanded_node == self.goal_node:
                print("Expanded goal {}, stop iteration".format(self.goal_node.label))
                break

            if expanded_node:
                # find children from graph
                children_node = self.find_children(expanded_node)
                for index in range(0, len(children_node), 2):
                    each_child = children_node[index: index + 2]
                    child_node = self.create_node(each_child[0], expanded_node, expanded_node.g + int(each_child[1]))

                    if not expanding_node.parent or expanding_node.parent != child_node:
                        self.priority_list.append(child_node)

        last_expaneded = self.expanded_list[-1]
        print()
        print("======== Summary ========")
        if last_expaneded == self.goal_node:
            path = self.find_path(last_expaneded)
            print("Expand: ", " ".join(list(map(lambda x: str(x), self.expanded_list))))
            print('Path: ', ' '.join(list(map(lambda x: x.label, path))))
        else:
            print("No solution found from {} to {}".format(self.start_node, self.goal_node))


if __name__ == "__main__":
    file_name = input("Please Enter your file name(default: in_aStar.txt): ") or 'in_aStar.txt'
    start_node = input("What is your start node? ")
    # print()
    # aa = list('ABCDEFGHIJKLMNOP')
    # for cha in aa:
    #     print('Start Node:', cha)
    #     start_node = cha
    #     Astar(file_name, start_node).run()
    #     print()

    Astar(file_name, start_node).run()
