from django.http import HttpRequest, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from ..common.proc_util import exec_iter_subproc, exec_subproc
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import json


@login_required()
def print_journal(request: HttpRequest, svcns: str, svcname: str):
    limit_bytes = 1024 * 1024 * 5  # 5mb
    app_name = svcname
    ns = svcns

    try:
        lines = int(request.GET.get("lines"))
    except:
        lines = 200

    cmd = f"kubectl -n '{ns}' logs --limit-bytes={limit_bytes} --tail={lines} 'deployments/{app_name}'"
    since = request.GET.get("since").lower()

    if since and since.endswith(("m", "h")):
        cmd = f"{cmd} --since={since}"

    response = StreamingHttpResponse(
        exec_iter_subproc(cmd, lines + 10),
        "text/plain; charset=utf-8",
    )
    return response


@login_required()
def index(request: HttpRequest):
    context = {}
    return render(request, "pages/kubic.html", context)


@login_required()
def rescan_services(request: HttpRequest, reload: int = 0):
    key = "kubic:apps"
    if reload == 1:
        cache.delete(key)

    if cache.has_key(key):
        data = cache.get(key)
    else:
        cmd = "kubectl get deployments.apps -A --no-headers"
        data = []
        for line_app in exec_iter_subproc(cmd, 200):
            item = line_app.split()
            if item[0] == "kube-system":
                continue
            data.append({"Name": item[1], "Ns": item[0]})
            print(item)
        cache.set(key, data, 600)

    return JsonResponse({"data": data})
