import os
import click
from app import db

def register(app):
    @app.cli.group()
    def data_generate():
        """Data generation commands"""
        pass