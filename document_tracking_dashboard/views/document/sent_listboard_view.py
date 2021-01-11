import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from document_tracking.models import SendDocument

from ...model_wrappers import SentDocumentModelWrapper


class SentListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'sent_document_listboard_template'
    listboard_url = 'sent_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fas fa-file"

    model = 'document_tracking.senddocument'
    model_wrapper_cls = SentDocumentModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'sent_documents'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'sent_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def document(self, doc_identifier=None):
        """Reeturn a new contract obj.
        """
        return SentDocumentModelWrapper(SendDocument(doc_identifier=doc_identifier))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_identifier = kwargs.get('doc_identifier', None)



        context.update(
            document=self.document(doc_identifier=doc_identifier),
            sent=SendDocument.objects.filter(
                user_created=self.request.user.username).filter(
                status='sent').count(),
            received=SendDocument.objects.filter(
                user_created=self.request.user.username).filter(
                status='received').count(),
            processing=SendDocument.objects.filter(
                user_created=self.request.user.username).filter(
                status='processing').count(),
            processed=SendDocument.objects.filter(
                user_created=self.request.user.username).filter(
                status='processed').count(),
            all=SendDocument.objects.filter(
                user_created=self.request.user.username).count()

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
