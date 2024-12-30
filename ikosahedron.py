import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as anim

# Define the golden ratio
phi = (1 + np.sqrt(5)) / 2

# Define the 12 vertices of a regular icosahedron
vertices = np.array([
  [-1, phi, 0],
  [1, phi, 0],
  [-1, -phi, 0],
  [1, -phi, 0],
  [0, -1, phi],
  [0, 1, phi],
  [0, -1, -phi],
  [0, 1, -phi],
  [phi, 0, -1],
  [phi, 0, 1],
  [-phi, 0, -1],
  [-phi, 0, 1]
])

# Define the faces (triangles) that make up the icosahedron's surface
faces = [
  [0, 11, 5],
  [0, 5, 1],
  [0, 1, 7],
  [0, 7, 10],
  [0, 10, 11],
  [1, 5, 9],
  [5, 11, 4],
  [11, 10, 2],
  [10, 7, 6],
  [7, 1, 8],
  [4, 9, 5],
  [6, 2, 10],
  [8, 6, 7],
  [9, 8, 1],
  [2, 4, 11],
  [3, 9, 4],
  [3, 4, 2],
  [3, 2, 6],
  [3, 6, 8],
  [3, 8, 9],
]

# Create the graph using networkx
G = nx.Graph()
# Add the edges to the graph based on the icosahedron's structure
icosahedron_edges = [
  (0, 1), (0, 2), (0, 4), (0, 5), (0, 10),
  (1, 0), (1, 2), (1, 6), (1, 8), (1, 11),
  (2, 0), (2, 1), (2, 3), (2, 5), (2, 10),
  (3, 2), (3, 4), (3, 7), (3, 8), (3, 11),
  (4, 0), (4, 3), (4, 5), (4, 7), (4, 9),
  (5, 0), (5, 2), (5, 4), (5, 6), (5, 10),
  (6, 1), (6, 5), (6, 7), (6, 8), (6, 9),
  (7, 3), (7, 4), (7, 6), (7, 8), (7, 11),
  (8, 1), (8, 3), (8, 6), (8, 7), (8, 9),
  (9, 4), (9, 6), (9, 7), (9, 8), (9, 10),
  (10, 0), (10, 2), (10, 5), (10, 9), (10, 11),
  (11, 1), (11, 3), (11, 7), (11, 9), (11, 10)
]
G.add_edges_from(icosahedron_edges)


def plx(line, d):
  p1, p2 = line
  p1 = np.array(p1)
  p2 = np.array(p2)

  # Calculate the point on the line at distance D
  p = (1 - d) * p1 + d * p2

  return np.array(p)


def draw_edge(ax, target, _color, d):
  ne = [target[0], plx(target, d)]
  # print(f'edge: {target}\n\n{ne}')
  poly3d = Poly3DCollection([ne], facecolors='green', linewidths=5, edgecolors='#C20', alpha=1)
  ax.add_collection3d(poly3d)


# Apply spectral layout to position the vertices in 2D
pos = nx.spectral_layout(G)

# Plotting the icosahedron in 3D
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

face_colors = [
  '#0A0', '#090', '#080', '#070', '#060',
  '#0AA', '#1AA', '#2AA', '#3AA', '#4AA',
  '#08A', '#18A', '#28A', '#38A', '#48A',
  '#01A', '#02A', '#03A', '#04A', '#05A',
]


def draw_shape():
  ax.set_axis_off()

  # Plot faces (surface)
  for i, face in enumerate(faces):
    verts = vertices[face]  # Get the 3D coordinates of the face's vertices
    color = face_colors[i % len(face_colors)]
    poly3d = Poly3DCollection([verts], facecolors=color, linewidths=0, edgecolors='#ccc', alpha=0.5)
    ax.add_collection3d(poly3d)

  # Plot vertices (using the spectral layout for node positioning)
  for v in vertices:
    ax.scatter(v[0], v[1], v[2], color='b', s=100)

  # Labels for vertices (optional)
  for i, v in enumerate(vertices):
    ax.text(v[0], v[1], v[2], f'{i}', color='#777', fontsize=20)

  # Set the aspect ratio and labels
  # ax.set_xlabel('X')
  # ax.set_ylabel('Y')
  # ax.set_zlabel('Z')

  # Set the viewing angle
  ax.view_init(72, -169, -114)

  # Set limits for a better view
  ax.set_xlim([-1.5, 1.5])
  ax.set_ylim([-1.5, 1.5])
  ax.set_zlim([-1.5, 1.5])


def update(i):
  ax.clear()
  draw_shape()

  d1 = max(0, min((i + 1) / 10, 1))
  d2 = max(0, min((i - 9) / 10, 1))
  d3 = max(0, min((i - 19) / 10, 1))
  d4 = max(0, min((i - 29) / 10, 1))
  d5 = max(0, min((i - 39) / 10, 1))

  for k in range(0, 5):
    draw_edge(ax, vertices[faces[k][0:2]], '#F00', d=d1)

  if d2 == 0:
    return

  for k in range(0, 5):
    draw_edge(ax, vertices[faces[k][1:3]], '#F00', d=d2)

  if d3 == 0:
    return

  for k in range(5, 10):
    draw_edge(ax, vertices[faces[k][1:3]], '#F00', d=d3)
    draw_edge(ax, vertices[faces[5+k][::2]][::-1], '#F00', d=d3)

  if d4 == 0:
    return

  for k in range(15, 20):
    draw_edge(ax, vertices[faces[k][1:3]], '#F00', d=d4)

  if d5 == 0:
    return

  for k in range(15, 20):
    draw_edge(ax, vertices[faces[k][0:2]][::-1], '#F00', d=d5)


a = anim.FuncAnimation(fig, update, frames=50, repeat=True, repeat_delay=5000, interval=300)
plt.show()
