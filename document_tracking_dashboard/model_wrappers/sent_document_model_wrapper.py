from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .sent_document_model_wrapper_mixin import \
    SentDocumentModelWrapperMixin


class SentDocumentModelWrapper(SentDocumentModelWrapperMixin, ModelWrapper):

    model = 'document_tracking.sent_document'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'sent_document_listboard_url')

    @property
    def sent_document(self):
        """"Returns a wrapped saved or unsaved sent document
        """
        model_obj = self.sent_document_model_obj or self.sent_document_cls(
            **self.sent_document_options)
        return SentDocumentModelWrapper(model_obj=model_obj)
