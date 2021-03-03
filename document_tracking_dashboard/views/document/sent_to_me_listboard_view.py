import re
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.core.exceptions import ValidationError
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
    listboard_view_filters = SentDocumentViewFilters()

    model = 'document_tracking.senddocument'
    model_wrapper_cls = SentDocumentModelWrapper
    navbar_name = 'document_tracking_dashboard'
    navbar_selected_item = 'documents_sent_to_me'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'sent_to_me_listboard_url'

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

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        group_filter = options.get('group__name__icontains', '')
        if group_filter:
            options = {key: val for key, val in options.items() if key != 'group__name__icontains'}
            usr_groups = [g.name for g in self.request.user.groups.all()]
            options.update({'group__name__in': usr_groups})
        dept_filter = options.get('dept__name__icontains')
        if dept_filter:
            department = self.employee_dept
            options = {key: val for key, val in options.items() if key != 'dept__name__icontains'}
            options.update({'department__dept_name': department.dept_name})
        options.update({'send_to': request.user.id})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(doc_identifier__exact=search_term)
        return q

    def get_queryset(self):
        qs = super().get_queryset()
        criterion1 = Q(department__name=self.employee_dept.name)
        criterion2 = Q(send_to__id__icontains=self.request.user.id)
        criterion3 = Q(group__in=self.request.user.groups.all())
        qs = qs.filter(criterion1 | criterion2 | criterion3)
        return qs

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            identifier = request.POST.get('identifier')
            if identifier:
                SendDocument.objects.filter(
                    transaction_identifier=identifier).update(
                    status='received',
                    received_by=request.user.username)
                print("Document set to received")
            try:
                url_name = request.url_name_data['sent_to_me_listboard_url']
            except KeyError as e:
                raise SentToMeViewError('Object not updated')
            url = reverse(url_name)
            return HttpResponseRedirect(url)

    @property
    def employee_dept(self):
        employee_cls = django_apps.get_model('bhp_personnel.employee')
        try:
            employee = employee_cls.objects.get(email=self.request.user.email)
        except employee_cls.DoesNotExist:
            raise ValidationError('User does not exist as an employee')
        else:
            return employee.department
