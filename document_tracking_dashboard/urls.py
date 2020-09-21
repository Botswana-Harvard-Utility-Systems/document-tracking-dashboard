"""potlako_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/"""
from django.urls import path

from edc_dashboard import UrlConfig

from .patterns import doc_identifier
from .views import DocumentListBoardView, HomeView
app_name = 'document_tracking_dashboard'

document_listboard_url_config = UrlConfig(
    url_name='document_listboard_url',
    view_class=DocumentListBoardView,
    label='document_listboard',
    identifier_label='doc_identifier',
    identifier_pattern=doc_identifier)


urlpatterns = [
]

urlpatterns += [path('document/', HomeView.as_view(), name='document_url')]
urlpatterns += document_listboard_url_config.listboard_urls
