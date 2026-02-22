import typer

class User:
    @staticmethod
    def list():
        typer.echo("Listing users")

    @staticmethod
    def create(user: str, password: str):
        typer.echo(f"Creating user: {user} with password {password}")

    @staticmethod
    def delete(user: str):
        typer.echo(f"Deleting user: {user}")

    @staticmethod
    def owner(user: str, share: str):
        typer.echo(f"Setting user {user} as owner of share {share}")