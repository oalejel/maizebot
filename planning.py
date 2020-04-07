class Planner():
    def __init__(self, maze):
        self.maze  = maze

        # TODO: Maxpool map, store 

    class Node:
        def __init__(self, point):
            self.point = point
            self.parent = None
            self.H = 0
            self.G = 0
        def move_cost(self,other):
            # TODO: Add smoothing penalty
            return 0 if self.value == '.' else 1
    
    def children(point,grid):
        x,y = point.point
        links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
        return [link for link in links if link.value != '%']

    def manhattan(point,point2):
        return abs(point[0] - point2[0]) + abs(point[1] - point2[1])

    def aStar(start, goal, grid):
        
        start = Node((self.ball_x, self.ball_y))
        goal = self.maze.goal_x, self.maze.goal_y


        #The open and closed sets
        openset = [(0.0,start)]
        closedset = []
        #Current point is the starting point
        current = start
        #While the open set is not empty
        while openset:
            #Find the item in the open set with the lowest G + H score
            current_score, current = openset[0]
            #If it is the item we want, retrace the path and return it
            if current == goal:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            #Remove the item from the open set
            heappop(openset)
            #Add it to the closed set
            closedset.add((current_score, current))
            #Loop through the node's children/siblings
            for node in children(current,grid):
                #If it is already in the closed set, skip it
                if node in closedset:
                    continue
                #Otherwise if it is already in the open set
                if node in openset:
                    #Check if we beat the G score 
                    new_g = current.G + current.move_cost(node)
                    if node.G > new_g:
                        #If so, update the node to have a new parent
                        node.G = new_g
                        node.parent = current
                else:
                    #If it isn't in the open set, calculate the G and H score for the node
                    node.G = current.G + current.move_cost(node)
                    node.H = manhattan(node, goal)
                    #Set the parent to our current item
                    node.parent = current
                    #Add it to the set
                    openset.add(node)
        #Throw an exception if there is no path
        raise ValueError('No Path Found')

    def plan_path():

