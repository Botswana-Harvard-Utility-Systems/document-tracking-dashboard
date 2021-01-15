from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_model_wrapper import ModelWrapper


class SendHardCopyModelWrapper(ModelWrapper):

    model = 'document_tracking.sendhardcopy'
    querystring_attrs = ['doc_identifier']
    next_url_attrs = ['doc_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'send_hard_copy_listboard_url')

    @property
    def doc_identifier(self):
        if self.send_hard_copy_model_obj:
            return self.send_hard_copy_model_obj.doc_identifier
        return None

    @property
    def send_hard_copy_model_obj(self):
        """Returns a sent hard copy model instance or None.
        """
        try:
            return self.send_hard_copy_cls.objects.get(
                **self.send_hard_copy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def send_hard_copy_cls(self):
        return django_apps.get_model('document_tracking.sendhardcopy')

    @property
    def create_send_hard_copy_options(self):
        """Returns a dictionary of options to create a new
        unpersisted send hard copy model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options

    @property
    def send_hard_copy_options(self):
        """Returns a dictionary of options to get an existing
        send hard copy model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options
