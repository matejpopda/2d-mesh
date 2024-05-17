# Program structure
1. Logika pro generování sítě ve Voronoi.py
2. Třídy definované ve vor_classes.py
3. Soubor draw.py pro vykreslování

# Aktuální stav
- Voronoiovská mesh (Fortune's algorithm).
- Rošíření kódu o případ s lineárním rozhraním. (Ale buňky na rozhraní nemají společné vrcholy.)
- Automatická generace náhodných bodů.
- Náhodný pohyb buněk, nicméně bez vyhlazování sítě (křížení).  

   _voronoi.py: logika generování sítě_  
  _draw.py: tkinter okno pro interaktivní vizualizaci_  
  _vor_classes: objekty pro výpočet sítě_


<p float="left">
  <img src="img/noline.png" width="500"/>
  <img src="img/line.png" width="500" /> 
</p>
