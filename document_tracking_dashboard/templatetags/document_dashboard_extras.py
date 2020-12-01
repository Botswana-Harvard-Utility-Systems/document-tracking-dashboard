from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('document_tracking_dashboard/buttons/forward_document_button.html')
def forward_document_button(model_wrapper):
    return dict(
        send_document_href=model_wrapper.sent_document.href,
        doc_identifier=model_wrapper.object.doc_identifier)


@register.inclusion_tag('document_tracking_dashboard/buttons/send_button.html')
def send_button(model_wrapper):
    return dict(
        send_document_href=model_wrapper.sent_document.href,
        doc_identifier=model_wrapper.object.doc_identifier)


@register.inclusion_tag('document_tracking_dashboard/buttons/edit_document_button.html')
def edit_document_button(model_wrapper):
    title = ['Edit document form.']
    return dict(
        doc_identifier=model_wrapper.object.doc_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
