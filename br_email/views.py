from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Event
from django.core.mail import send_mail


def home(request):
    return render(request, 'br_email/home.html')


class EventListView(ListView):

    context_object_name = 'races'
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('EventDate')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def contact(request):

    context = {
        'title': 'Contact',
        'ind': None
     }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        if form.is_valid():
            context['ind'] = 1
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            send_mail(
                        'RaceReminder-contactform ' + sender,
                        message,
                        'race.reminders@gmail.com',
                        ['race.reminders@gmail.com'],
                        fail_silently=True,
                    )
    else:
        form = ContactForm()
        context['form'] = form
    return render(request, 'br_email/contact.html', context)


def handler404(request, exception=None):
    return render(request, 'br_email/404.html', status=404)


def handler500(request, exception=None):
    return render(request, 'br_email/500.html', status=500)