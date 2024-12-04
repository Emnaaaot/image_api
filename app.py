
from flask import Flask, request, jsonify
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Utiliser une clé API depuis un fichier d'environnement pour plus de sécurité
API_KEY = os.getenv("STABILITY_API_KEY", "sk-HZiNPQvTfwh68RsYEE1kUeeH6TRth7Sn5npEwDgPKXlYoFUY")

# Stockage local des URLs d'images générées
image_history = []

@app.route("/generate-image", methods=["POST"])
def generate_image():
    """Endpoint pour générer une image."""
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Envoi de la requête à l'API Stability AI avec multipart/form-data
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/ultra",  # Correct API endpoint
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Accept": "image/*",  # Accept image as response
            },
            files={  # Using 'files' to send multipart/form-data
                "prompt": (None, prompt),
                "output_format": (None, "webp"),
                "cfg_scale": (None, "7"),
                "clip_guidance_preset": (None, "FAST_BLUE"),
                "height": (None, "512"),
                "width": (None, "512"),
                "samples": (None, "1"),
                "steps": (None, "50"),
            },
        )

        # Vérifier la réponse de l'API
        if response.status_code == 200:
            image_name = f"generated_image_{int(time.time())}.webp"
            image_path = os.path.join("static", image_name)
            with open(image_path, 'wb') as file:
                file.write(response.content)

            image_url = f"/static/{image_name}"
            image_history.append(image_url)
            return jsonify({"image_url": image_url}), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/image-history", methods=["GET"])
def get_image_history():
    """Endpoint pour récupérer l'historique des images générées."""
    return jsonify({"image_history": image_history})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)

print(f"API Key Loaded: {API_KEY}")
