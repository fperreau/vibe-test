import typer
from nas import NAS

class Share(NAS):
    def __init__(self, share_name, source, share_type):
        super().__init__(NAS.name)
        self.share_name = share_name
        self.source = source
        self.share_type = share_type

    @staticmethod
    def list():
        typer.echo("Listing shares")

    @staticmethod
    def create(share_name: str, source: str, share_type: str):
        share = Share(share_name, source, share_type)
        typer.echo(f"Creating share: {share.name} with name {share_name}, source {source}, type {share_type}")

    @staticmethod
    def delete(name: str):
        typer.echo(f"Deleting share: {name}")