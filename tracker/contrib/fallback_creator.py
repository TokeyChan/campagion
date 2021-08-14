from string import ascii_lowercase, ascii_uppercase
from collections import defaultdict
import copy

LETTERS = list(ascii_lowercase + ascii_uppercase)

class Graph:
    def __init__(self):
        self._graph = defaultdict(set)

    def __str__(self):
        return str(self._graph)

    def add_connections(self, collections):
        """ must be a list of tuple-paires """
        for node1, node2 in collections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_all_paths(self, start, end):
        return self.dfs(start, end, [], [])
    
    def dfs(self, current_node, destination_node, path, all_paths):
        path.append(current_node)

        if current_node == destination_node:
            all_paths.append(copy.deepcopy(path))

        for connection in self._graph[current_node]:
            if connection not in path:
                p = self.dfs(connection, destination_node, path, all_paths)

        path.pop()
        
        if not path:
            return all_paths



class FallbackCreator:
    def __init__(self, workflow, task):
        self.workflow = workflow
        self.task = task
        self.fallback_task = task.fallback_task
        self.graph = Graph()

        self.dict = {}

    def create(self):
        self.create_dict()
        self.create_graph()
        paths = self.graph.find_all_paths(self.dict[self.fallback_task], self.dict[self.task])
        lines = self.find_lines(paths)
        tasks = self.create_tasks(paths)
        self.create_lines(lines, tasks)

        destination_char = paths[0][-1]

        for line in self.task.node.outgoing_lines.all():
            line.from_node = tasks[destination_char].node
            line.save()
        
        self.task.connect_to(tasks[paths[0][0]])

    def create_tasks(self, paths):
        return {k:t.copy() for k,t in self.find_tasks(paths).items()}

    def create_lines(self, lines, tasks):
        for line in lines:
            tasks[line[0]].connect_to(tasks[line[1]])

    def find_lines(self, paths):
        lines = [] #list of tuples
        
        for path in paths:
            for i in range(len(path) - 1):
                line = (path[i], path[i + 1])
                if line not in lines:
                    lines.append(line)

        return lines

    def find_tasks(self, paths):
        tasks = {}
        keys = list(self.dict.keys())
        values = list(self.dict.values())

        for path in paths:
            for node in path:
                if node not in tasks:
                    key = keys[values.index(node)]
                    tasks[node] = key

        return tasks

    def create_dict(self):
        i = 0
        for task in self.workflow.task_set.all():
            self.dict[task] = LETTERS[i]
            i += 1

    def create_graph(self):
        for task in self.workflow.task_set.all():
            for child in task.child_tasks():
                self.graph.add(self.dict[task], self.dict[child])