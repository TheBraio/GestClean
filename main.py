from config import app, db, login_manager
from routes import blueprints
from dotenv import load_dotenv
from models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

for rota, blueprint in blueprints.items():
    app.register_blueprint(blueprint, url_prefix=f'/{rota}')



load_dotenv(".flaskenv")
if __name__ == "__main__":
    app.run(debug=True)
