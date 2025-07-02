import os
import shutil
import numpy as np
from PIL import Image
from pygltflib import GLTF2, Image as GLTFImage, Texture, Material, PbrMetallicRoughness, Sampler

# === CONFIG ===
INPUT_DIR = "input"
STATIC_DIR = "static"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Step 1: Modify GLB with textures ===
gltf_path = os.path.join(STATIC_DIR, "traditional_saree.glb")
gltf = GLTF2().load(gltf_path)

# Texture mapping
texture_map = {
    "pallu": os.path.join(INPUT_DIR, "blouse.png"),
    "body": os.path.join(INPUT_DIR, "body.png"),
    "blouse": os.path.join(INPUT_DIR, "body.png")
}

# Ensure at least one sampler exists
if not hasattr(gltf, "samplers") or gltf.samplers is None:
    gltf.samplers = []
if len(gltf.samplers) == 0:
    gltf.samplers.append(Sampler())

SCALE_FACTOR = 10  # Change this to your desired scale (e.g., 2.0 for double size)

for i, (part, tex_path) in enumerate(texture_map.items()):
    texture_name = f"{part}_texture.png"
    out_path = os.path.join(OUTPUT_DIR, texture_name)

    if part == "blouse":
        # Open, scale, and save the blouse texture
        img = Image.open(tex_path)
        new_size = (int(img.width * SCALE_FACTOR), int(img.height * SCALE_FACTOR))
        img = img.resize(new_size, Image.LANCZOS)
        img.save(out_path)
    else:
        shutil.copy(tex_path, out_path)

    # Ensure gltf.images has enough entries
    while len(gltf.images) <= i:
        gltf.images.append(GLTFImage())
    gltf.images[i].uri = texture_name

    # Ensure gltf.textures has enough entries
    while len(gltf.textures) <= i:
        gltf.textures.append(Texture())
    gltf.textures[i] = Texture(sampler=0, source=i)

    # Ensure gltf.materials has enough entries
    while len(gltf.materials) <= i:
        gltf.materials.append(Material())
    gltf.materials[i].pbrMetallicRoughness = PbrMetallicRoughness(
        baseColorTexture={"index": i}
    )

# Save updated GLB
updated_glb_path = os.path.join(OUTPUT_DIR, "textured_saree.glb")
gltf.save(updated_glb_path)
print(f"✅ Textured GLB saved to: {updated_glb_path}")

# === Step 2: Render GLB to PNG ===
# The following code requires OpenGL and may not work in headless environments.
# Commenting out for headless/cloud environments.
# import trimesh
# import pyrender
# scene = trimesh.load(updated_glb_path)
# render_scene = pyrender.Scene.from_trimesh_scene(scene)
# camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
# cam_pose = np.array([
#     [1, 0, 0, 0],
#     [0, 1, 0, 1.5],
#     [0, 0, 1, 3],
#     [0, 0, 0, 1]
# ])
# render_scene.add(camera, pose=cam_pose)
# light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
# render_scene.add(light, pose=np.eye(4))
# renderer = pyrender.OffscreenRenderer(800, 600)
# color, _ = renderer.render(render_scene)
# rendered_path = os.path.join(OUTPUT_DIR, "saree_preview.png")
# Image.fromarray(color).save(rendered_path)
# print(f"🖼️ Preview image saved to: {rendered_path}")
