import re
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from document_tracking.models import Courier, SendHardCopy
from document_tracking.forms import CourierForm

from ...model_wrappers import SendHardCopyModelWrapper


class ReceptionDocsViewError(Exception):
    pass


class ReceptionDocsListBoardView(
        NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
        SearchFormViewMixin, ListboardView):

    listboard_template = 'reception_docs_listboard_template'
    listboard_url = 'reception_docs_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = "fas fa-file"

    model = 'document_tracking.sendhardcopy'
    model_wrapper_cls = SendHardCopyModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = ''
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'reception_docs_listboard_url'

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
            couriers=Courier.objects.all().values_list('full_name', flat=True),
            secondary_recep=Group.objects.all().values_list(
                'name',
                flat=True),
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

        options.update()

        # if request.user.groups.filter(name='BHP HQ').exists():
        #     options.update({'reception__name': 'BHP HQ'})
        #     return options
        #
        # elif request.user.groups.filter(name='Finance Reception').exists():
        #     options.update({'secondary_recep__name': 'Finance Reception'})
        #     # options.update({'reception__name': 'Finance Reception'})
        #     return options

        return options


    # def get_queryset_filter_options(self, request, *args, **kwargs):
    #     options = super().get_queryset_filter_options(request, *args, **kwargs)
    #     if kwargs.get('doc_identifier'):
    #
    #         options.update(
    #             {'doc_identifier': kwargs.get('doc_identifier')})
    #     try:
    #         if request.user.groups.filter(name='BHP HQ').exists():
    #             options.update({'reception__name': 'BHP HQ'})
    #
    #         elif request.user.groups.filter(name='Finance Reception').exists():
    #             options.update({'secondary_recep__name': 'Finance Reception'})
    #
    #     except TypeError as err:
    #         print(err.args)


    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.groups.filter(name='BHP HQ').exists():
            criterion1 = Q(reception__name='BHP HQ')
            criterion2 = Q(secondary_recep__name='BHP HQ')
            qs = qs.filter(criterion1 | criterion2)
            return qs

        elif self.request.user.groups.filter(name='Finance Reception').exists():
            criterion1 = Q(reception__in=self.request.user.groups.all())
            criterion2 = Q(secondary_recep__name='Finance Reception')
            qs = qs.filter(criterion1 | criterion2)
            return qs

        # criterion1 = Q(reception__in=self.request.user.groups.all())
        # criterion2 = Q(secondary_recep__in=self.request.user.groups.all())
        # criterion3 = Q(sent_to=self.request.user)
        # criterion4 = Q(user_created=self.request.user.username)
        # qs = qs.filter(criterion1 or criterion2 or criterion3 or criterion4)

        return qs

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            update = request.POST.get('update')
            identifier = request.POST.get('identifier')
            courier = request.POST.get('courier')



            if update and update == 'update courier':
                SendHardCopy.objects.filter(
                    doc_identifier=identifier).update(
                    courier=courier)
                print("Reception updated")
                try:
                    url_name = request.url_name_data[
                        'reception_docs_listboard_url']
                except KeyError:
                    raise ReceptionDocsViewError('Courier not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

            if update and update == 'receive_hq':
                SendHardCopy.objects.filter(
                    doc_identifier=identifier).update(
                    recep_received=request.user.username)
                print("Document received at Primary Reception")
                try:
                    url_name = request.url_name_data[
                        'reception_docs_listboard_url']
                except KeyError as e:
                    raise ReceptionDocsViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

            if update and update == 'receive_finance':
                SendHardCopy.objects.filter(
                    doc_identifier=identifier).update(
                    secondary_recep_received=request.user.username)
                print("Document received at Secondary Reception")
                try:
                    url_name = request.url_name_data[
                        'reception_docs_listboard_url']
                except KeyError as e:
                    raise ReceptionDocsViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

            if update and update == 'hand_over':
                SendHardCopy.objects.filter(
                    doc_identifier=identifier).update(
                    handed_over=True)
                print("Document received at Secondary Reception")
                try:
                    url_name = request.url_name_data[
                        'reception_docs_listboard_url']
                except KeyError as e:
                    raise ReceptionDocsViewError('Object not updated')
                url = reverse(url_name)
                return HttpResponseRedirect(url)

        #
        # if request.user.groups.filter(name='Finance Reception').exists():
        #     if request.method == 'POST':
        #         identifier = request.POST.get('identifier')
        #         if identifier:
        #             SendHardCopy.objects.filter(
        #                 doc_identifier=identifier).update(
        #                 secondary_recep_received=request.user.username)
        #             print("Document received at Secondary Reception")
        #         try:
        #             url_name = request.url_name_data[
        #                 'reception_docs_listboard_url']
        #         except KeyError as e:
        #             raise ReceptionDocsViewError('Object not updated')
        #         url = reverse(url_name)
        #         return HttpResponseRedirect(url)
