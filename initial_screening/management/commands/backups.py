import gzip
from io import StringIO
from datetime import datetime
from django.core.management.base import BaseCommand, CommandParser
from django.db import connection 
from typing import Any

class Command(BaseCommand):
    help = "Backup database using PostgreSQL COPY TO"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--output", default=None)

    def handle(self, *args: str, **options: Any):
        filename = options["output"] or (
            f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql.gz"
        )

        with gzip.open(filename, "wt", encoding="utf-8") as f:
            connection.set_autocommit(False)
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
                    cursor.execute("BEGIN")
                    for table in connection.introspection.table_names(cursor):
                        buf = StringIO()
                        cursor.copy_expert(f'COPY "{table}" TO STDOUT WITH (FORMAT csv, HEADER true)', buf)
                        f.write(f"-- {table}\n")
                        f.write(buf.getvalue())
                        f.write("\n")
                    cursor.execute("COMMIT")
            except: 
                connection.rollback()
                raise
            finally:
                connection.set_autocommit(True)
        self.stdout.write(self.style.SUCCESS(f"Backup written to {filename}"))