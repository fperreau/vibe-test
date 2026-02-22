import typer

app = typer.Typer()
nas_app = typer.Typer()
share_app = typer.Typer()
user_app = typer.Typer()



#
# CLI - user
#

user_app = typer.Typer()

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

#
# Helper Class
#
class Helper:
    name = None

    def __init__(self, name):
        self.name = name
        
    @staticmethod 
    def create(name: str):
        Helper.name = name 

#
# User Class
#
class User:
    dUsers = {}

    def __init__(self, name):
        User.dUsers[name] = self

    @staticmethod
    def list():
        typer.echo("Listing users")
        for user in User.dUsers:
            typer.echo(user)

    @staticmethod
    def create(user: str, password: str):
        typer.echo(f"Creating user: {user} with password {password}")

    @staticmethod
    def delete(user: str):
        typer.echo(f"Deleting user: {user}")
        User.dUsers.pop(user)
