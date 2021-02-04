from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper

from .sent_document_model_wrapper_mixin import SentDocumentModelWrapperMixin


class DocumentModelWrapper(SentDocumentModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.document'
    querystring_attrs = ['doc_identifier', 'document_form']
    next_url_attrs = ['doc_identifier', 'document_form']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'document_listboard_url')

    @property
    def document_form(self):
        document_form = 'Soft-Copy'
        return document_form

    @property
    def doc_identifier(self):
        if self.document_model_obj:
            return self.document_model_obj.doc_identifier
        return None

    @property
    def document_model_obj(self):
        """Returns a document model instance or None.
        """
        try:
            return self.document_cls.objects.get(
                **self.document_options)
        except ObjectDoesNotExist:
            return None

    @property
    def document(self):
        """Returns a wrapped saved or unsaved document.
        """
        model_obj = self.document_cls(
            **self.document_options)
        return DocumentModelWrapper(document_model_obj=model_obj)

    @property
    def document_cls(self):
        return django_apps.get_model('document_tracking.document')

    @property
    def create_document_options(self):
        """Returns a dictionary of options to create a new
        unpersisted document model instance.
        """
        options = dict(
            document_form=self.object.document_form,
            doc_identifier=self.object.doc_identifier)
        return options

    @property
    def document_options(self):
        """Returns a dictionary of options to get an existing
        document model instance.
        """
        options = dict(
            document_form=self.object.document_form,
            doc_identifier=self.object.doc_identifier)
        return options
