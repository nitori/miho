
import pathlib
import shutil

import click

from miho import create_app, utils

config_file = pathlib.Path('.').absolute() / 'config.py'
app = create_app(config_file)


@app.cli.command()
def reset():
    images_dir = utils.get_images_dir()
    click.confirm(f'This will delete all files in {str(images_dir)!r}. Continue?', abort=True, default=False)
    if images_dir.exists() and not images_dir.is_dir():
        click.echo(f'{str(images_dir)!r} is not a directory.', err=True)
        return

    if images_dir.exists():
        shutil.rmtree(images_dir)

    images_dir.mkdir(0o755, exist_ok=True)
    pathlib.Path(images_dir, 'thumbs').mkdir(0o755, exist_ok=True)
    pathlib.Path(images_dir, '.keep').touch(0o644, exist_ok=True)
    pathlib.Path(images_dir, 'thumbs', '.keep').touch(0o644, exist_ok=True)


if __name__ == '__main__':
    app.run()
