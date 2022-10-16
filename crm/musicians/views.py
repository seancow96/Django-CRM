import logging
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from bands.mixins import OrganisorAndLoginRequiredMixin
from .models import Musician, Band, Category
from .forms import (
    MusicianForm, 
    MusicianModelForm, 
    CustomUserCreationForm, 
    AssignBandForm, 
    MusicianCategoryUpdateForm,
    CategoryModelForm)


logger = logging.getLogger(__name__)


# CRUD+L - Create, Retrieve, Update and Delete + List


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class MusicianListView(LoginRequiredMixin, generic.ListView):
    template_name = "musicians/musician_list.html"
    context_object_name = "musicians"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Musician.objects.filter(
                organisation=user.userprofile, 
                band__isnull=False
            )
        else:
            queryset = Musician.objects.filter(
                organisation=user.band.organisation, 
                band__isnull=False
            )
            # filter for the band that is logged in
            queryset = queryset.filter(band__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MusicianListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Musician.objects.filter(
                organisation=user.userprofile, 
                band__isnull=True
            )
            context.update({
                "unassigned_musicians": queryset
            })
        return context


def musician_list(request):
    musicians = Musician.objects.all()
    context = {
        "musicians": musicians
    }
    return render(request, "musicians/musician_list.html", context)


class MusicianDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "musicians/musician_detail.html"
    context_object_name = "musician"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Musician.objects.filter(organisation=user.userprofile)
        else:
            queryset = Musician.objects.filter(organisation=user.band.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(band__user=user)
        return queryset


def musician_detail(request, pk):
    musician = Musician.objects.get(id=pk)
    context = {
        "musician": musician
    }
    return render(request, "musicians/musician_detail.html", context)


class MusicianCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "musicians/musician_create.html"
    form_class = MusicianModelForm

    def get_success_url(self):
        return reverse("musicians:musician-list")

    def form_valid(self, form):
        musician = form.save(commit=False)
        musician.organisation = self.request.user.userprofile
        musician.save()
        send_mail(
            subject="A musician has been created",
            message="Go to the site to see the new musician",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a musician")
        return super(MusicianCreateView, self).form_valid(form)


def musician_create(request):
    form = MusicianModelForm()
    if request.method == "POST":
        form = MusicianModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/musicians")
    context = {
        "form": form
    }
    return render(request, "musicians/musician_create.html", context)


class MusicianUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "musicians/musician_update.html"
    form_class = MusicianModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        return Musician.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("musicians:musician-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this musician")
        return super(MusicianUpdateView, self).form_valid(form)


def musician_update(request, pk):
    musician = Musician.objects.get(id=pk)
    form = MusicianModelForm(instance=musician)
    if request.method == "POST":
        form = MusicianModelForm(request.POST, instance=musician)
        if form.is_valid():
            form.save()
            return redirect("/musicians")
    context = {
        "form": form,
        "musician": musician
    }
    return render(request, "musicians/musician_update.html", context)


class MusicianDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "musicians/musician_delete.html"

    def get_success_url(self):
        return reverse("musicians:musician-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        return Musician.objects.filter(organisation=user.userprofile)


def musician_delete(request, pk):
    musician = Musician.objects.get(id=pk)
    musician.delete()
    return redirect("/musicians")


class AssignBandView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "musicians/assign_band.html"
    form_class = AssignBandForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignBandView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("musicians:musician-list")

    def form_valid(self, form):
        band = form.cleaned_data["band"]
        musician = Musician.objects.get(id=self.kwargs["pk"])
        musician.band = band
        musician.save()
        return super(AssignBandView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "musicians/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Musician.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Musician.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "musicians/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "musicians/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("musicians:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "musicians/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("musicians:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "musicians/category_delete.html"

    def get_success_url(self):
        return reverse("musicians:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class MusicianCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "musicians/musician_category_update.html"
    form_class = MusicianCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of musicians for the entire organisation
        if user.is_organisor:
            queryset = Musician.objects.filter(organisation=user.userprofile)
        else:
            queryset = Musician.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("musicians:musician-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        musician_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this musician was converted
            if musician_before_update.category != converted_category:
                # this musician has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(MusicianCategoryUpdateView, self).form_valid(form)


