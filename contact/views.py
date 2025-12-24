from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success')

    def form_valid(self, form):
        # save to DB
        form.save()
        # send notification email (placeholder - requires email settings)
        try:
            send_mail(
                f"New contact: {form.cleaned_data.get('subject')}",
                form.cleaned_data.get('message'),
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        return super().form_valid(form)


from django.views.generic import TemplateView


class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'
