from main.app import app
import os

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
    app.run(debug=True)