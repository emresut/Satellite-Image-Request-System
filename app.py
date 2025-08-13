from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os
from auth.routes import auth_bp
from image_requests.routes import image_requests_bp

app = Flask(__name__, static_folder="frontend/build", static_url_path="/")

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(image_requests_bp)

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    build_dir = os.path.join(os.getcwd(), "frontend", "build")

    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, "index.html")

if __name__ == "__main__":
    app.run(debug=False)