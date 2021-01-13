import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from document_tracking.models import Document

from .filters import DocumentViewFilters
from ...model_wrappers import DocumentModelWrapper


class DocumentListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'document_listboard_template'
    listboard_url = 'document_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = "fas fa-file"
    listboard_view_filters = DocumentViewFilters()

    model = 'document_tracking.document'
    model_wrapper_cls = DocumentModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'documents'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'document_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def document(self, doc_identifier=None):
    #     """Returns a document obj
    #     """
    #     return DocumentModelWrapper(Document(doc_identifier=doc_identifier))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_identifier = kwargs.get('doc_identifier', None)
        context.update(
            soft_copy=Document.objects.filter(
                user_created=self.request.user.username).filter(
                document_form='soft_copy').count,
            hard_copy=Document.objects.filter(
                user_created=self.request.user.username).filter(
                document_form='hard_copy').count,
            contracts=Document.objects.filter(
                user_created=self.request.user.username).filter(
                document_type='contract').count,
            letters=Document.objects.filter(
                user_created=self.request.user.username).filter(
                document_form='letter').count,
            reports=Document.objects.filter(
                user_created=self.request.user.username).filter(
                document_form='report').count,
            document_add_url=self.model_cls().get_absolute_url()
        )
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('doc_identifier'):
            options.update(
                {'doc_identifier': kwargs.get('doc_identifier')})
        options.update({'user_created': request.user.username})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q
