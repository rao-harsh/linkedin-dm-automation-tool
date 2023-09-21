from django.shortcuts import render, HttpResponse
from .utils import connect_and_send_message
import os
# Create your views here.


def index(request):

    if request.method == "POST":
        print(request.POST["email"])
        print(request.POST["password"])
        print(request.FILES["excel_file"].name)
        print(request.POST["run_type"])
        print(request.POST["delay"])

        email = request.POST["email"]
        password = request.POST["password"]
        run_type = request.POST["run_type"]
        delay = request.POST["delay"]

        if run_type == "seq":
            auto_delay = False
            delay = int(delay)
        else:
            auto_delay = True
            delay = 0

        file_name = request.FILES["excel_file"].name
        file_path = f"./linkedin_scraper/{file_name}"

        with open(file_path, "wb") as f:
            f.write(request.FILES["excel_file"].read())

        successful_count, unsuccessful_count, file_paths = connect_and_send_message(
            email=email, password=password, file_path=file_path, auto_delay=auto_delay, delay=delay)
        print(file_paths)

        os.remove(file_path)
        total_transactions = successful_count + unsuccessful_count
        data = {"total_transactions": total_transactions, "total_successful": successful_count,
                "total_unsuccessful": unsuccessful_count, "file_paths": file_paths}
        return render(request, "index.html", data)

    return render(request, "index.html")


def download_report(request):
    external_file_path = request.GET["file"]
    if os.path.exists(external_file_path):
        file_name = os.path.basename(external_file_path)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        with open(external_file_path, "rb") as f:
            response.write(f.read())

        return response
