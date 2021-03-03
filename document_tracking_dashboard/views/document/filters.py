from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class DocumentViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    soft_copy = ListboardFilter(
        label='Soft-Copies',
        position=10,
        lookup={'document_form': 'soft_copy'},)

    hard_copy = ListboardFilter(
        label='Hard-Copies',
        position=11,
        lookup={'document_form': 'hard_copy'},)

    contract = ListboardFilter(
        label='Contracts',
        position=12,
        lookup={'document_type': 'contract'},)

    letter = ListboardFilter(
        position=13,
        label='Letters',
        lookup={'document_type': 'letter'})

    report = ListboardFilter(
        position=14,
        label='Reports',
        lookup={'document_type': 'report'},)


class SentDocumentViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    priority = ListboardFilter(
        label='High Priority',
        position=10,
        lookup={'priority': 'high'},)

    group = ListboardFilter(
        position=15,
        label='Group',
        lookup={'group__name__icontains': 'group'})

    department = ListboardFilter(
        position=15,
        label='Department',
        lookup={'dept__name__icontains': 'department'})


class ReceptionViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    received_pri_recep = ListboardFilter(
        label='Received: Primary Reception',
        position=10,
        lookup={'status': 'Received at primary Reception'}, )

    in_transit = ListboardFilter(
        label='In transit',
        position=10,
        lookup={'status': 'In transit'},)

    received_sec_recep = ListboardFilter(
        label='Received: Destination Reception',
        position=11,
        lookup={'status': 'Received at Destination Reception'}, )

    handed_over = ListboardFilter(
        label='Handed Over',
        position=12,
        lookup={'handed_over': True}, )

    received = ListboardFilter(
        label='User Received',
        position=13,
        lookup={'status': 'Received'}, )
