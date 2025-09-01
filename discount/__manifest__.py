{
    'name': "Discount Account Management",
    'version': '18.0.1.0',
    'summary': "Automatic discount accounting for sales and purchase orders",
    'description': """
        This module extends Odoo's accounting functionality to:
        - Add discount configuration in accounting settings
        - Automatically create journal entries for discounts in sales and purchase orders
        - Handle discount posting to specified accounts (Sales: Debit, Purchase: Credit)
        - Calculate discounts using the standard formula: price_subtotal = qty * price_unit * (1 - discount)
    """,
    'category': 'Accounting',
    'author': "Abdelrahman Yousef",
    'website': "https://zadsolutions.com",
    'depends': [
        'base',
        'account',
        'accountant',
        'sale',
        'sale_management',
        'purchase',
    ],

    'data': [
        'views/res_config_settings_views_inherit.xml',
        'views/purchase_order_views_inherit.xml',
        'views/sale_order_views_inherit.xml',
        'views/account_move_views_inherit.xml',
    ],
    'assets': {
    },
    'installable': True,
    'application': False,
}
