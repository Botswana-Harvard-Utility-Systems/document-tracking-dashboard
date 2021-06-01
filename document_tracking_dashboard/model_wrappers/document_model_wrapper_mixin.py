from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class DocumentModelWrapperMixin:

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
    def document_cls(self):
        return django_apps.get_model('document_tracking.document')

    @property
    def create_document_options(self):
        """Returns a dictionary of options to create a new
        unpersisted document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options

    @property
    def document_options(self):
        """Returns a dictionary of options to get an existing
        document model instance.
        """
        options = dict(
            doc_identifier=self.object.doc_identifier)
        return options
