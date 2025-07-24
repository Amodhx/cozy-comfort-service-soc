from flask import Flask
from flask_cors import CORS 
from routes import api_routes 
from flask import send_from_directory
import os


app = Flask(__name__)
CORS(app) 
app.register_blueprint(api_routes, url_prefix="/cozy_comfort") 

@app.route('/')
def home():
    return "Welcome to Cozy Comfort API!"


@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(upload_folder, filename)

if __name__ == '__main__':
    print("Seller SERVER Started ON : port 3002 :!")
    app.run(debug=True, port=3002)
