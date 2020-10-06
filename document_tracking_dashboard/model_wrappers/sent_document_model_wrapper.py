from django.conf import settings
from edc_model_wrapper import ModelWrapper


class SentDocumentModelWrapper(ModelWrapper):

    model = 'document_tracking.senddocument'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'sent_document_listboard_url')
