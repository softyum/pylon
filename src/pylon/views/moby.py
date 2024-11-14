import json
from django.http import HttpRequest, HttpResponse, JsonResponse, StreamingHttpResponse
from django.urls import resolve
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..common.proc_util import exec_iter_subproc
from ..models.moby import ServiceApp
from django.core.cache import cache

"""
docker stack ls --format json
docker stack services ns_dev --format json
docker service logs ns_dev_hscrm-api-java -n 200 --since 72h
"""


@login_required()
def print_journal(request: HttpRequest, svcname: str):
    # cmd = "docker logs -n 500 pg-prd-m1"
    cmd = ["docker", "service", "logs", svcname]
    try:
        lines = int(request.GET.get("lines"))
    except:
        lines = 20
    since = request.GET.get("since").lower()
    if since and since.endswith(("m", "h")):
        cmd += ["--since", since]
    else:
        cmd += [f"-n{lines}"]

    response = StreamingHttpResponse(
        exec_iter_subproc(cmd, lines),
        "text/plain; charset=utf-8",
    )
    return response


@login_required()
def rescan_services(request: HttpRequest, reload: int = 0):
    key = "moby:services"
    if reload == 1:
        cache.delete(key)

    if cache.has_key(key):
        data = cache.get(key)
    else:
        cmd = "docker service ls --format json"
        data = []

        for value in exec_iter_subproc(cmd, 100):
            item = json.loads(value)
            data.append(item)
            print(item)
        cache.set(key, data, 600)

    return JsonResponse({"data": data})


@login_required()
def index(request: HttpRequest):
    context = {}
    return render(request, "pages/index.html", context)


@login_required()
def get_services(request: HttpRequest):
    all_objects = ServiceApp.objects.all()
    # clean all data
    # ServiceApp.objects.all().delete()
    # app = ServiceApp(name=item["Name"], image=item["Image"], service_id=item["ID"])
    # app.save()
    page_size = 100
    search_kw = request.GET.get("s", "")
    p1 = request.GET.get("page_num", "1")
    page_number = int(p1) if p1.isdigit() else 1
    if page_number < 1:
        page_number = 1
