import trimesh
import pyrender
import matplotlib.pyplot as plt
import numpy as np
import os

def render_3d_model(file_path, output_folder):
    # Load the 3D model
    mesh = trimesh.load(file_path)

    # Ensure the mesh is loaded correctly
    if mesh.is_empty:
        print("Failed to load 3D model.")
        return

    # Camera setup
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    camera_distance = 2.0  # Distance from object
    camera_pose_template = np.eye(4)

    # Define camera positions and orientations
    views = {
        "front": np.eye(4),  # Default pose (no rotation)
        "back": trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0]),
        "left": trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0]),
        "right": trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]),
        "top": trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]),
        "bottom": trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]),
    }

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Renderer setup
    r = pyrender.OffscreenRenderer(800, 800)

    # Render images for each view
    for view_name, rotation_matrix in views.items():
        # Create a new scene for each view
        scene = pyrender.Scene()

        # Add the mesh to the scene
        render_mesh = pyrender.Mesh.from_trimesh(mesh)
        scene.add(render_mesh)

        # Apply rotation to the camera pose
        camera_pose = np.dot(camera_pose_template, rotation_matrix)
        camera_pose[:3, 3] = np.dot(rotation_matrix[:3, :3], [0, 0, camera_distance])

        # Add the camera and light to the scene
        scene.add(camera, pose=camera_pose)
        light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
        scene.add(light, pose=camera_pose)

        # Render the scene
        color, _ = r.render(scene)

        # Save the image
        output_path = f"{output_folder}/{view_name}.png"
        plt.imsave(output_path, color)

        # Remove all nodes (clear the scene for the next view)
        scene.clear()

    print("Images saved successfully in", output_folder)

# Example Usage
file_path = "path/to/your/model.stl"  # Path to your STL file
output_folder = "output_images"  # Folder to save images
render_3d_model(file_path, output_folder)
