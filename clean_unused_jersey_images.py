import os
import json

# Chemins
JERSEYS_JSON = os.path.join('data', 'jerseys.json')
IMAGES_DIR = os.path.join('assets', 'images', 'jerseys')

# Charger les images utilisées dans les maillots
with open(JERSEYS_JSON, encoding='utf-8') as f:
    jerseys = json.load(f)

used_images = set()
for jersey in jerseys:
    img = jersey.get('image')
    if img:
        # On ne garde que le nom de fichier, pas le chemin complet
        used_images.add(os.path.basename(img))

# Lister toutes les images du dossier
all_images = set(os.listdir(IMAGES_DIR))

# Images à supprimer
unused_images = all_images - used_images

print(f"Images utilisées: {len(used_images)}")
print(f"Images dans le dossier: {len(all_images)}")
print(f"Images à supprimer: {len(unused_images)}")

for img in unused_images:
    img_path = os.path.join(IMAGES_DIR, img)
    try:
        os.remove(img_path)
        print(f"Supprimé: {img}")
    except Exception as e:
        print(f"Erreur suppression {img}: {e}")

print("Nettoyage terminé.")
