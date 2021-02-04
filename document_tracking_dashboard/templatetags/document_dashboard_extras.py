from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='has_primary_recep')
def has_primary_recep(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_secondary_recep')
def has_secondary_recep(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.inclusion_tag('document_tracking_dashboard/buttons/soft_copy_button.html')
def soft_copy_button(model_wrapper):
    return dict(
        document_href=model_wrapper.document.href,
        document_form=model_wrapper.document_form)


@register.inclusion_tag('document_tracking_dashboard/buttons/sent_document_button.html')
def sent_document_button(model_wrapper):
    return dict(
        send_document_href=model_wrapper.href,
        doc_identifier=model_wrapper.object.doc_identifier)

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


@register.inclusion_tag('document_tracking_dashboard/buttons/send_hard_copy_button.html')
def send_hard_copy_document_button(model_wrapper):
    return dict(
        send_hard_copy_document_href=model_wrapper.send_hard_copy_document.href,
        doc_identifier=model_wrapper.object.doc_identifier)


@register.inclusion_tag('document_tracking_dashboard/buttons/edit_document_button.html')
def edit_document_button(model_wrapper):
    title = ['Edit document form.']
    return dict(
        doc_identifier=model_wrapper.object.doc_identifier,
        href=model_wrapper.href,
        title=' '.join(title))
