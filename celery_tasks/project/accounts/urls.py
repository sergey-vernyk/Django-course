from django.urls import path

from . import views

urlpatterns = [
    path("long_task/", views.run_long_task, name="long_task"),
    path("calculate/", views.run_calculation, name="calculation"),
    path("random/", views.run_unstable_task, name="random"),
    path("hash_passwords/", views.run_hashing_passwords_task, name="hashing"),
    path("get_result/<uuid:task_id>/", views.get_task_result, name="task_result"),
]
