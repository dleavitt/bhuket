from flask.ext.script import Manager
from flask.ext.assets import ManageAssets
from app import app

manager = Manager(app)

manager.add_command("assets", ManageAssets())

# heroku runs collectstatic upon deployment
manager.add_command("collectstatic", ManageAssets())

if __name__ == "__main__":
    manager.run()
