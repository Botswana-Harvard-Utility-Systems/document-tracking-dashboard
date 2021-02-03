import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from document_tracking.models import SendHardCopy

from ...model_wrappers import SendHardCopyModelWrapper


class SentHardCopyViewError(Exception):
    pass


class SendHardCopyListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'send_hard_copy_listboard_template'
    listboard_url = 'send_hard_copy_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = "fas fa-file"

    model = 'document_tracking.sendhardcopy'
    model_wrapper_cls = SendHardCopyModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'sent_documents'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'send_hard_copy_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def document(self, doc_identifier=None):
        """Returns a new sent document obj.
        """
        return SendHardCopyModelWrapper(SendHardCopy(doc_identifier=doc_identifier))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_identifier = kwargs.get('doc_identifier', None)

        context.update(
            document=self.document(doc_identifier=doc_identifier),
            sent=SendHardCopy.objects.filter(
                user_created=self.request.user.username).filter(
                status='sent').count(),
            received=SendHardCopy.objects.filter(
                user_created=self.request.user.username).filter(
                status='received').count(),
            processing=SendHardCopy.objects.filter(
                user_created=self.request.user.username).filter(
                status='processing').count(),
            processed=SendHardCopy.objects.filter(
                user_created=self.request.user.username).filter(
                status='processed').count(),
            all=SendHardCopy.objects.filter(
                user_created=self.request.user.username).count()

        )
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('doc_identifier'):

            options.update(
                {'doc_identifier': kwargs.get('doc_identifier')})
        # elif request.user.groups.filter(name='BHP HQ').exists():
        #     options.update()
        #
        # elif request.user.groups.filter(name='Finance Reception').exists():
        #     options.update()
        #
        # if SendHardCopy.objects.filter(send_to=request.user).exists():
        #     options.update({'send_to': request.user})
        #
        # else:
        #     options.update({'user_created': request.user.username})

        options.update()
        return options

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #
    #     criterion1 = Q(reception__in=self.request.user.groups.all())
    #     criterion2 = Q(secondary_recep__in=self.request.user.groups.all())
    #     criterion3 = Q(sent_to=self.request.user)
    #     criterion4 = Q(user_created=self.request.user.username)
    #     qs = qs.filter(criterion1 or criterion2 or criterion3 or criterion4)
    #
    #     return qs

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q

    def post(self, request, *args, **kwargs):

        if request.user.groups.filter(name='BHP HQ').exists():
            if request.method == 'POST':
                identifier = request.POST.get('identifier')
                if identifier:
                    SendHardCopy.objects.filter(
                        doc_identifier=identifier).update(
                        recep_received=request.user.username)
                    print("Document received at Primary Reception")
                try:
                    url_name = request.url_name_data[
                        'send_hard_copy_listboard_url']
                except KeyError as e:
                    raise SentHardCopyViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

        if request.user.groups.filter(name='Finance Reception').exists():
            if request.method == 'POST':
                identifier = request.POST.get('identifier')
                if identifier:
                    SendHardCopy.objects.filter(
                        doc_identifier=identifier).update(
                        secondary_recep_received=request.user.username)
                    print("Document received at Secondary Reception")
                try:
                    url_name = request.url_name_data[
                        'send_hard_copy_listboard_url']
                except KeyError as e:
                    raise SentHardCopyViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

        else:
            if request.method == 'POST':
                identifier = request.POST.get('identifier')
                if identifier:
                    SendHardCopy.objects.filter(
                        doc_identifier=identifier).update(
                        received_by=request.user.username)
                    print("Document received")
                try:
                    url_name = request.url_name_data[
                        'send_hard_copy_listboard_url']
                except KeyError as e:
                    raise SentHardCopyViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)
