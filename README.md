# TODO
- Vytvořit buňky (napč přes voronoi teselací)
- Uložit je do tříd v classes.py
- Hledání průniků, tj. je bod v buňce? prochází přímka buňkou? Najít průsečík 2 úseček
- Při vytváření mít překážky
- Kreslení buněk (asi v matplotlibu, případně přes pygame, [nebo přes cv2 ](https://stackoverflow.com/questions/60587273/drawing-a-line-on-an-image-using-mouse-clicks-with-python-opencv-library))
- Nějak s buňkami hýbat, třeba by každá hrana fungovat jako pružina, nebo něco takového, případně náhodně
- Nějaká regularizace?


# Program flow
1. Ze souboru mesh_generation.py se vezme funkce generate_mesh (případně více možností), ta nějak vygeneruje mesh
2. Používáme třídy definované v classes
3. Ze souboru draw.py budeme pak vykreslovat