import os

from dotenv import load_dotenv

from app import create_app
from app.ext.extensions import db

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'default'))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'app': app}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
