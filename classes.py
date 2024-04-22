from dataclasses import dataclass



@dataclass(kw_only=True)
class Point:
    x: float
    y: float
    edges: list["Edge"]

@dataclass(kw_only=True)
class Edge:
    start: Point
    end: Point
    cells: list["Cell"]

@dataclass(kw_only=True)
class Cell:
    edges_with_orientation: list[tuple[Edge, bool]] # bool říká orientaci strany- true pokud stejná, false opačně

    @property
    def neighbors(self) -> list["Cell"]:
        result :list["Cell"] = []
        for edges,_ in self.edges_with_orientation:
            for cell in edges.cells:
                if cell != self and cell not in result:
                    result.append(cell)
        return result
    
@dataclass(kw_only=True)
class Mesh:
    cells: list[Cell]
    obstructions: list[Cell|Edge] # Nevím jak to pojmenovat, pokud tam je cell, tak se sít vytvoří kolem, pokud edge tak by síť hranu měla následovat.