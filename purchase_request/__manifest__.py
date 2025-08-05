{
    'name': "purchase request",
    'summary': "Odoo 18 module for managing purchase requests with approval workflow and automated notifications.",
    'description': """
purchase_request  
https://github.com/ayousef-zad/training_modules/blob/main/README.md#purchase_request

An Odoo 18 module to manage purchase requests:
- Approval workflow with statusbar.
- Request line details and dynamic total.
- Editable/request fields based on state.
- Rejection wizard with reason capture.
- Manager notifications by email.

Key fields: name, requested_by, status, order_lines_ids, total_price, is_editable.

Workflow: submit, approve, reject, cancel with transitions and field security. Views, menu integration, and wizard included.
""",
    'author': "Abdelrahman Yousef / Zad Solutions",
    'website': "http://zadsolutions.com",
    'category': 'Purchases',
    'version': '18.0.1.0.0',
    'depends': ['base', 'mail', 'purchase'],
    'data': [
        'wizard/rejected_reason_wizard_view.xml',
        'security/ir.model.access.csv',
        'views/purchase_request_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
