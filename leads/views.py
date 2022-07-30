from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import LoginAndAdminRequiredMixin

from leads.forms import LeadForm, LeadModelForm
from .models import Agent, Category, Lead
from .forms import AssignAgentForm, CustomUserCreationForm, LeadCategoryUpdateForm


class LandingPageView(generic.TemplateView):
    template_name = "landing_page.html"


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(agent__isnull=False)

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation, agent__user=user)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_admin:
            unassigned_leads = Lead.objects.filter(organisation=user.organisation, agent__isnull=True)
            context.update({
                "unassigned_leads":unassigned_leads
            })
        return context
    


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation, agent__user=user)
        
        return queryset


class LeadCreateView(LoginAndAdminRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # Send email on new lead creation
        send_mail(
            subject="A new lead has been created",
            message="Go to the LeadBoard to view the newly created lead.",
            from_email="info@leadboard.com",
            recipient_list=["user@gmail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(LoginAndAdminRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.organisation)

    def get_success_url(self):
        return reverse("leads:lead-list")


class LeadDeleteView(LoginAndAdminRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.organisation)

    def get_success_url(self):
        return reverse("leads:lead-list")


class AssignAgentView(LoginAndAdminRequiredMixin, generic.FormView):
    template_name = "leads/agent_assign.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation)

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation)
        
        return queryset


class CategoryDetailView(generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     queryset = self.get_object().leads.all()

    #     context.update({
    #         "leads": queryset
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.all()

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation)
        
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.all()

        if user.is_admin:
            queryset = queryset.filter(organisation=user.organisation)
        elif user.is_agent:
            queryset = queryset.filter(organisation=user.agent.organisation, agent__user=user)
        
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})