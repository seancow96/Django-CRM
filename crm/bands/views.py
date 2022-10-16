from django.shortcuts import render
from django.core.mail import send_mail
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from musicians.models import Band
from .forms import BandModelForm
from .mixins import OrganisorAndLoginRequiredMixin
import random 

# Create your views here.

class BandsListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name: str = "bands/band_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Band.objects.filter(organisation=organisation)

class BandCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "bands/band_create.html"
    form_class = BandModelForm

    def get_success_url(self):
        return reverse("bands:band-list")
    

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Band.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be a band",
            message="You were added as a band on DJCRM. Please come login to start working.",
            from_email="band@test.com",
            recipient_list=[user.email]
        )
        return super(BandCreateView, self).form_valid(form)

class BandDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "bands/band_detail.html"
    context_object_name = "band"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Band.objects.filter(organisation=organisation)

class BandUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "bands/band_update.html"
    form_class = BandModelForm

    def get_success_url(self):
        return reverse("bands:band-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Band.objects.filter(organisation=organisation)

class BandDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "bands/band_delete.html"
    context_object_name = "band"

    def get_success_url(self):
        return reverse("bands:band-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Band.objects.filter(organisation=organisation)