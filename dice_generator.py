import bpy
import bmesh
from mathutils import *
from math import *

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

def euc_dist(c1, c2):
    '''Take two 3-tuples of x,y,z coordinates and return the Euclidian distance between them'''
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    return sqrt(pow(x2-x1, 2) + pow(y2-y1, 2) + pow(z2-z1, 2))

# Golden ratiooooo
gr = (1 + sqrt(5)) / 2
inv_gr = 1/gr


# Define geometry sets

tetrahedron = {"vertices": [], "edges": []}
tetrahedron["vertices"] = [
    (1.0, 1.0, 1.0),
    (1.0, -1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (-1.0, -1.0, 1.0),
]
tetrahedron["edges"] = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# Yes I know there's a primitive cube type that does this!
cube = {"vertices": [], "edges": []}
# Iteratively generate all corners
for z in [1.0, -1.0]:
    for y in [1.0, -1.0]:
        for x in [1.0,-1.0]:
            cube["vertices"].append((x,y,z))
# Index our vertices so we can compare and associate
vert_set = list(enumerate(cube["vertices"]))
for index, vertex in vert_set:
    for sec_index, sec_vertex in vert_set:
        if index == sec_index:
            pass
        elif (sec_index, index) in cube["edges"]:
            pass
        else:
            diff = 0
            for i in [0,1,2]:
                diff = diff+1 if (vertex[i] * sec_vertex[i]) < 0 else diff
            if diff == 1:
                cube["edges"].append((index, sec_index))


octahedron = {"vertices": [], "edges": []}

# Construct the positive face set first, then the negative
for i in [1.0, -1.0]:
    octahedron["vertices"].append((i, 0.0, 0.0))
    octahedron["vertices"].append((0.0, i, 0.0))
    octahedron["vertices"].append((0.0, 0.0, i))

vert_set = list(enumerate(octahedron["vertices"]))

# I should really use a map function here, huh?
for index, vertex in vert_set:
    for sec_index, sec_vertex in vert_set:
        if index == sec_index:
            pass
        elif (sec_index, index) in octahedron["edges"]:
            pass
        else:
            x1, y1, z1 = vertex
            x2, y2, z2 = sec_vertex
            if not (
                x1 == -x2 and x1 != 0.0
                or y1 == -y2 and y1 != 0.0
                or z1 == -z2 and z1 != 0.0
            ):
                octahedron["edges"].append((index, sec_index))


# Yes, I know I can just use the built in icosphere.                
icosahedron = {"vertices": [], "edges": []}

for i in [1.0, -1.0]:
    for j in [gr, -gr]:
        icosahedron["vertices"].append((0.0, i, j))
        icosahedron["vertices"].append((i, j, 0.0))
        icosahedron["vertices"].append((j, 0.0, i))

vert_set = list(enumerate(icosahedron["vertices"]))
# I'm going to switch to calculating the distance between vertices now, much easier than trying to topological reasoning.
for index, vertex in vert_set:
    adjacent_indices = []
    for sec_index, sec_vertex in vert_set:
        if not index == sec_index:
            if euc_dist(vertex, sec_vertex) == 2.0:
                adjacent_indices.append(sec_index)
        else:
            pass
    for sec_index in adjacent_indices:
        if (sec_index, index) not in icosahedron["edges"]:
            icosahedron["edges"].append((index, sec_index))


dodecahedron = {"vertices": [], "edges": []}

# Stealing the first 8 points because I'm lazy.
dodecahedron["vertices"]=cube["vertices"].copy()

for i in [inv_gr, -inv_gr]:
    for j in [gr, -gr]:
        dodecahedron["vertices"].append((0.0, i, j))
        dodecahedron["vertices"].append((i, j, 0.0))
        dodecahedron["vertices"].append((j, 0.0, i))

vert_set = list(enumerate(dodecahedron["vertices"]))

# Caclulate by distance once again
for index, vertex in vert_set:
    adjacent_indices = []
    for sec_index, sec_vertex in vert_set:
        if not index == sec_index:
            if euc_dist(vertex, sec_vertex) < 1.5:
                adjacent_indices.append(sec_index)
        else:
            pass
    for sec_index in adjacent_indices:
        if (sec_index, index) not in dodecahedron["edges"]:
            dodecahedron["edges"].append((index, sec_index))


decahedron = {"vertices": [(0, 0, 1), (0, 0, -1)], "edges": []}
vert_set = []
# Lazy implementation of a ring
ind_set = range(0, 10)
# Start Z offsets on the Southern equator as derived
z_off = round(-(1 - cos(pi / 5)) / 2, 10)

for index in ind_set:
    # Added rounding to 10 sig fig thanks to weird float precision errors on sin functions)
    vertex = (
        round(cos(2 * pi * index / 10), 10),
        round(sin(2 * pi * index / 10), 10),
        z_off if index % 2 else -z_off,
    )
    decahedron["vertices"].append(vertex)
    decahedron["edges"].append((index + 2, ind_set[index - 1] + 2))
    if index % 2:
        decahedron["edges"].append((index + 2, 1))
    else:
        decahedron["edges"].append((index + 2, 0))


die = {
    "tetrahedron": tetrahedron,
    "cube": cube,
    "octahedron": octahedron,
    "decahedron": decahedron,
    "dodecahedron": dodecahedron,
    "icosahedron": icosahedron
}

for key, geo in die.items():
    new_mesh = bpy.data.meshes.new(f"{key}_mesh")
    new_mesh.from_pydata(vertices = geo["vertices"], edges = geo["edges"], faces = [])
    
    #Construct faces in bmesh
    bm = bmesh.new()
    bm.from_mesh(new_mesh)
    for edge in bm.edges:
        edge.select=True
    bmesh.ops.edgenet_fill(bm, edges=bm.edges)
    bm.to_mesh(new_mesh)
    bm.free()
    
    new_obj = bpy.data.objects.new(key, new_mesh)
    bpy.context.collection.objects.link(new_obj)

#inset_dia = 25


    