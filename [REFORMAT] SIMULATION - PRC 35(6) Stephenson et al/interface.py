# # interface.py
# import vispy
# from vispy import scene
# from imports import *

# # Set up a canvas with a 3D view
# canvas = scene.SceneCanvas(keys='interactive', show=True)
# view = canvas.central_widget.add_view()
# view.camera = 'turntable'
# view.camera.up = "+y" # type: ignore

# # Render line to scene
# def line(position,color=(0,0,1)):
#     view.add(scene.Line(pos=position, color=color, connect='strip', antialias=False))

# # Render marker to scene
# def marker(position,color=(0,0.7,0)):
#     marker = scene.visuals.Markers() # type: ignore
#     marker.set_data(array([position]), face_color=color, symbol='square', size=7)
#     view.add(marker)

# # Render box to the scene
# def box(min_pt, max_pt, rotation=(0,0,0), color=(0,0,1,1)):
#     corners = array([[x, y, z] for x in (min_pt[0], max_pt[0]) for y in (min_pt[1], max_pt[1]) for z in (min_pt[2], max_pt[2])])

#     corners_translated = corners - (min_pt + max_pt) / 2

#     def rotation_matrix(roll, pitch, yaw):
#         Rx = array([[1, 0, 0],
#                        [0, cos(roll), -sin(roll)],
#                        [0, sin(roll), cos(roll)]])
#         Ry = array([[cos(pitch), 0, sin(pitch)],
#                        [0, 1, 0],
#                        [-sin(pitch), 0, cos(pitch)]])
#         Rz = array([[cos(yaw), -sin(yaw), 0],
#                        [sin(yaw), cos(yaw), 0],
#                        [0, 0, 1]])
#         return Rz @ Ry @ Rx

#     corners_rotated = corners_translated.dot(rotation_matrix(*rotation).T)

#     # Translate back to the original position
#     corners_final = corners_rotated + (min_pt + max_pt) / 2

#     # Define the box's faces
#     faces = array([
#         [0, 1, 2], [1, 3, 2],  # Front face
#         [4, 6, 5], [5, 6, 7],  # Back face
#         [0, 2, 4], [4, 2, 6],  # Left face
#         [1, 5, 3], [3, 5, 7],  # Right face
#         [0, 4, 1], [1, 4, 5],  # Bottom face
#         [2, 3, 6], [3, 7, 6]   # Top face
#     ], dtype=uint32)

#     # Render the mesh
#     mesh_visual = scene.Mesh(
#         vertices=corners_final.astype(float32),
#         faces=faces,
#         color=color,
#         shading='flat'        # Smooth shading for a better appearance
#     )
#     view.add(mesh_visual)

# # Axes
# line([[0,0,0],[0,0,1]],(1,0,0))
# line([[0,0,0],[0,1,0]],(0,1,0))
# line([[0,0,0],[1,0,0]],(0,0,1))

# # Target Box
# box(T_min, T_max)

# # Run the application
# def print_scene():
#     vispy.app.run() # type: ignore

# interface.py
import vispy
from vispy import app,scene,visuals
import vispy.visuals
import vispy.visuals.filters
from imports import *

# Set up a canvas with a 3D view
canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.up = "+y" # type: ignore

# Render line to scene
def line(position,color=(0,0,1)):
    view.add(scene.Line(pos=position, color=color, connect='segments', antialias=False))

# Render marker to scene
def marker(position,color=(0,0.7,0)):
    marker = scene.visuals.Markers() # type: ignore
    marker.set_data(array([position]), face_color=color, symbol='square', size=7)
    view.add(marker)

# Render box to the scene
def box(min_pt, max_pt, rotation=(0,0,0), color=(0,0,1,1), wireframe=False):
    corners = array([[x, y, z] for x in (min_pt[0], max_pt[0]) for y in (min_pt[1], max_pt[1]) for z in (min_pt[2], max_pt[2])])

    corners_translated = corners - (min_pt + max_pt) / 2

    def rotation_matrix(roll, pitch, yaw):
        Rx = array([[1, 0, 0],
                       [0, cos(roll), -sin(roll)],
                       [0, sin(roll), cos(roll)]])
        Ry = array([[cos(pitch), 0, sin(pitch)],
                       [0, 1, 0],
                       [-sin(pitch), 0, cos(pitch)]])
        Rz = array([[cos(yaw), -sin(yaw), 0],
                       [sin(yaw), cos(yaw), 0],
                       [0, 0, 1]])
        return Rz @ Ry @ Rx

    corners_rotated = corners_translated.dot(rotation_matrix(*rotation).T)

    # Translate back to the original position
    corners_final = corners_rotated + (min_pt + max_pt) / 2

    # Define the box's faces
    faces = array([
        [0, 1, 2], [1, 3, 2],  # Front face
        [4, 6, 5], [5, 6, 7],  # Back face
        [0, 2, 4], [4, 2, 6],  # Left face
        [1, 5, 3], [3, 5, 7],  # Right face
        [0, 4, 1], [1, 4, 5],  # Bottom face
        [2, 3, 6], [3, 7, 6]   # Top face
    ], dtype=uint32)

    # Render the mesh
    mesh_visual = scene.Mesh(
        vertices=corners_final.astype(float32),
        faces=faces,
        color=color,
        shading='flat'
    )
    if wireframe:
        edges = [[c1.tolist(), c2.tolist()] for i, c1 in enumerate(corners) for j, c2 in enumerate(corners) 
         if i < j and sum(c1 != c2) == 1]
        line(edges,(0,0,1))
    else:
        view.add(mesh_visual)

# Axes
line([[0,0,0],[0,0,1]],(1,0,0))
line([[0,0,0],[0,1,0]],(0,1,0))
line([[0,0,0],[1,0,0]],(0,0,1))

# Target Box
box(T_min, T_max,wireframe=True)

# Detectors
box(*D_90_minmax, (0,α1+α1,0), (1,0,0,1))
box(*D_135_minmax, (0,α1+α2,0), (1,1,0,1))
box(*D_155_minmax, (0,α1+α3,0), (0,1,0,1))
box(*D_45_minmax, (0,α1+α4,0), (0,1,1,1))

# Define keybind actions
def on_key_press(event):
    if event.text == '1':
        view.camera.center = (0, 0, 0)
        print("looking at origin")
    elif event.text == '2':
        view.camera.center = (0, 0, T_depth / 2 + O_T_dist)
        print("looking at target")
    elif event.text == '3':
        view.camera.center = tuple(D_90_pos)
        print("looking at 90° detector")
    elif event.text == '4':
        view.camera.center = tuple(D_135_pos)
        print("looking at 135° detector")
    elif event.text == '5':
        view.camera.center = tuple(D_155_pos)
        print("looking at 155° detector")
    elif event.text == '6':
        view.camera.center = tuple(D_45_pos)
        print("looking at 45° detector")

# Connect the keypress event to the handler
canvas.events.key_press.connect(on_key_press)

# Run the application
def print_scene():
    vispy.app.run() # type: ignore