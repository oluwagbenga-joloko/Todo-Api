import os
from api import create_flask_app

app = create_flask_app(os.getenv('ENVIRONMENT'))

if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)

