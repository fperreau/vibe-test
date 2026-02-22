#! /usr/bin/env python.exe
##
#   NAS Helper Script
#
#   New-Alias incus .\helper.py
#   Remove-Alias incus
##

import typer
import helper as HR

#
# CLI - nas [user, share]
#
app_nas = typer.Typer()
app_nas.add_typer(HR.user_app, name="user")

share_app = typer.Typer()
app_nas.add_typer(share_app, name="share")

@app_nas.command()
def list():
    NAS.list()

@app_nas.command()
def create(name: str):
    NAS.create(name)

@app_nas.command()
def delete(name: str):
    NAS.delete(name)

@app_nas.command()
def use(name: str):
    NAS.use(name)

#
# Share Class
#
@share_app.command()
def list():
    Share.list()

@share_app.command()
def create(share: str, source: str, type: str):
    Share.create(share, source, type)

@share_app.command()
def delete(name: str):
    Share.delete(name)

#
# NAS Class
#
class NAS(HR.Helper):
    
    def __init__(self, name):
        super().__init__(name)

    def list():
        typer.echo("Listing NAS devices")

    def create(name: str):
        HR.Helper.create(name)
        typer.echo(f"Creating NAS device: {name}")

    def delete(name: str):
        typer.echo(f"Deleting NAS device: {name}")

#
#  Share Class
#
class Share(NAS):
    dShare = {} # Use a dictionary to store shares by name

    def __init__(self, share, source, mount_point, user, type):
        super().__init__(NAS.name)
        Share.dShare[share] = self
        self.source = source
        self.mount_point = mount_point
        self.user = user
        self.type = type
    
    def __str__(self):
        return f"share: {self.name}, source: {self.source}, mount_point: {self.mount_point}, owner: {self.user}, type: {self.type}"

    def list():
        typer.echo("Listing shares")
        i = 0
        for obj in Share.dShare.values():
            i += 1
            typer.echo(f"id: {i}, {obj.__str__()}")   

    def create(name: str, source: str, mount_point: str, user=None, type="cifs"):
        obj = Share(name, source, mount_point, user, type)
        Share.dShare[name] = obj
        typer.echo(f"Created share: {obj.__str__()}")

    def delete(name: str):

        typer.echo(f"Deleting share: {name}")

    def owner(user: str):
        typer.echo(f"Setting user {user} as owner of share {share}")

#
#   Main
#
if __name__ == "__main__":
    app_nas()