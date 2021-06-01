from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .send_hard_copy_model_wrapper import SendHardCopyModelWrapper


class SendHardCopyModelWrapperMixin:

    send_hard_copy_model_wrapper_cls = SendHardCopyModelWrapper

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
    def send_hard_copy_document(self):
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.send_hard_copy_cls(
            **self.send_hard_copy_options)
        return self.send_hard_copy_model_wrapper_cls(model_obj=model_obj)

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
