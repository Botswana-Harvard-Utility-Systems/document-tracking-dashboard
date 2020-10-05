from django import template
# from django.conf import settings

register = template.Library()


@register.inclusion_tag('document_tracking_dashboard/buttons/send_document_button.html')
def send_document_button(model_wrapper):
    title = ['Send Document.']
    return dict(
        doc_identifier=model_wrapper.object.doc_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('document_tracking_dashboard/buttons/edit_document_button.html')
def edit_document_button(model_wrapper):
    title = ['Edit document form.']
    return dict(
        doc_identifier=model_wrapper.object.doc_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
