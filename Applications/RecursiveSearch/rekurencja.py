import math

class Element:
    def __init__(self, pos:tuple) -> None:
        self.Value = 0
        self.Weight = 0
        self.Neighbours = []
        self.Position = pos
        self.Visited = False

class Graph:
    def __init__(self, m) -> None:
        self.Elements = []
        self.Matrix = m
        self.Path = []

    def create_graph(self) -> None:
        def get_neighbors(pos:tuple, size:tuple) -> list:
            x,y = pos
            points = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            res = []
            for p in points:
                if p[0] >= 0 and p[0]<size[0] and p[1] >= 0 and p[1]<size[1] and self.Matrix[p[0]][p[1]] == 0: res.append(p)
            return res
        size = (len(self.Matrix), len(self.Matrix[0]))
        for x in range(size[0]):
            temp = []
            for y in range(size[1]):temp.append(Element((x,y)))
            self.Elements.append(temp)
        for x in range(size[0]):
            for y in range(size[1]):
                if self.Matrix[x][y] == 1: continue
                e = self.Elements[x][y]
                nei = get_neighbors((x,y), size)
                for n in nei:
                    e.Neighbours.append(self.Elements[n[0]][n[1]])

    def search(self, start : tuple, end: tuple):
        def compute_distanse(A,B): return math.sqrt(math.pow(A[0]-B[0],2)+math.pow(A[1]-B[1],2))

        def search_algorithm(step, element:Element, end:Element):
            print("Krok:\t{0}\tPos:\t{1}".format(step,element.Position))
            element.Visited = True
            if not element in self.Path: self.Path.append(element)
            if element == end: return self.Path
            
            not_visited = []
            values = []
            not_visited_sorted = []
            for nei in element.Neighbours:
                print("{0}\t=>\t{1}".format(nei.Position, nei.Visited))
                if nei.Visited == False:
                    nei.Value = compute_distanse(nei.Position, end.Position)
                    values.append(nei.Value)
                    not_visited.append(nei)
            while len(not_visited) > 0:
                index = values.index(min(values))
                not_visited_sorted.append(not_visited[index])
                not_visited.pop(index)
                values.pop(index)

            if len(not_visited_sorted ) > 0:
                for nei in not_visited_sorted : 
                    return search_algorithm(step+1, nei, end)
            else:
                if len(self.Path)>0: self.Path.pop()
                if len(self.Path)>0: 
                    return search_algorithm(step+1, self.Path[-1], end)
                return self.Path

        start_element = self.Elements[start[0]][start[1]]
        end_element = self.Elements[end[0]][end[1]]
        return search_algorithm(0,start_element, end_element)



if __name__ == "__main__":
    m = [
[0,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,1,0],
[1,1,1,0,0,0,0,1,0,0],
[0,0,0,0,0,0,1,0,0,0],
[0,0,0,0,0,1,0,0,0,0],
[0,0,0,0,1,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0],
    ]
    graph = Graph(m)
    graph.create_graph()
    res = graph.search((0,0),(9,9))
    print("Path:")
    for i in res:
        print(i.Position)