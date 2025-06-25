from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("thanks/", views.ContactFormView.as_view(), name="thanks"),
    path("author/create/", views.AuthorCreateView.as_view(), name="author-create"),
    path("author/<int:question_id>/update/", views.AuthorUpdateView.as_view(), name="author-update"),
]