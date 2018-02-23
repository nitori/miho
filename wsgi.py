
import pathlib

from miho import create_app

config_file = pathlib.Path('.').absolute() / 'config.py'
application = create_app(config_file)


if __name__ == '__main__':
    application.run()
