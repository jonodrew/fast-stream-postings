from app import create_app, db, cli
from app.models import Role
import click
from flask import url_for

app = create_app()
cli.register(app)



@app.cli.command()
@click.argument('name')
def print_name(name):
    """Prints a user's name"""
    print('Hello ' + name)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Role': Role}


