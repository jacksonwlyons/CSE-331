"""
CSE 331 FS22 (Onsay)
Graph Project
Jackson Lyons
"""

import math
import queue
import time
import csv
from typing import TypeVar, Tuple, List, Set, Dict

import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')  # Graph Class Instance


class Vertex:
    """
    Class representing a Vertex object within a Graph.
    """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, id_init: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex.
        :param id_init: [str] A unique string identifier used for hashing the vertex.
        :param x: [float] The x coordinate of this vertex (used in a_star).
        :param y: [float] The y coordinate of this vertex (used in a_star).
        :return: None.
        """
        self.id = id_init
        self.adj = {}  # dictionary {id : weight} of outgoing edges
        self.visited = False  # boolean flag used in search algorithms
        self.x, self.y = x, y  # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY.
        Equality operator for Graph Vertex class.
        :param other: [Vertex] vertex to compare.
        :return: [bool] True if vertices are equal, else False.
        """
        if self.id != other.id:
            return False
        if self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        if self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        if self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        if set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Constructs string representation of Vertex object.
        :return: [str] string representation of Vertex object.
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]
        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    __str__ = __repr__

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set. Used in unit tests.
        :return: [int] Hash value of Vertex.
        """
        return hash(self.id)

    # ============== Modify Vertex Methods Below ==============#

    def deg(self) -> int:
        """
        Returns the number of outgoing edges from this vertex;
        i.e., the outgoing degree of this vertex
        :return: integer representing number of outgoing edges
        """
        return len(self.adj)

    def get_outgoing_edges(self) -> Set[Tuple[str, float]]:
        """
        This function will return a set of tuples representing outgoing edges from this vertex
        :return:  set of tuples representing outgoing edges from this vertex.
         If the vertex has no outgoing edges, it will return an empty set
        """
        outgoing_edges = set()
        for id, weight in self.adj.items():
            outgoing_edges.add((id, weight))
        return outgoing_edges


    def euclidean_dist(self, other: Vertex) -> float:
        """
        This function returns the euclidean distance between this vertex and vertex other
        :param other: other vertex to compute distance between
        :return: float representing euclidean distance between self and other.
        """
        d = math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        return d

    def taxicab_dist(self, other: Vertex) -> float:
        """
        This function returns the taxicab distance between this vertex and vertex other
        :param other: other vertex to compute distance between
        :return float representing taxicab distance between self and other
        """
        d = abs(other.x - self.x) + abs(other.y - self.y)
        return d


class Graph:
    """
    Class implementing the Graph ADT using an Adjacency Map structure.
    """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csvf: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance.
        :param plt_show: [bool] If true, render plot when plot() is called; else, ignore plot().
        :param matrix: [Matrix] Optional matrix parameter used for fast construction.
        :param csvf: [str] Optional filepath to a csv containing a matrix.
        :return: None.
        """
        matrix = matrix if matrix else np.loadtxt(csvf, delimiter=',', dtype=str).tolist() \
            if csvf else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)

    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class.
        :param other: [Graph] Another graph to compare.
        :return: [bool] True if graphs are equal, else False.
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        for vertex_id, vertex in self.vertices.items():
            other_vertex = other.get_vertex_by_id(vertex_id)
            if other_vertex is None:
                print(f"Vertices not equal: '{vertex_id}' not in other graph")
                return False

            adj_set = set(vertex.adj.items())
            other_adj_set = set(other_vertex.adj.items())

            if not adj_set == other_adj_set:
                print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                print(f"Adjacency symmetric difference = "
                      f"{str(adj_set.symmetric_difference(other_adj_set))}")
                return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        Constructs string representation of graph.
        :return: [str] String representation of graph.
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    __str__ = __repr__

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib.
        :return: None.
        """
        if self.plot_show:
            import matplotlib.cm as cm
            import matplotlib.patches as patches
            import matplotlib.pyplot as plt

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_all_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_all_edges())
            max_weight = max([edge[2] for edge in self.get_all_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_all_edges()):
                origin = self.get_vertex_by_id(edge[0])
                destination = self.get_vertex_by_id(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_all_vertices()])
            y = np.array([vertex.y for vertex in self.get_all_vertices()])
            labels = np.array([vertex.id for vertex in self.get_all_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_all_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03 * max(x), y[j] - 0.03 * max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    def add_to_graph(self, begin_id: str, end_id: str = None, weight: float = 1) -> None:
        """
        Adds to graph: creates start vertex if necessary,
        an edge if specified,
        and a destination vertex if necessary to create said edge
        If edge already exists, update the weight.
        :param begin_id: [str] unique string id of starting vertex
        :param end_id: [str] unique string id of ending vertex
        :param weight: [float] weight associated with edge from start -> dest
        :return: None
        """
        if self.vertices.get(begin_id) is None:
            self.vertices[begin_id] = Vertex(begin_id)
            self.size += 1
        if end_id is not None:
            if self.vertices.get(end_id) is None:
                self.vertices[end_id] = Vertex(end_id)
                self.size += 1
            self.vertices.get(begin_id).adj[end_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        Given an adjacency matrix, construct a graph
        matrix[i][j] will be the weight of an edge between the vertex_ids
        stored at matrix[i][0] and matrix[0][j]
        Add all vertices referenced in the adjacency matrix, but only add an
        edge if matrix[i][j] is not None
        Guaranteed that matrix will be square
        If matrix is nonempty, matrix[0][0] will be None
        :param matrix: [Matrix] an n x n square matrix (list of lists) representing Graph
        :return: None
        """
        for i in range(1, len(matrix)):  # add all vertices to begin with
            self.add_to_graph(matrix[i][0])
        for i in range(1, len(matrix)):  # go back through and add all edges
            for j in range(1, len(matrix)):
                if matrix[i][j] is not None:
                    self.add_to_graph(matrix[i][0], matrix[j][0], matrix[i][j])

    def graph2matrix(self) -> Matrix:
        """
        Given a graph, creates an adjacency matrix of the type described in construct_from_matrix.
        :return: [Matrix] representing graph.
        """
        matrix = [[None] + list(self.vertices)]
        for v_id, outgoing in self.vertices.items():
            matrix.append([v_id] + [outgoing.adj.get(v) for v in self.vertices])
        return matrix if self.size else None

    def graph2csv(self, filepath: str) -> None:
        """
        Given a (non-empty) graph, creates a csv file containing data necessary to reconstruct.
        :param filepath: [str] location to save CSV.
        :return: None.
        """
        if self.size == 0:
            return

        with open(filepath, 'w+') as graph_csv:
            csv.writer(graph_csv, delimiter=',').writerows(self.graph2matrix())

    # ============== Modify Graph Methods Below ==============#

    def unvisit_vertices(self) -> None:
        """
        Resets visited flags to False of all vertices within the graph
        :return: None
        """
        for vertex in self.vertices.values():
            vertex.visited = False

    def get_vertex_by_id(self, v_id: str) -> Vertex:
        """
        This function returns the Vertex object with id v_id
        if it exists in the graph. Otherwise, it will return None
        :param v_id: vertex id of vertex object to return
        :return: Vertex object corresponding to that id. Or None if the v_id does not exist.
        """
        if v_id in self.vertices:
            return self.vertices[v_id]
        else:
            return None

    def get_all_vertices(self) -> Set[Vertex]:
        """
        This function returns a set of all Vertex objects held in the graph
        :return: set of all vertex objects in graph.
        """
        vertex_objs = set()
        for vertex in self.vertices.values():
            vertex_objs.add(vertex)
        return vertex_objs

    def get_edge_by_ids(self, begin_id: str, end_id: str) -> Tuple[str, str, float]:
        """
        This function Returns the edge connecting the vertex with id begin_id
        to the vertex with id end_id in a tuple of the form (begin_id, end_id, weight)
        :param begin_id: unique string id of the starting vertex
        :param end_id: unique string id of the destination vertex
        :return: Tuple of the form (begin_id, end_id, weight)
        """
        # check if both vertices exist in graph
        if begin_id in self.vertices and end_id in self.vertices:
            begin_vertex = self.get_vertex_by_id(begin_id)
            # check if edge exists between two vertices
            if end_id in begin_vertex.adj:
                weight = begin_vertex.adj[end_id]
                return (begin_id, end_id, weight)
        return None

    def get_all_edges(self) -> Set[Tuple[str, str, float]]:
        """
        This function returns a set of tuples representing all edges within the graph
        :return: set of tuples (begin_id, end_id, weight) representing all edges within the graph
        """
        edges = set()
        # iterate through vertices in graph
        for begin_id in self.vertices:
            begin_vertex = self.vertices[begin_id]
            # iterate through outgoing edges from each vertex
            for end_id, weight in begin_vertex.adj.items():
                edges.add((begin_id, end_id, weight))
        return edges

    def _build_path(self, back_edges: Dict[str, str], begin_id: str, end_id: str) \
            -> Tuple[List[str], float]:
        """
        This function reconstructs the path from start_id to end_id and computes the total distance
        :param back_edges: dictionary of back-edges (a mapping of vertex id to predecessor vertex id)
        :param begin_id: unique string id of the starting vertex
        :param end_id: unique string id of the destination vertex
        :return: Returns tuple of the form ([path], distance)
        """
        path_weight = 0
        path = []
        if end_id in back_edges:
            # build list from end to start and then reverse it at the end
            path.append(end_id)
            walk = end_id
            while walk is not begin_id:
                predecessor = back_edges[walk]
                weight = self.get_edge_by_ids(predecessor, walk)[-1]
                path.append(predecessor)
                path_weight += weight
                walk = predecessor
            path.reverse()
        return (path, path_weight)

    def bfs(self, begin_id: str, end_id: str) -> Tuple[List[str], float]:
        """
        Perform a breadth-first search beginning at vertex with id
        begin_id and terminating at vertex with id end_id
        :param begin_id: unique string id of the starting vertex
        :param end_id: unique string id of the destination vertex
        :return: Returns tuple of the form ([path], distance)
        """

        back_edges = {}
        q = queue.SimpleQueue()
        # check for graph with no edges
        edges = self.get_all_edges()
        if len(edges) == 0:
            return ([], 0)
        # reset all visited flags
        self.unvisit_vertices()
        # mark beginning vertex as visited and push it onto queue
        self.vertices[begin_id].visited = True
        q.put(begin_id)
        while not q.empty():
            next_id = q.get()
            next = self.get_vertex_by_id(next_id)
            if next_id == end_id:
                return self._build_path(back_edges, begin_id, end_id)
            for u_id in next.adj.keys():  # iterate through adjacent vertices
                u = self.get_vertex_by_id(u_id)
                if u.visited == False:
                    u.visited = True
                    q.put(u_id)
                    # add (vertex, parent) to back_edges
                    back_edges[u_id] = next_id
        return ([], 0)


    def dfs(self, begin_id: str, end_id: str) -> Tuple[List[str], float]:
        """
        Wrapper function for dfs_inner
        :param begin_id: unique string id of the starting vertex
        :param end_id: unique string id of the destination vertex
        :return: Returns tuple of the form ([path], distance)
        """

        def dfs_inner(current_id: str, end_id: str, path: List[str]) -> Tuple[List[str], float]:
            """
            Performs the recursive work of depth-first search by searching
            for a path from vertex with id current_id to vertex with id end_id
            :param current_id: unique string id of the starting vertex
            :param end_id: unique string id of the destination vertex
            :param path: list where each vertex will be added in dfs order
            :return: tuple of the form ([path], distance)
            """
            curr = self.get_vertex_by_id(current_id)
            curr.visited = True
            if current_id == end_id:  # reached end
                return [end_id], 0
            for next_id, weight in curr.adj.items():  # for every outgoing edge from current
                next = self.get_vertex_by_id(next_id)
                if next.visited == False:  # if adj vertex has not been visited
                    path, distance = dfs_inner(next_id, end_id, path)  # recurse with that adj vertex
                    if path:
                        path.append(current_id)
                        return path, distance + weight
            return (path, 0)

        edges = self.get_all_edges()
        if len(edges) == 0:
            return ([], 0)

        # take care of invalid cases
        if self.get_vertex_by_id(begin_id) is None or self.get_vertex_by_id(end_id) is None:
            return ([], 0)
        reversed_dfs, distance = dfs_inner(begin_id, end_id, [])
        reversed_dfs.reverse()
        return (reversed_dfs, distance)


    def topological_sort(self) -> List[str]:
        """
        Performs topological sort on the graph, returning a possible
        topological ordering as a list of vertex ids
        :return: sorted list of vertex ids
        """

        def topological_sort_inner(current_id: str, topo: List[str]) -> None:
            """
            Inner recursive function for topological sort
            :param current_id: unique string id current vertex
            :param topo: list of vertex ids in topological ordering
            """
            curr = self.get_vertex_by_id(current_id)
            curr.visited = True
            for adj_id in curr.adj.keys():
                adj = self.get_vertex_by_id(adj_id)
                if adj.visited == False:
                    topological_sort_inner(adj_id, topo)

            topo.append(current_id)

        # check for graph with no vertices
        vertices = self.get_all_vertices()
        if len(vertices) == 0:
            return []
        self.unvisit_vertices()
        topo = []
        for v_id, v in self.vertices.items():
            if v.visited == False:
                topological_sort_inner(v_id, topo)

        topo.reverse()
        return topo

    def friends_recommender(self, current_id: str) -> List[str]:
        """
        Given an id of vertex in graph, determine whether recommended friend of given id
        :param current_id: str Given current id of vertex to recommend a friend
        :return: List of name of recommend vertex sorted by friend score
        """
        friends = {}    # {friend:distance}
        if current_id == "":
            return []
        # reset all visited flags
        self.unvisit_vertices()
        level = [current_id]
        curr = self.get_vertex_by_id(current_id)
        curr.visited = True
        my_friends = list(curr.adj.keys())  # to compare for mutual friends
        distance = 0

        while level:
            next_lvl = []
            for u_id in level:
                u = self.get_vertex_by_id(u_id)
                for next_id in u.adj.keys():    # iterate through adjacent vertices
                    next = self.get_vertex_by_id(next_id)
                    if next.visited == False:
                        next.visited = True
                        next_lvl.append(next_id)
                        friends[next_id] = distance   # add friend to friends
                        mutual_count = 0
                        for adj in next.adj.keys():  # check for mutual friends
                            if adj in my_friends:
                                mutual_count += 1
                        if mutual_count >= 2:
                            friends[next_id] -= 1
            level = next_lvl
            distance += 1

        friends_list = sorted(friends.items(), key=lambda x: (x[1], x[0]))   # first sort by distance then by friend name
        friends_final = []
        for friend, d in friends_list:
            if friend not in my_friends:
                friends_final.append(friend)
        return friends_final


