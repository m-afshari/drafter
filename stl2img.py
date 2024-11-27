import trimesh
import pyrender
import matplotlib.pyplot as plt
import numpy as np

def render_3d_model(file_path, output_folder):
    # Load the 3D model
    mesh = trimesh.load(file_path)

    # Ensure the file is loaded correctly
    if not mesh.is_empty:
        # Create a pyrender scene
        scene = pyrender.Scene()
        # Convert trimesh to pyrender mesh
        render_mesh = pyrender.Mesh.from_trimesh(mesh)
        scene.add(render_mesh)

        # Define camera positions (top, right, left, front)
        views = {
            "top": np.array([0, 1, 0]),
            "bottom": np.array([0, -1, 0]),
            "left": np.array([-1, 0, 0]),
            "right": np.array([1, 0, 0]),
            "front": np.array([0, 0, 1]),
            "back": np.array([0, 0, -1]),
        }

        for view_name, direction in views.items():
            # Set up camera
            camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
            camera_pose = np.eye(4)
            camera_pose[:3, 3] = direction * 2  # Adjust distance
            scene.add(camera, pose=camera_pose)

            # Set up light source
            light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
            scene.add(light, pose=camera_pose)

            # Render the scene
            r = pyrender.OffscreenRenderer(800, 800)
            color, _ = r.render(scene)

            # Save the image
            output_path = f"{output_folder}/{view_name}.png"
            plt.imsave(output_path, color)

            # Clean up
            scene.remove_node(scene.get_nodes(name="camera")[-1])
            scene.remove_node(scene.get_nodes(name="light")[-1])

        print("Images saved successfully.")
    else:
        print("Failed to load 3D model.")

# Example Usage
file_path = "path/to/your/model.stl"  # Path to your STL file
output_folder = "output_images"  # Folder to save images
render_3d_model(file_path, output_folder)
