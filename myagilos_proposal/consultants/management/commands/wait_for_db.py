"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""
    
    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 seoncd...")
                time.sleep(1)
            else:
                self.stdout.write(self.style.SUCCESS("Database ready"))
                db_up = True