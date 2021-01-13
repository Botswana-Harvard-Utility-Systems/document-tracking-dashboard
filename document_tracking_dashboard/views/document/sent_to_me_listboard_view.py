import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from django.http import HttpResponseRedirect
from django.urls import reverse

from document_tracking.models import SendDocument
from document_tracking.forms import SendDocumentForm
from .filters import SentDocumentViewFilters
from ...model_wrappers import SentDocumentModelWrapper


class SentToMeViewError(Exception):
    pass


class SentToMeListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'sent_to_me_listboard_template'
    listboard_url = 'sent_to_me_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = "fas fa-file"

    model = 'document_tracking.senddocument'
    model_wrapper_cls = SentDocumentModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'documents_sent_to_me'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'sent_to_me_listboard_url'
    listboard_view_filters = SentDocumentViewFilters()

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
            doc_identifier=doc_identifier,
            document=self.document(doc_identifier=doc_identifier),
            sent=SendDocument.objects.filter(
                send_to=self.request.user.id).filter(
                status='sent').count(),
            received=SendDocument.objects.filter(
                send_to=self.request.user.id).filter(
                status='received').count(),
            processing=SendDocument.objects.filter(
                send_to=self.request.user.id).filter(
                status='processing').count(),
            processed=SendDocument.objects.filter(
                send_to=self.request.user.id).filter(
                status='processed').count(),
            all=SendDocument.objects.filter(
                send_to=self.request.user.id).count()
        )
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('doc_identifier'):
            options.update(
                {'doc_identifier': kwargs.get('doc_identifier')})

        groups = request.user.groups.all()
        groups_as_list = list(groups)

        if groups_as_list:
            for group_item in groups_as_list:

                    options.update(
                        {'group': group_item.id})
        else:
            options.update({'send_to': request.user.id})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            identifier = request.POST.get('identifier')
            if identifier:
                SendDocument.objects.filter(
                    doc_identifier=identifier).update(
                    status='received',
                    received_by=request.user.username)
                print("Document set to received")
            try:
                url_name = request.url_name_data['sent_to_me_listboard_url']
            except KeyError as e:
                raise SentToMeViewError('Object not updated')
            url = reverse(url_name)
            return HttpResponseRedirect(url)





        # send_document = SendDocumentForm(self.request.POST)
        #
        # identifier = send_document['identifier']
        #
        #
        # return self.get(request, *args, **kwargs)
        #

# def receive_document(request):
#     if request.method == 'POST':
#         send_document = SendDocument(request.POST)
#
#         identifier = send_document.cleaned_data['identifier']
#
#         if identifier:
#             SendDocument.objects.filter(
#                 doc_identifier=identifier).update(
#                 show=False, status='received')
#         print("Updated")
