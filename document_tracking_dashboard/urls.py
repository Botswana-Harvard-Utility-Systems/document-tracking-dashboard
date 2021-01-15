"""potlako_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from edc_dashboard import UrlConfig

from .patterns import doc_identifier
from .views import (SentToMeListBoardView, SharedDocumentsListBoardView,
                    DashboardView, DocumentListBoardView, HomeView,
                    HardCopyDocumentListBoardView,
                    SendHardCopyListBoardView, SentListBoardView)

app_name = 'document_tracking_dashboard'

document_listboard_url_config = UrlConfig(
    url_name='document_listboard_url',
    view_class=DocumentListBoardView,
    label='document_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

document_dashboard_url_config = UrlConfig(
    url_name='document_dashboard_url',
    view_class=DashboardView,
    label='document_dashboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

hard_copy_document_listboard_url_config = UrlConfig(
    url_name='hard_copy_document_listboard_url',
    view_class=HardCopyDocumentListBoardView,
    label='hard_copy_document_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

send_hard_copy_listboard_url_config = UrlConfig(
    url_name='send_hard_copy_listboard_url',
    view_class=SendHardCopyListBoardView,
    label='send_hard_copy_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

sent_to_me_listboard_urlconfig = UrlConfig(
    url_name='sent_to_me_listboard_url',
    view_class=SentToMeListBoardView,
    label='sent_to_me_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

sent_listboard_urlconfig = UrlConfig(
    url_name='sent_listboard_url',
    view_class=SentListBoardView,
    label='sent_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

shared_documents_listboard_urlconfig = UrlConfig(
    url_name='shared_documents_listboard_url',
    view_class=SharedDocumentsListBoardView,
    label='shared_documents_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

urlpatterns = [
]

urlpatterns += [path('document/', HomeView.as_view(), name='document_url')]
urlpatterns += document_dashboard_url_config.dashboard_urls
urlpatterns += document_listboard_url_config.listboard_urls
urlpatterns += hard_copy_document_listboard_url_config.listboard_urls
urlpatterns += send_hard_copy_listboard_url_config.listboard_urls
urlpatterns += sent_to_me_listboard_urlconfig.listboard_urls
urlpatterns += sent_listboard_urlconfig.listboard_urls
urlpatterns += shared_documents_listboard_urlconfig.listboard_urls
