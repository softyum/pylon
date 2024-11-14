from django.http import HttpRequest, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from ..common.proc_util import exec_iter_subproc
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import json


@login_required()
def print_journal(request: HttpRequest):
    tail = 1000
    limit_bytes = 1024 * 1024 * 5  # 5mb
    app_name = "whoami"
    ns = "default"
    cmd = f"kubectl -n '{ns}' logs --limit-bytes={limit_bytes} -n {tail} 'deployments/{app_name}'"

    return StreamingHttpResponse(
        exec_iter_subproc(cmd),
        "text/plain; charset=utf-8",
    )


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
        cmd = "kubectl get deployments.apps -A -o json"
        data = []

        for value in exec_iter_subproc(cmd, 100):
            item = json.loads(value)
            data.append(item)
            print(item)
        cache.set(key, data, 600)

    return JsonResponse({"data": data})
