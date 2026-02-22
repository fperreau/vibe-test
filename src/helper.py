#! /usr/bin/env python.exe
##
#   NAS Helper Script
#
#   New-Alias incus .\helper.py
#   Remove-Alias incus
#
##

import typer
from nas import NAS
from share import Share
from user import User

app = typer.Typer()
nas_app = typer.Typer()
share_app = typer.Typer()
user_app = typer.Typer()

app.add_typer(nas_app, name="nas")
nas_app.add_typer(share_app, name="share")
nas_app.add_typer(user_app, name="user")

@nas_app.command()
def list():
    NAS.list()
@nas_app.command()
def create(name: str):
    NAS.create(name)
@nas_app.command()
def delete(name: str):
    NAS.delete(name)
@nas_app.command()
def use(name: str):
    NAS.use(name)
@share_app.command()
def list():
    Share.list()
@share_app.command()
def create(share_name: str, source: str, share_type: str):
    Share.create(share_name, source, share_type)
@share_app.command()
def delete(name: str):
    Share.delete(name)
@user_app.command()
def list():
    User.list()
@user_app.command()
def create(user: str, password: str):
    User.create(user, password)
@user_app.command()
def delete(user: str):
    User.delete(user)
@user_app.command()
def owner(user: str, share: str):
    User.owner(user, share)
if __name__ == "__main__":
    app()
