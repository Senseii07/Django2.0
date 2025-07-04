
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .models import Choice, Question
from .models import Author
from .forms import ContactForm
from django.views.generic.edit import FormView
# Create your views here.


class ContactFormView(FormView):
    template_name = "polls/contact.html"
    form_class = ContactForm
    success_url = "/polls/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
    
class ContactThanksView(FormView):
    template_name = "polls/thanks.html"

class AuthorCreateView(CreateView):
    model = Author
    fields = ["name", "message"]
    template_name = "polls/author_form.html"
    success_url = "/polls/thanks/"

class AuthorUpdateView(UpdateView):
    model = Question
    fields = ["question_text","image"]

    template_name = "polls/author_update_form.html"

    def get_success_url(self):
        return reverse("polls:index")
    
class AuthorDeleteView(DeleteView):
    model = Question
    template_name = "polls/author_confirm_delete.html"

    def get_success_url(self):
        return reverse("polls:index")

class IndexView(ListView):
    template_name = "polls/index.html"

    def get_queryset(self):
    # """
    # Return the last five published questions (not including those set to be
    # published in the future).
    # """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(DetailView):
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["question_list"] = Question.objects.all()
        return context


class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

