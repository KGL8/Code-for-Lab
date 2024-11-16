import vispy
from vispy import scene
from imports import *

# Set up a canvas with a 3D view
canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

# Render line to scene
def line(position,color=(0,0,1)):
    view.add(scene.Line(pos=position, color=color, connect='segments'))

# Render box to the scene
def box(min_pt, max_pt, rotation=(0,0,0), color=(0,0,1,0.5)):
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
        shading='flat'        # Smooth shading for a better appearance
    )
    view.add(mesh_visual)

# Axes
line([[0,0,0],[0,0,1]],(1,0,0))
line([[0,0,0],[0,1,0]],(0,1,0))
line([[0,0,0],[1,0,0]],(0,0,1))

# Target Box
box(T_min, T_max, color=(1,0,0,0.5))

# Run the application
if __name__ == '__main__':
    vispy.app.run()
