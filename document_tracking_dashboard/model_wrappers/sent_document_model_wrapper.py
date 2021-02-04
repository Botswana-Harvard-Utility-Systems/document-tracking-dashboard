from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper
from .document_model_wrapper_mixin import DocumentModelWrapperMixin


class SentDocumentModelWrapper(DocumentModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.senddocument'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'sent_listboard_url')

    @property
    def doc_obj(self):
        if self.document_model_obj:
            return self.document_model_obj
        return None

    @property
    def sent_document_model_obj(self):
        """Returns a sent document model instance or None.
        """
        try:
            return self.sent_document_cls.objects.get(
                **self.sent_document_options)
        except ObjectDoesNotExist:
            return None

    @property
    def sent_document_cls(self):
        return django_apps.get_model('document_tracking.senddocument')

    @property
    def sent_document(self):
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.sent_document_cls(
            **self.sent_document_options)
        return SentDocumentModelWrapper(model_obj=model_obj)

    @property
    def sent_document_options(self):
        """Returns a dictionary of options to get an existing
        sent document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options
