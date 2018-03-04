#!/usr/bin/env python3

import pathlib
import os
import sys
from urllib.parse import quote

import click
import requests
from requests.auth import HTTPBasicAuth

try:
    authentication = HTTPBasicAuth(
        os.environ['MIHO_API_USER'],
        os.environ['MIHO_API_PASS']
    )
except KeyError:
    print('Environment variables MIHO_API_USER and MIHO_API_PASS must be set.')
    sys.exit(1)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
def upload(filename):

    path = pathlib.Path(filename).absolute()
    if not path.exists():
        raise FileNotFoundError(f'No such file {filename!r}.')
    if path.is_dir():
        raise IsADirectoryError(f'{filename!r} is a directory.')

    # curl -u "$AUTH" -F "image=@$2" https://img.chireiden.net/api/upload
    with path.open('rb') as fh:
        r = requests.post(
            'https://img.chireiden.net/api/upload',
            files={'image': fh},
            auth=authentication
        )
    print(r)
    print(r.text)


@cli.command()
@click.argument('id_or_filename')
def delete(id_or_filename):
    # curl -X DELETE -u "$AUTH" "https://img.chireiden.net/api/delete/$2"
    id_or_filename = quote(id_or_filename)
    r = requests.delete(
        f'https://img.chireiden.net/api/delete/{id_or_filename}',
        auth=authentication
    )
    print(r)
    print(r.text)


if __name__ == '__main__':
    try:
        cli()
    except (FileNotFoundError, IsADirectoryError) as exc:
        print(exc)
