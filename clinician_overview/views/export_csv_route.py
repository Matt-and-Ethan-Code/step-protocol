import csv
from django.http import HttpRequest, HttpResponse
import json

def export_csv_route(request: HttpRequest, client_id:str) -> HttpResponse:
    data = json.loads(request.body)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    writer.writerow(data["headers"])

    for row in data["rows"]:
        writer.writerow(row)

    return response
