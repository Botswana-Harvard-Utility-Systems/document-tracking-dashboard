from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'document_tracking_dashboard' else False

document_tracking_dashboard = Navbar(name='document_tracking_dashboard')

document_tracking_dashboard.append_item(
    NavbarItem(
        name='documents',
        title='Documents',
        label='Soft-Copy Documents',
        fa_icon='far fa-file',
        url_name=settings.DASHBOARD_URL_NAMES[
            'document_listboard_url'],
        no_url_namespace=no_url_namespace))

document_tracking_dashboard.append_item(
    NavbarItem(
        name='sent_documents',
        title='Sent Documents',
        label='Sent Soft-Copies',
        fa_icon='fa fa-list-alt fa-sm',
        url_name=settings.DASHBOARD_URL_NAMES[
            'sent_listboard_url'],
        no_url_namespace=no_url_namespace))

document_tracking_dashboard.append_item(
    NavbarItem(
        name='documents_sent_to_me',
        title='Documents Sent To Me',
        label='Soft-Copies Sent To Me',
        fa_icon='fas fa-inbox',
        url_name=settings.DASHBOARD_URL_NAMES[
            'sent_to_me_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(document_tracking_dashboard)
