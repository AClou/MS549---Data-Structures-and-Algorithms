class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def contains(self, point):
        #check whether a point is within this rectangle
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def distance_sq_to_point(self, point):
        #Uses the squared distance to find the nearest point to this rectangle
        dx = max(0, self.x - point.x, point.x - (self.x + self.width))
        dy = max(0, self.y - point.y, point.y - (self.y + self.height))
        return dx*dx + dy*dy

class QuadtreeNode:
    #initialize QuadtreeNode class with 8 attributes
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity 
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        #divides main (parent) node into 4 quadrants (smaller nodes/children)
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height

        #New quadrant boundaries
        ne_node = Rectangle(x + w / 2, y, w/2, h/2)
        self.northeast = QuadtreeNode(ne_node, self.capacity)

        nw_node = Rectangle(x, y, w/2, h/2)
        self.northwest = QuadtreeNode(nw_node, self.capacity)

        se_node = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.southeast = QuadtreeNode(se_node, self.capacity)

        sw_node = Rectangle(x, y + h/2, w/2, h/2)
        self.southwest = QuadtreeNode(sw_node, self.capacity)

        self.divided = True

        #Insert the points into the smaller nodes
        for p in self.points:
            self.insert(p)
        self.points = [] #clear points form this node

    def insert(self, point):
        #Puts the point into the quadtree
        if not self.boundary.contains(point):
            return False

        #Add the point to this node if there is space to do so and it isn't divided
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        
        #Divide the node if it isn't already divided
        if not self.divided:
            self.subdivide()
        
        #Move the points to the appropriate quadrant
        if self.northeast.insert(point): return True
        if self.northwest.insert(point): return True
        if self.southeast.insert(point): return True
        if self.southwest.insert(point): return True
        
        return False

    def remove(self, point):
        #removes the old point from the quadtree
        if not self.boundary.contains(point):
            return False
        
        if point in self.points:
            self.points.remove(point)
            return True

        #if the node is divided, remove from the children nodes
        if self.divided:
            return (
                self.northeast.remove(point) or
                self.northwest.remove(point) or
                self.southeast.remove(point) or
                self.southwest.remove(point)
            )

        return False

    def query(self, point, best_found_point):
        #If this node doesn't have a closer point, stop searching
        if self.boundary.distance_sq_to_point(point) > best_found_point['dist_squared']:
            return
        
        #Check points within this node
        for p in self.points:
            dist_squared = (p.x - point.x)**2 + (p.y - point.y)**2
            if dist_squared < best_found_point['dist_squared']:
                best_found_point['dist_squared'] = dist_squared
                best_found_point['point'] = p

        #If children exist, recursively searh them
        if self.divided:
            #search children, closest first
            children = [self.northeast, self.northwest, self.southeast, self.southwest]
            children.sort(key=lambda child: child.boundary.distance_sq_to_point(point))

            for child in children:
                child.query(point, best_found_point)
        return 


class Quadtree:
    #initialize Quadtree class
    def __init__(self, boundary):
        self.boundary = boundary
        self.root = None