from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from document_tracking.models import Document

from ...model_wrappers import SentDocumentModelWrapper
from ...model_wrappers import DocumentModelWrapper


class DashboardView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):

    template_name = 'document_tracking_dashboard/document/document_dashboard.html'
    navbar_name = 'document_tracking_dashboard'

    wrapper = DocumentModelWrapper

    def document(self, doc_identifier=None):
        """Return a document.
        """
        try:
            document = Document.objects.get(doc_identifier=doc_identifier)
        except Document.DoesNotExist:
            raise ValidationError(
                f"Document with identifier {doc_identifier} does not exist")
        else:
            return document

    @property
    def sent_document_cls(self):
        return django_apps.get_model('document_tracking.senddocument')

    def data_action_item(self, doc_identifier=None):
        """Returns a wrapped saved or unsaved document.
        """
        model_obj = self.sent_document_cls(doc_identifier=doc_identifier)
        return SentDocumentModelWrapper(model_obj=model_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_identifier = kwargs.get('doc_identifier', None)
        context.update(
            document=self.document(doc_identifier=doc_identifier),
            data_action_item_add_url=self.data_action_item(doc_identifier).href,
            send_document_url=self.sent_document_cls().get_absolute_url(),)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
