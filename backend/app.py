from app.xd import create_app
from config import config

configuracion = config['development']
app = create_app(configuracion)

if __name__ == '__main__':
    app.run()