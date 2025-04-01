import os

from dotenv import load_dotenv
from src import create_app

load_dotenv()

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
