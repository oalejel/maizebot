from heapq import heappush, heappop, heapify
import cv2
from maze import Maze
import numpy as np
import skimage.measure

class Node:
        def __init__(self, point):
            self.point = point
            self.parent = None
            self.visited = False
            self.in_heap = False
            self.G = 0
            self.H = 0.0
        def __lt__(self, other):
            return self.G + self.H < other.G + other.H
        def move_cost(self,other):
            return 1
            # TODO: Add smoothing penalty
            return 0 if self.value == '.' else 1

def children(node, grid, node_dict):
        x,y = node.point

        neighbors_index = []
        if x > 0:
            neighbors_index.append((x-1, y))
        if y > 0:
            neighbors_index.append((x, y-1))
        if x < grid.shape[1] - 1:
            neighbors_index.append((x+1,y))
        if y < grid.shape[0] - 1:
            neighbors_index.append((x,y+1))

        neighbors_nodes = []
        for p in neighbors_index:
            # if cell is a hole or a wall
            if grid[p[1]][p[0]] != 0:
                continue

            if p not in node_dict:
                node_dict[p] = Node(p)  

            neighbors_nodes.append(node_dict[p])

        return neighbors_nodes

def manhattan(node1,node2):
    return abs(node1.point[0] - node2.point[0]) + abs(node1.point[1] - node2.point[1])

def astar(start_point, goal_point, grid, map_copy, s):
    

    # start = Node())
    # goal = Node(self.maze.goal_x, self.maze.goal_y)

    node_dict = {}
    start = Node(start_point)
    goal = Node(goal_point)

    node_dict[start_point] = start
    node_dict[goal_point] = goal

    #The open and closed sets
    open_heap = []
    heappush(open_heap, start)
    start.in_heap = True
    # closed_dict = {}
    #Current point is the starting point
    current = start
    #While the open set is not empty

    count = 0
    while open_heap:
        count += 1
        if count%1000 ==0:
            print(count)
            cv2.imshow("goal", map_copy)
            cv2.waitKey(1)
        #Find the item in the open set with the lowest G + H score, remove the item from the open set

        current = heappop(open_heap)
        current.in_heap = False
        #Add it to the closed set
        current.visited = True
        #color it on the map
        map_copy[current.point[1], current.point[0]] = [0,0,255]
        #If it is the item we want, retrace the path and return it
        if current.point == goal.point:
            path = []
            while current.parent:
                path.append((current.point[0]*s, current.point[1]*s))
                current = current.parent
            path.append((current.point[0]*s, current.point[1]*s))
            return path[::-1]
        
        
        #Loop through the node's children/siblings
        for node in children(current,grid, node_dict):
            #If it is already in the closed set, skip it
            if node.visited:
                continue
            #Otherwise if it is already in the open set
            if node.in_heap:
                #Check if we beat the G score 
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
                    heapify(open_heap)
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                # node.H = manhattan(node, goal)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                heappush(open_heap,  node)
                node.in_heap = True
    #Throw an exception if there is no path
    raise ValueError('No Path Found')

class Planner():
    def __init__(self, maze):
        self.maze  = maze
        self.path = []

        # TODO: Maxpool map, store 
    # https://gist.github.com/jamiees2/5531924
    


    def plan_path(self):
        s = 2
        pooled_map = skimage.measure.block_reduce(self.maze.map, (s, s), np.max)
        map_copy = np.copy(pooled_map)*50


        start = (int(self.maze.ball_x/s), int(self.maze.ball_y/s))
        goal = (int(self.maze.goal_x/s), int(self.maze.goal_y/s))

        map_copy = cv2.cvtColor(map_copy, cv2.COLOR_GRAY2BGR) 
        cv2.circle(map_copy, start, 5, (255, 0, 0), -1)
        cv2.circle(map_copy, goal, 5, (0, 255, 0), -1)


        self.path = astar(start, goal, pooled_map, map_copy, s)
        return self.path

    def draw_path(self):
        map_copy = np.copy(self.maze.map)*50
        map_copy = cv2.cvtColor(map_copy, cv2.COLOR_GRAY2BGR) 
        for x,y in self.path:
            map_copy[y,x] = [0,0,255]
        cv2.imshow("path", map_copy)
        cv2.waitKey(0)
        



def main():
    img = cv2.imread("sample_frames/image1.png")
    # detect_corners(img)
    maze = Maze(img)
    maze.detect_ball(img, 1)
    planner = Planner(maze)
    print(planner.plan_path())
    planner.draw_path()
    

if __name__ == "__main__":
    main()
