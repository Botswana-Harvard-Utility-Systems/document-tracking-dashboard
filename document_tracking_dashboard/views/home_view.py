from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'document_tracking_dashboard/home.html'
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'Document'
