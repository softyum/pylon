from django.http import HttpRequest, JsonResponse, StreamingHttpResponse
from ..common.proc_util import exec_iter_subproc
from django.urls import resolve
from django.contrib.auth.decorators import login_required


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
