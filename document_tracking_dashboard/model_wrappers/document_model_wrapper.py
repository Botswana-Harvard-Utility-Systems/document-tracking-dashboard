from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .document_model_wrapper_mixin import \
    DocumentModelWrapperMixin


class DocumentModelWrapper(DocumentModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.document'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'document_listboard_url')

    @property
    def document(self):
        """"Returns a wrapped saved or unsaved document
        """
        model_obj = self.document_model_obj or self.document_cls(
            **self.document_options)
        return DocumentModelWrapper(model_obj=model_obj)
