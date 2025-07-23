from flask import Flask
from routes import api_routes 

app = Flask(__name__)
app.register_blueprint(api_routes, url_prefix="/cozy_comfort") 

@app.route('/')
def home():
    return "Welcome to Cozy Comfort API!"

if __name__ == '__main__':
    print("Seller SERVER Started ON : port 3000 :!")
    app.run(debug=True, port=3000)
