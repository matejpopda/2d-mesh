import math

from vor_classes import Point, Event, Arc, Edge, PriorityQueue

class Voronoi:
    def __init__(self, points):
        """Initialize the Voronoi diagram with given points."""
        self.output = [] # List of line segments
        self.arc = None  # Binary tree of parabola arcs (beachline)

        self.points = PriorityQueue() # Site events
        self.event = PriorityQueue() # Circle events

        # Initial bounding box
        self.x0 = -50.0
        self.x1 = -50.0
        self.y0 = 550.0
        self.y1 = 550.0

        # Insert points into the site event priority queue and adjust the bounding box
        for p in points:
            point = Point(p[0], p[1])
            self.points.push(point)
            if point.x < self.x0: self.x0 = point.x
            if point.y < self.y0: self.y0 = point.y
            if point.x > self.x1: self.x1 = point.x
            if point.y > self.y1: self.y1 = point.y

        # Add margins to the bounding box
        difx = (self.x1 - self.x0 + 1) / 5.0
        dify = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - difx
        self.x1 = self.x1 + difx
        self.y0 = self.y0 - dify
        self.y1 = self.y1 + dify

    def run_diagram(self):
        """Run the Voronoi diagram algorithm."""
        while not self.points.empty():
            if not self.event.empty() and (self.event.top().x <= self.points.top().x):
                self.handle_circle_event()
            else:
                self.handle_site_event() 

        while not self.event.empty():
            self.handle_circle_event()
        self.finish_edges()

    def handle_site_event(self):
        """Handle site events by inserting new arcs."""
        point = self.points.pop()
        self.insert_arc(point)

    def handle_circle_event(self):
        """Handle circle events and remove arcs that disappear."""
        event = self.event.pop()
        if event.valid:
            edge = Edge(event.p)
            self.output.append(edge)

            arc = event.a
            if arc.pprev is not None:
                arc.pprev.pnext = arc.pnext
                arc.pprev.s1 = edge
            if arc.pnext is not None:
                arc.pnext.pprev = arc.pprev
                arc.pnext.s0 = edge

            if arc.s0 is not None: arc.s0.finish(event.p)
            if arc.s1 is not None: arc.s1.finish(event.p)

            if arc.pprev is not None: self.check_circle_event(arc.pprev, event.x)
            if arc.pnext is not None: self.check_circle_event(arc.pnext, event.x)

    def insert_arc(self, p):
        """Insert a new arc corresponding to a new site event."""
        if self.arc is None:
            self.arc = Arc(p)
        else:
            current_arc = self.arc
            while current_arc is not None:
                flag, z = self.check_intersection(p, current_arc)
                if flag:
                    flag, zz = self.check_intersection(p, current_arc.pnext)
                    if (current_arc.pnext is not None) and (not flag):
                        current_arc.pnext.pprev = Arc(current_arc.p, current_arc, current_arc.pnext)
                        current_arc.pnext = current_arc.pnext.pprev
                    else:
                        current_arc.pnext = Arc(current_arc.p, current_arc)
                    current_arc.pnext.s1 = current_arc.s1

                    current_arc.pnext.pprev = Arc(p, current_arc, current_arc.pnext)
                    current_arc.pnext = current_arc.pnext.pprev
                    current_arc = current_arc.pnext 

                    seg = Edge(z)
                    self.output.append(seg)
                    current_arc.pprev.s1 = current_arc.s0 = seg

                    seg = Edge(z)
                    self.output.append(seg)
                    current_arc.pnext.s0 = current_arc.s1 = seg

                    self.check_circle_event(current_arc, p.x)
                    self.check_circle_event(current_arc.pprev, p.x)
                    self.check_circle_event(current_arc.pnext, p.x)

                    return
                        
                current_arc = current_arc.pnext

            current_arc = self.arc
            while current_arc.pnext is not None:
                current_arc = current_arc.pnext
            current_arc.pnext = Arc(p, current_arc)
            x = self.x0
            y = (current_arc.pnext.p.y + current_arc.p.y) / 2.0
            start = Point(x, y)

            edge = Edge(start)
            current_arc.s1 = current_arc.pnext.s0 = edge
            self.output.append(edge)

    def check_circle_event(self, arc, x_sweep):
        """Check and add valid circle events to the priority queue."""
        if (arc.edge is not None) and (arc.edge.x != self.x0):
            arc.edge.valid = False
        arc.edge = None

        if (arc.pprev is None) or (arc.pnext is None): return

        flag, x, o = self.compute_circle(arc.pprev.p, arc.p, arc.pnext.p)
        if flag and (x > self.x0):
            arc.edge = Event(x, o, arc)
            self.event.push(arc.edge)

    def compute_circle(self, pointA, pointB, pointC):
        """Calculate the circle defined by points pointA, pointB, and pointC."""
        if ((pointB.x - pointA.x) * (pointC.y - pointA.y) - (pointC.x - pointA.x) * (pointB.y - pointA.y)) > 0:
            return False, None, None

        deltaX_AB = pointB.x - pointA.x
        deltaY_AB = pointB.y - pointA.y
        deltaX_AC = pointC.x - pointA.x
        deltaY_AC = pointC.y - pointA.y
        productX = deltaX_AB * (pointA.x + pointB.x) + deltaY_AB * (pointA.y + pointB.y)
        productY = deltaX_AC * (pointA.x + pointC.x) + deltaY_AC * (pointA.y + pointC.y)
        denominator = 2 * (deltaX_AB * (pointC.y - pointB.y) - deltaY_AB * (pointC.x - pointB.x))

        if denominator == 0:
            return False, None, None

        centerX = (deltaY_AC * productX - deltaY_AB * productY) / denominator
        centerY = (deltaX_AB * productY - deltaX_AC * productX) / denominator

        radius_squared = (pointA.x - centerX) ** 2 + (pointA.y - centerY) ** 2
        radius = math.sqrt(radius_squared)
        center = Point(centerX, centerY)

        return True, radius + centerX, center
        
    def check_intersection(self, new_site, existing_arc):
        """Check if a new site event intersects with an existing arc."""
        if existing_arc is None:
            return False, None
        if existing_arc.p.x == new_site.x:
            return False, None

        y_intersection_above = 0.0
        y_intersection_below = 0.0

        if existing_arc.pprev is not None:
            y_intersection_above = (self.parabola_intersection(existing_arc.pprev.p, existing_arc.p, 1.0 * new_site.x)).y
        if existing_arc.pnext is not None:
            y_intersection_below = (self.parabola_intersection(existing_arc.p, existing_arc.pnext.p, 1.0 * new_site.x)).y

        if (((existing_arc.pprev is None) or (y_intersection_above <= new_site.y)) and
            ((existing_arc.pnext is None) or (new_site.y <= y_intersection_below))):
            intersection_y = new_site.y
            intersection_x = ((existing_arc.p.x ** 2 + (existing_arc.p.y - intersection_y) ** 2 - new_site.x ** 2)
                            / (2 * existing_arc.p.x - 2 * new_site.x))
            intersection_point = Point(intersection_x, intersection_y)
            return True, intersection_point
        return False, None

    def parabola_intersection(self, point1, point2, directrix):
        """Compute the intersection of two parabolas defined by point1, point2 and the directrix."""
        if point1.x == point2.x:
            intersection_y = (point1.y + point2.y) / 2.0
        elif point2.x == directrix:
            intersection_y = point2.y
        elif point1.x == directrix:
            intersection_y = point1.y
        else:
            denom1 = 2.0 * (point1.x - directrix)
            denom2 = 2.0 * (point2.x - directrix)

            a_coeff = 1.0 / denom1 - 1.0 / denom2
            b_coeff = -2.0 * (point1.y / denom1 - point2.y / denom2)
            c_coeff = ((point1.y ** 2 + point1.x ** 2 - directrix ** 2) / denom1
                    - (point2.y ** 2 + point2.x ** 2 - directrix ** 2) / denom2)

            discriminant = b_coeff ** 2 - 4 * a_coeff * c_coeff
            intersection_y = (-b_coeff - math.sqrt(discriminant)) / (2 * a_coeff)
            
        intersection_x = ((point1.x ** 2 + (point1.y - intersection_y) ** 2 - directrix ** 2)
                        / (2 * point1.x - 2 * directrix))
        intersection_point = Point(intersection_x, intersection_y)
        
        return intersection_point

    def finish_edges(self):
        """Finish the remaining edges of the Voronoi diagram."""
        boundary_length = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        current_arc = self.arc
    
        while current_arc.pnext is not None:
            if current_arc.s1 is not None:
                intersection_point = self.parabola_intersection(current_arc.p, current_arc.pnext.p, boundary_length * 2.0)
                current_arc.s1.finish(intersection_point)
            current_arc = current_arc.pnext
            
    def disp_output(self):
        """Display the generated Voronoi diagram edges."""
        edge_index = 0
        for edge in self.output:
            edge_index += 1
            start_point = edge.start
            end_point = edge.end
            print(start_point.x, start_point.y, end_point.x, end_point.y)

    def get_output(self):
        """Get the list of edges in the Voronoi diagram."""
        res = []
        for out in self.output:
            start_point = out.start
            end_point = out.end
            res.append((start_point.x, start_point.y, end_point.x, end_point.y))
        return res
