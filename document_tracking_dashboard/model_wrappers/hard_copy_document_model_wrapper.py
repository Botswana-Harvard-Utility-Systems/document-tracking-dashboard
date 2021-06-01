from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper

from .send_hard_copy_model_wrapper_mixin import SendHardCopyModelWrapperMixin
from .document_model_wrapper_mixin import DocumentModelWrapperMixin


class HardCopyDocumentModelWrapper(
        SendHardCopyModelWrapperMixin, DocumentModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.document'
    querystring_attrs = ['doc_identifier', 'document_form']
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
    def hard_copy_document(self):
        """Returns a wrapped saved or unsaved hard document.
        """
        model_obj = self.hard_copy_document_model_obj or self.hard_copy_document_cls(
            **self.create_hard_copy_document_options)
        return HardCopyDocumentModelWrapper(model_obj=model_obj)

    @property
    def hard_copy_document_cls(self):
        return django_apps.get_model('document_tracking.document')

    @property
    def create_hard_copy_document_options(self):
        """Returns a dictionary of options to create a new
        unpersisted document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier,
            document_form=self.object.document_form,)
        return options

    @property
    def hard_copy_document_options(self):
        """Returns a dictionary of options to get an existing
        document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier,
            document_form=self.object.document_form,)
        return options

    @property
    def sent(self):
        send_hard_copies_model_cls = django_apps.get_model(
            'document_tracking.sendhardcopy')
        try:
            send_hard_copies_model_cls.objects.get(
                doc_identifier=self.object.doc_identifier)
        except send_hard_copies_model_cls.DoesNotExist:
            return False
        else:
            return True
