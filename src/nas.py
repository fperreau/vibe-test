import typer

class Helper:
    name = None

    def __init__(self, name):
        self.name = name

class NAS(Helper):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def list():
        typer.echo("Listing NAS devices")

    @staticmethod
    def create(name: str):
        NAS.name = name
        typer.echo(f"Creating NAS device: {name}")

    @staticmethod
    def delete(name: str):
        typer.echo(f"Deleting NAS device: {name}")

    @staticmethod
    def use(name: str):
        typer.echo(f"Using NAS device: {name}")