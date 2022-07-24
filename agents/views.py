from django.urls import reverse
from django.views import generic
from agents.forms import AgentModelForm
from agents.mixins import LoginAndAdminRequiredMixin
from leads.models import Agent


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
        agent = form.save(commit=False)
        agent.organisation = self.request.user.organisation
        agent.save()
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
