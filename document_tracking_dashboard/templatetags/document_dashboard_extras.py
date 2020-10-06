from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('document_tracking_dashboard/buttons/send_document_button.html')
def send_document_button(model_wrapper):
    sent_document_listboard_url = settings.DASHBOARD_URL_NAMES.get(
        'sent_document_listboard_url')
    title = ['Send Document.']
    return dict(
        sent_document_listboard_url=sent_document_listboard_url,
        # doc_identifier=model_wrapper.doc_identifier,
        # href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('document_tracking_dashboard/buttons/send_button.html')
def send_button(model_wrapper):
    return dict(
        send_document_href=model_wrapper.sent_document.href,
        doc_identifier=model_wrapper.object.doc_identifier,
        sent_document_model_obj=model_wrapper.sent_document_model_obj)


@register.inclusion_tag('document_tracking_dashboard/buttons/edit_document_button.html')
def edit_document_button(model_wrapper):
    title = ['Edit document form.']
    return dict(
        doc_identifier=model_wrapper.object.doc_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
