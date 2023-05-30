"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    """Django command to wait for database."""
    
    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("waiting for database...")
        db_up = False
        while not db_up:
            try:
                # Try to connect to the default database
                connection = connections['default']
                connection.cursor()
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 5 seconds...")
                time.sleep(5)
            else:
                self.stdout.write(self.style.SUCCESS("Database ready"))
                db_up = True
