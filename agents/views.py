import random
import environ
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail

from agents.forms import AgentModelForm
from agents.mixins import LoginAndAdminRequiredMixin
from leads.models import Agent


env = environ.Env()
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


class AgentListView(LoginAndAdminRequiredMixin,  generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        user_org = self.request.user.organisation
        return Agent.objects.filter(organisation=user_org)


class AgentCreateView(LoginAndAdminRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        print("host:")
        print(self.request.get_host())
        user = form.save(commit=False)
        user.is_agent = True
        user.is_admin = False
        user.set_password(f"{random.randint(10000000, 99999999)}")
        user.save()

        current_user = self.request.user
        Agent.objects.create(
            user=user,
            organisation=current_user.organisation
        )

        subject = "%s invited you to join %s on LeadBoard" % (current_user.first_name, current_user.organisation)
        login_link = "%s/login" % self.request.get_host()
        message = "%s invited you to join %s on LeadBoard. Login to your account to start working.\n%s" % (current_user.first_name, current_user.organisation, login_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginAndAdminRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        user_org = self.request.user.organisation
        return Agent.objects.filter(organisation=user_org)


class AgentUpdateView(LoginAndAdminRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        user_org = self.request.user.organisation
        return Agent.objects.filter(organisation=user_org)

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(LoginAndAdminRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        user_org = self.request.user.organisation
        return Agent.objects.filter(organisation=user_org)

    def get_success_url(self):
        return reverse("agents:agent-list")
