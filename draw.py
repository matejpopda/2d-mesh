import tkinter as tk
from tkinter import simpledialog
import random
from shapely.geometry import LineString
from Voronoi import Voronoi

class MainWindow:
    RADIUS = 2

    LOCK_FLAG = False
    
    def __init__(self, master):
        self.master = master
        self.master.title("Voronoi")
        self.divided = False

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=500, height=500)
        self.w.config(background='white')
        self.w.bind('<Double-1>', self.onDoubleClick)
        self.w.pack()       

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack(padx=5, pady=5)
        
        self.btnCalculate = tk.Button(self.frmButton, text='Calculate', width=12, command=self.onClickCalculate)
        self.btnCalculate.pack(side=tk.LEFT)
        
        self.btnClear = tk.Button(self.frmButton, text='Clear', width=12, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)
        
        self.line_btn = tk.Button(self.frmButton, text="Line", width=12, command=self.draw_line)
        self.line_btn.pack(side=tk.LEFT)
        
        self.btn_random_points = tk.Button(self.frmButton, text="Random Points", width=12, command=self.add_random_points)
        self.btn_random_points.pack(side=tk.LEFT)  

        
    def draw_line(self):
        self.y1, self.y2 = 0, self.w.winfo_height()
        self.x1, self.x2 = random.randint(0, self.w.winfo_width()),random.randint(0, self.w.winfo_width())
        self.line = self.w.create_line(self.x1, self.y1,self.x2,self.y2, fill='crimson')
        self.line_btn.config(state=tk.DISABLED)
        self.divided = True
        
    def add_random_points(self):
        num_points = simpledialog.askinteger("Input", "Enter number of random points:", parent=self.master)
        if num_points is not None:
            for _ in range(num_points):
                x = random.randint(1, self.w.winfo_width())
                y = random.randint(1, self.w.winfo_width())
                self.w.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill='coral', outline='lightcoral')

    def onClickCalculate(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True
        
            if self.divided == True:
                points_left, points_right = self.classify_points()
                vp = Voronoi(points_left)
                vp.process()
                lines = vp.get_output()
                self.draw_adjusted_lines(lines,[self.x1,self.y1,self.x2,self.y2],'A')
                
                vp = Voronoi(points_right)
                vp.process()
                lines = vp.get_output()
                self.draw_adjusted_lines(lines,[self.x1,self.y1,self.x2,self.y2],'B')
            else:
                pObj = self.w.find_all()
                points = []
                for p in pObj:
                    coord = self.w.coords(p)
                    points.append((coord[0]+self.RADIUS, coord[1]+self.RADIUS))
                    
                vp = Voronoi(points)
                vp.process()
                lines = vp.get_output()
                self.drawLinesOnCanvas(lines)

    def onClickClear(self):
        self.LOCK_FLAG = False
        self.w.delete(tk.ALL)
        self.line_btn.config(state=tk.NORMAL)
        self.divided = False 

    def onDoubleClick(self, event):
        if not self.LOCK_FLAG:
            self.w.create_oval(event.x-self.RADIUS, event.y-self.RADIUS, event.x+self.RADIUS, event.y+self.RADIUS, fill="black")

    def drawLinesOnCanvas(self, lines):
        for l in lines:
            self.w.create_line(l[0], l[1], l[2], l[3], fill='darkblue')
            
    def classify_points(self):
        a = self.y2 - self.y1
        b = self.x1 - self.x2
        c = self.x2 * self.y1 - self.x1 * self.y2
        points_left = []
        points_right = []
        pObj = self.w.find_all()
        for p in pObj:
            coord = self.w.coords(p)
            x = coord[0] + self.RADIUS
            y = coord[1] + self.RADIUS

            d = a * x + b * y + c
            if d > 0 or d==0:
                points_left.append((x, y))
            elif d < 0:
                points_right.append((x, y))

        return points_left, points_right

    
    @staticmethod
    def adjust_line_to_boundaryA(line, boundary):
        a = boundary.coords[1][1] - boundary.coords[0][1]  # y2 - y1
        b = boundary.coords[0][0] - boundary.coords[1][0]  # x1 - x2
        c = boundary.coords[1][0] * boundary.coords[0][1] - boundary.coords[0][0] * boundary.coords[1][1]  # x2*y1 - x1*y2

        # Check where each end of the line is with respect to the boundary
        start_side = a * line.coords[0][0] + b * line.coords[0][1] + c  # Plug x, y of the start point
        end_side = a * line.coords[1][0] + b * line.coords[1][1] + c    # Plug x, y of the end point


        if line.intersects(boundary):
            intersection = line.intersection(boundary)
            if intersection.geom_type == 'Point':
                intersection_point = intersection.coords[0] 
                if start_side > 0:  # Assuming negative side is the left side
                    return LineString([line.coords[0], intersection_point])
                else:
                    return LineString([intersection_point, line.coords[1]])
            elif intersection.geom_type == 'LineString':
                # If the intersection is a line (coincident parts), decide based on one of the endpoints
                return line if start_side > 0 else None
        return line if start_side > 0 else None 
    
    @staticmethod
    def adjust_line_to_boundaryB(line, boundary):
        a = boundary.coords[1][1] - boundary.coords[0][1]  # y2 - y1
        b = boundary.coords[0][0] - boundary.coords[1][0]  # x1 - x2
        c = boundary.coords[1][0] * boundary.coords[0][1] - boundary.coords[0][0] * boundary.coords[1][1]  # x2*y1 - x1*y2

        # Check where each end of the line is with respect to the boundary
        start_side = a * line.coords[0][0] + b * line.coords[0][1] + c  # Plug x, y of the start point
        end_side = a * line.coords[1][0] + b * line.coords[1][1] + c    # Plug x, y of the end point

        if line.intersects(boundary):
            intersection = line.intersection(boundary)
            if intersection.geom_type == 'Point':
                intersection_point = intersection.coords[0] 
                if start_side < 0:  # Assuming negative side is the left side
                    return LineString([line.coords[0], intersection_point])
                else:
                    return LineString([intersection_point, line.coords[1]])
            elif intersection.geom_type == 'LineString':
                # If the intersection is a line (coincident parts), decide based on one of the endpoints
                return line if start_side < 0 else None
        return line if start_side < 0 else None 
    
    def draw_adjusted_lines(self, lines, boundary,mode):
        for line in lines:
            x1, y1, x2, y2 = line
            line_geom = LineString([(x1, y1), (x2, y2)])
            boundary_geom = LineString([(boundary[0], boundary[1]), (boundary[2], boundary[3])])
            if mode =="A":
                color = 'darkblue'
                adjusted_line = self.adjust_line_to_boundaryA(line_geom, boundary_geom)
            else:
                color = 'orange'
                adjusted_line = self.adjust_line_to_boundaryB(line_geom, boundary_geom)
            if adjusted_line:
                self.w.create_line(adjusted_line.coords[0][0], adjusted_line.coords[0][1],
                                adjusted_line.coords[1][0], adjusted_line.coords[1][1], fill=color)

