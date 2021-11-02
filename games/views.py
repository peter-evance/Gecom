from django.shortcuts import render,reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                            CreateView,
                            ListView,
                            DetailView,                    
                                )
from .models import CategoryModel, GamesModel, OrganisationModel

from games.forms import GameCreationForm,OrganisationCreationForm

class GamesListView(ListView):
    template_name="games/games_list.html"
    context_object_name="games"
    paginate_by=16
    queryset=GamesModel.objects.all()


class GamesDetailView(DetailView):
      template_name="games/games_detail.html"
      context_object_name="game"
      model=GamesModel


class GamesCreateView(LoginRequiredMixin ,CreateView):
    template_name="games/games_create.html"
    form_class=GameCreationForm

    def get_form_kwargs(self,**kwargs):
        kwargs=super(GamesCreateView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("home")

class OrganisationCreateView(LoginRequiredMixin ,CreateView):
    template_name="games/organisation_create.html"
    form_class=OrganisationCreationForm
    
    def form_valid(self,form):
        organisation = form.save(commit=False)
        organisation.owner = self.request.user
        organisation.save()

        return super(OrganisationCreateView,self).form_valid(form)

    def get_success_url(self):
        return reverse("home")

class PublisherDetailView(DetailView):
    template_name="games/publisher_detail.html"
    model=OrganisationModel
    context_object_name="publisher"
    slug_url_kwarg = "name"
    slug_field = "name"

    def get_context_data(self,**kwargs):
        context=super(PublisherDetailView,self).get_context_data(**kwargs)
        games=self.get_object().GameModel_OrganisationModel.all()              
        context["games"]=games
        return context

class CategoryDetailView(DetailView):
    template_name="games/category_detail.html"
    model=CategoryModel
    context_object_name="category"
    slug_url_kwarg = "name"
    slug_field = "name"

    def get_context_data(self,**kwargs):
        context=super(CategoryDetailView,self).get_context_data(**kwargs)
        games=self.get_object().GameModel_CategoryModel.all()              
        context["games"]=games
        return context
