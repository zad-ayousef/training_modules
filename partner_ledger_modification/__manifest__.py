{
    'name': 'Partner Ledger Initial Balance Filter',
    'version': '18.0.1.0.0',
    'summary': 'Add a Show Initial Balance toggle to Partner Ledger (account_reports)',
    'description': """
Partner Ledger Initial Balance Filter

This module extends the Partner Ledger report functionality by adding
a filter option to show/hide initial balances.

Features:
* Add "Show Initial Balance" filter option in Partner Ledger report
* Toggle initial balance display without affecting calculations
* Maintain compatibility with existing Partner Ledger functionality
* Support for PDF and Excel export with filter applied

Technical Details:
* Extends account_reports module
* Inherits Partner Ledger JavaScript widgets
* Modifies backend report generation logic
* Compatible with Odoo 18.0 Enterprise Edition
    """,
    'category': 'Accounting',
    'author': 'Zad solutions / Abdelrahman Yousef',
    'license': 'LGPL-3',
    'depends': ['account', 'account_reports', 'web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'partner_ledger_modification/static/src/js/partner_ledger_owl_inject.js',
        ],
    },
    'installable': True,
    'application': False,
}
