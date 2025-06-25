from django.urls import path
from .views import AuthorUpdateView    
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("thanks/", views.ContactFormView.as_view(), name="thanks"),
    path("create/", views.AuthorCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.AuthorUpdateView.as_view(),name="update"),
    path("<int:pk>/delete/", views.AuthorDeleteView.as_view(), name="delete"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)