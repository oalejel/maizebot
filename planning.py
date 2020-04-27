from heapq import heappush, heappop, heapify
import cv2
from maze import Maze
import numpy as np
import skimage.measure
from collections import deque

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

class Planner():
    def __init__(self, maze):
        self.maze  = maze
        self.path = []
        self.scale = 2
        self.pooled_map = skimage.measure.block_reduce(self.maze.map, (self.scale, self.scale), np.max)
        self.hole_distance_grid = np.full(self.pooled_map.shape, np.inf)
        self.wall_distance_grid = np.full(self.pooled_map.shape, np.inf)
        self.create_distance_grid(self.hole_distance_grid, 2)
        self.create_distance_grid(self.wall_distance_grid, 1)


        # TODO: Maxpool map, store 
    # https://gist.github.com/jamiees2/5531924
    
    def astar(self, start_point, goal_point, map_copy):
    

        grid = self.pooled_map
        s = self.scale
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
            #if count%1000 ==0:
                #cv2.imshow("goal", map_copy)
                #cv2.waitKey(1)
            #Find the item in the open set with the lowest G + H score, remove the item from the open set

            current = heappop(open_heap)
            current.in_heap = False
            #Add it to the closed set
            current.visited = True
            #color it on the map
            map_copy[current.point[1], current.point[0]] = [0,0,255]
            # print("Current cost: ", current.G + current.H)
            #If it is the item we want, retrace the path and return it
            if current.point == goal.point:
                print("PATH FOUND")
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

                    ball_size = 5

                    h_dist = self.hole_distance_grid[node.point[1]][node.point[0]]
                    w_dist = self.wall_distance_grid[node.point[1]][node.point[0]]

                    if h_dist < ball_size or w_dist < ball_size:
                        continue

                    wall_affinity = 2
                    hole_repulsion = 20

                    node.H = (
                             manhattan(node, goal) + 
                             np.exp((1/(h_dist - ball_size)) * hole_repulsion)+ 
                             np.exp(w_dist * wall_affinity)
                             )
                    #Set the parent to our current item
                    node.parent = current
                    #Add it to the set
                    heappush(open_heap,  node)
                    node.in_heap = True
        #Throw an exception if there is no path
        raise ValueError('No Path Found')


    def create_distance_grid(self, grid, val):

        H, W = self.pooled_map.shape
        to_visit = deque()
        visited = np.zeros((H, W), dtype="bool")
        closest_obstacle = np.zeros((H, W, 2), dtype="uint16")

        for i in range(H):
            for j in range(W):
                if self.pooled_map[i][j] == val:
                    closest_obstacle[i][j][0] = i 
                    closest_obstacle[i][j][1] = j
                    grid[i][j] = 0
                    to_visit.append((i, j))
        
        explore_order = [(1,0), (-1, 0), (0,1), (0,-1)]

        while to_visit:
            y, x = to_visit.popleft()
            if visited[y][x]:
                continue
            visited[y][x] = True

            for ny, nx in explore_order:
                next_y = y + ny
                next_x = x + nx

                if next_y < 0 or next_x < 0 or next_y >= H or next_x >= W :
                    continue
                closest_y = closest_obstacle[y][x][0]
                closest_x = closest_obstacle[y][x][1]

                new_dist = np.sqrt((closest_y - next_y)**2 +
                                   (closest_x - next_x)**2)
                if new_dist < grid[next_y][next_x]:
                    closest_obstacle[next_y][next_x][0] = closest_obstacle[y][x][0]
                    closest_obstacle[next_y][next_x][1] = closest_obstacle[y][x][1]
                    grid[next_y][next_x] = new_dist
                to_visit.append((next_y, next_x))

        # cv2.imshow("distance", grid/100)
        # cv2.waitKey(0)



    def plan_path(self):
        
        map_copy = np.copy(self.pooled_map)*50


        start = (int(self.maze.ball_x/self.scale), int(self.maze.ball_y/self.scale))
        goal = (int(self.maze.goal_x/self.scale), int(self.maze.goal_y/self.scale))

        map_copy = cv2.cvtColor(map_copy, cv2.COLOR_GRAY2BGR) 
        cv2.circle(map_copy, start, 1, (255, 0, 0), -1)
        cv2.circle(map_copy, goal, 1, (0, 255, 0), -1)

        print("GOAL: ", goal)

        self.path = self.astar(start, goal, map_copy)
        return self.path

    def draw_path(self, use_imshow=True):
        if use_imshow:
            map_copy = np.copy(self.maze.map)*50
            map_copy = cv2.cvtColor(map_copy, cv2.COLOR_GRAY2BGR) 
            for x,y in self.path:
                map_copy[y,x] = [0,0,255]
            cv2.imshow("path", map_copy)
            cv2.waitKey(0)
        return self.path
    

    def is_valid_line(self, start_cell, goal_cell, tolerance):
        x1, y1 = start_cell
        x2, y2 = goal_cell

        x1 = x1 // self.scale
        x2 = x2 // self.scale
        y1 = y1 // self.scale
        y2 = y2 // self.scale

        theta = np.arctan2(y2-y1, x2-x1)

        dx = x2 - x1
        dy = y2 - y1

        error = -1

        inc_var = x1
        cond_var = y1
        inc_var_limit = x2
        inc = int(dx / np.fabs(dx)) if dx != 0 else 0
        cond_inc = int(dy/np.fabs(dy)) if dy != 0 else 0
        derror = np.fabs(dy/dx) if dx != 0 else 0

        if np.fabs(dx) < np.fabs(dy):
            inc_var = y1
            cond_var = x1
            inc_var_limit = y2
            inc = int(dy/np.fabs(dy)) if dy != 0 else 0
            cond_inc = int(dx/np.fabs(dx)) if dx != 0 else 0
            derror = 1/derror if derror != 0 else 0
        
        while np.abs(inc_var - inc_var_limit) > 0:
            hole_distance = self.hole_distance_grid[inc_var][cond_var] if np.fabs(dx) < np.fabs(dy) else self.hole_distance_grid[cond_var][inc_var]
            wall_distance = self.wall_distance_grid[inc_var][cond_var] if np.fabs(dx) < np.fabs(dy) else self.wall_distance_grid[cond_var][inc_var]
            if hole_distance < tolerance or wall_distance < tolerance:
                return False
            error += derror
            if error > 0:
                cond_var += cond_inc
                error += -1
            inc_var += inc
        return True

    def aggregate_path(self, tolerance=5):
        aggregated_path = []
        aggregated_path.append(self.path[0])
        for i in range(1, len(self.path)-1):
            if not self.is_valid_line(aggregated_path[-1], self.path[i], tolerance):
                aggregated_path.append(self.path[i])

        aggregated_path.append(self.path[-1])
        self.path = aggregated_path
        return aggregated_path


def main():
    img = cv2.imread("sample_frames/image7.png")
    # detect_corners(img)
    maze = Maze(img)
    maze.detect_ball(img, 1)
    planner = Planner(maze)
    print(planner.plan_path())
    planner.aggregate_path()
    planner.draw_path()
    

if __name__ == "__main__":
    main()
