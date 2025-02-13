from flask import Flask, request, jsonify
import os
from samsungtvws import SamsungTVWS

app = Flask(__name__)

# Replace with your TV's local IP address.
TV_IP = "192.168.1.100"  # Update this with your actual TV IP

def upload_image(image_path):
    """
    Connects to the TV and uploads the image.
    Returns the response from the TV or an error message.
    """
    try:
        tv = SamsungTVWS(host=TV_IP)
        art = tv.art()
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        # Note: Using only 'matte' since 'portrait_matte' isn't supported.
        response = art.upload(
            image_data,
            file_type="JPEG",
            matte="flexible_apricot"
        )
        return {"success": True, "response": response}
    except Exception as e:
        return {"error": str(e)}

@app.route("/upload", methods=["POST"])
def upload():
    """
    Expects a JSON payload with a key "image_path" that provides
    the full path to the image file.
    """
    data = request.get_json()
    if not data or "image_path" not in data:
        return jsonify({"error": "No image_path provided"}), 400

    image_path = data["image_path"]
    if not os.path.exists(image_path):
        return jsonify({"error": "File not found"}), 404

    result = upload_image(image_path)
    return jsonify(result)

if __name__ == "__main__":
    # Run the server on port 5000 (or any free port you choose)
    app.run(port=5000)
