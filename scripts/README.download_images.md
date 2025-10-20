Demo image population (Render)

This script fills missing jersey images for the demo environment on Render.

Behavior:
- Reads data/jerseys.json.
- If legacy fields image_url + image exist, it downloads from the URL.
- Otherwise, for the current schema (thumbnail + images[] as filenames), it creates placeholder files under assets/images/jerseys/<filename> so the frontend can render without 404s.
- Ensures a placeholder.jpg exists in both assets/img/ and assets/images/jerseys/.

Dependencies:
- Uses Pillow (PIL) to generate a simple JPEG placeholder; falls back to a remote placeholder if Pillow is missing.

Notes:
- Render has an ephemeral filesystem; generated files are lost on redeploy. This is fine for demo. For production, store media in persistent storage (S3, Cloud Storage, etc.).