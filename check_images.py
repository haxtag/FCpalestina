import json
import os

# Charger les maillots
with open('data/jerseys.json', encoding='utf-8') as f:
    jerseys = json.load(f)

# Vérifier les images
with_images = []
without_images = []

for jersey in jerseys:
    thumbnail = jersey.get('thumbnail', '')
    if thumbnail:
        img_path = f"assets/images/jerseys/{thumbnail}"
        if os.path.exists(img_path):
            with_images.append(jersey)
        else:
            without_images.append(jersey)
            print(f"❌ Image manquante: {thumbnail} pour {jersey.get('title', 'Sans titre')}")
    else:
        without_images.append(jersey)
        print(f"⚠️  Pas de thumbnail: {jersey.get('title', 'Sans titre')}")

print(f"\n📊 Résumé:")
print(f"✅ Maillots AVEC images valides: {len(with_images)}")
print(f"❌ Maillots SANS images: {len(without_images)}")
print(f"📦 Total: {len(jerseys)}")
