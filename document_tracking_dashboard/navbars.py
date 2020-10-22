from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'document_tracking_dashboard' else False

document_tracking_dashboard = Navbar(name='document_tracking_dashboard')

document_tracking_dashboard.append_item(
    NavbarItem(
        name='procurement',
        title='Procurement',
        label='Procurement',
        fa_icon='fa fa-list-alt',
        url_name=settings.DASHBOARD_URL_NAMES[
            'procurement_url'],
        no_url_namespace=no_url_namespace))

document_tracking_dashboard.append_item(
    NavbarItem(
        name='documents',
        title='Documents',
        label='Documents',
        fa_icon='fas fa-file',
        url_name=settings.DASHBOARD_URL_NAMES[
            'document_listboard_url'],
        no_url_namespace=no_url_namespace))

document_tracking_dashboard.append_item(
    NavbarItem(
        name='CMS',
        title='CMS',
        label='CMS',
        fa_icon='',
        url_name=settings.DASHBOARD_URL_NAMES[
            'bhp_personnel_url'],
        no_url_namespace=no_url_namespace))


site_navbars.register(document_tracking_dashboard)
