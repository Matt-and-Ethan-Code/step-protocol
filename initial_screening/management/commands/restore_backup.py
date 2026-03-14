from django.core.management.base import BaseCommand, CommandParser
from io import StringIO
from collections.abc import Generator
from typing import Any, IO
from django.db import connection
import gzip
from django.db import transaction

def parse_backup(f: IO[str]) -> Generator[tuple[str, str], None, None]:
    current_table = None 
    current_lines: list[str] = []

    for line in f: 
        if line.startswith("-- "):
            if current_table is not None:
                yield current_table, "".join(current_lines)
            current_table = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_table is not None:
        yield current_table, "".join(current_lines)


class Command(BaseCommand):
    help = "Restore database backup."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--input", default=None, required=True)

    def handle(self, *args: str, **options: Any):
        filename: str = options["input"] 
        with gzip.open(filename, "rt", encoding="utf-8") as f:
            with connection.cursor() as cursor:
                with transaction.atomic():
                    for table, csv_data in parse_backup(f):
                        buf = StringIO(csv_data)
                        cursor.copy_expert(f'COPY "{table}" FROM STDIN WITH (FORMAT csv, HEADER true)', buf)