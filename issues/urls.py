from django.urls import path
from .views import text_sample, json_sample, db_json


urlpatterns = [
    path("text", text_sample, name="issues_text_sample"),
    path("json", json_sample, name="issues_json_sample"),
    path("db/<int:pk>", db_json, name="issues_db_json"),
]
