
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone

from .models import Choice, Question
from .models import Author
from .forms import ContactForm
from django.views.generic.edit import FormView


class ContactFormView(FormView):
    template_name = "polls/contact.html"
    form_class = ContactForm
    success_url = "/polls/thanks/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
    
class ContactThanksView(generic.TemplateView):
    template_name = "polls/thanks.html"

class AuthorCreateView(generic.CreateView):
    model = Author
    fields = ["name", "message"]
    template_name = "polls/author_form.html"
    success_url = "/polls/thanks/"

class AuthorUpdateView(generic.UpdateView):
    model = Author
    fields = ["name"]
    template_name = "polls/author_update_form.html"
    success_url = "/thanks/"



class IndexView(generic.ListView):
    template_name = "polls/index.html"

    def get_queryset(self):
    # """
    # Return the last five published questions (not including those set to be
    # published in the future).
    # """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
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


class ResultsView(generic.DetailView):
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

