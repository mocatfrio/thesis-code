# application imports

from flask_script import Manager, Server
from app import app

manager = Manager(app)

manager.add_command("run", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = '8991')
)

if __name__ == '__main__':
    manager.run()
