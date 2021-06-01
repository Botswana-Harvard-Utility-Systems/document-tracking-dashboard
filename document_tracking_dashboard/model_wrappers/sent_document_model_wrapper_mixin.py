from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .sent_document_model_wrapper import SentDocumentModelWrapper


class SentDocumentModelWrapperMixin:

    sent_document_model_wrapper_cls = SentDocumentModelWrapper

    @property
    def doc_identifier(self):
        if self.sent_document_model_obj:
            return self.sent_document_model_obj.doc_identifier
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
        return self.sent_document_model_wrapper_cls(model_obj=model_obj)

    @property
    def create_sent_document_options(self):
        """Returns a dictionary of options to create a new
        unpersisted sent document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options

    @property
    def sent_document_options(self):
        """Returns a dictionary of options to get an existing
        sent document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options
