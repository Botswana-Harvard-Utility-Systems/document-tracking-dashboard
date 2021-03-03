from django.views.generic.base import TemplateView
from django.contrib.auth.models import Group

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'document_tracking_dashboard/home.html'
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'Document'

    groups = Group.objects.all()

    @property
    def is_receptionist(self):
        reception_groups = ['BHP HQ', 'Finance Reception', 'CTU Reception']
        return self.request.user.groups.filter(
            name__in=reception_groups).count() != 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            is_receptionist=self.is_receptionist
        )
        return context

