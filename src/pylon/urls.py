from django.urls import path
from .views import moby, kubic
from .views.auth import require_login

app_name = "pods"
urlpatterns = [
    path("authority/", require_login, name="authority"),
    # ex: /polls/
    path("", moby.index, name="moby_index"),
    path("moby/svcscan/<int:reload>", moby.rescan_services, name="moby_svcscan"),
    path("moby/logs/<str:svcname>/", moby.print_journal, name="moby_journal"),
    # ex: /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path("kubic/", kubic.index, name="kubic_index"),
    path("kubic/api/svcscan/<int:reload>", kubic.rescan_services, name="kubic_svcscan"),
    path("kubic/api/logs/<str:svcns>/<str:svcname>/", kubic.print_journal, name="kubic_journal"),
]
