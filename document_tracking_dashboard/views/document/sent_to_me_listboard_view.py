import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

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
    # listboard_view_filters = SentDocumentViewFilters()

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
        # import pdb; pdb.set_trace()
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

    # def get_queryset_filter_options(self, request, *args, **kwargs):
    #     options = super().get_queryset_filter_options(request, *args, **kwargs)
    #     if kwargs.get('doc_identifier'):
    #         options.update(
    #             {'doc_identifier': kwargs.get('doc_identifier')})
    #
    #     options.update()
    #
    #     return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.groups.filter(name='BHP HQ').exists():
            # criterion1 = Q(department__in=self.request.user.department.all())
            criterion2 = Q(send_to__id__icontains=self.request.user.id)
            criterion3 = Q(group__in=self.request.user.groups.all())
            qs = qs.filter(criterion2 | criterion3)
            return qs

        # criterion1 = Q(reception__in=self.request.user.groups.all())
        # criterion2 = Q(secondary_recep__in=self.request.user.groups.all())
        # criterion3 = Q(sent_to=self.request.user)
        # criterion4 = Q(user_created=self.request.user.username)
        # qs = qs.filter(criterion1 or criterion2 or criterion3 or criterion4)

        return qs

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
