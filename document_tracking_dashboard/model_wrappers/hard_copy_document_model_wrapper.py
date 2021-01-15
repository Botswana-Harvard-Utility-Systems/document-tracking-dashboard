from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper

from .send_hard_copy_model_wrapper_mixin import SendHardCopyModelWrapperMixin


class HardCopyDocumentModelWrapper(SendHardCopyModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.document'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'hard_copy_document_listboard_url')

    @property
    def doc_identifier(self):
        if self.hard_copy_document_model_obj:
            return self.hard_copy_document_model_obj.doc_identifier
        return None

    @property
    def hard_copy_document_model_obj(self):
        """Returns a document model instance or None.
        """
        try:
            return self.hard_copy_document_cls.objects.get(
                **self.hard_copy_document_options)
        except ObjectDoesNotExist:
            return None

    @property
    def hard_copy_document_cls(self):
        return django_apps.get_model('document_tracking.document')

    @property
    def create_hard_copy_document_options(self):
        """Returns a dictionary of options to create a new
        unpersisted document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options

    @property
    def hard_copy_document_options(self):
        """Returns a dictionary of options to get an existing
        document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options
