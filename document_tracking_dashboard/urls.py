"""potlako_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/"""
from django.urls import path

from edc_dashboard import UrlConfig

from .patterns import doc_identifier
from .views import SentDocumentListBoardView, DashboardView, \
    DocumentListBoardView, HomeView, SentListBoardView

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

sent_document_listboard_urlconfig = UrlConfig(
    url_name='sent_document_listboard_url',
    view_class=SentDocumentListBoardView,
    label='sent_document_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)

sent_listboard_urlconfig = UrlConfig(
    url_name='sent_listboard_url',
    view_class=SentListBoardView,
    label='sent_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)


urlpatterns = [
]

urlpatterns += [path('document/', HomeView.as_view(), name='document_url')]
urlpatterns += document_dashboard_url_config.dashboard_urls
urlpatterns += document_listboard_url_config.listboard_urls
urlpatterns += sent_document_listboard_urlconfig.listboard_urls
urlpatterns += sent_listboard_urlconfig.listboard_urls
