{
    'name': 'POS Modification',
    'version': '18.0.1.0.0',
    'summary': 'Custom modifications for Point of Sale (Attachments + Product Limit)',
    'description': """
POS Custom Modifications

Features:
* Add Attachment field to POS Orders (read-only, downloadable).
* Add Attachment field to Close Register wizard and propagate to POS Orders.
* Add "Add Limit" boolean and "The Limit" integer field to product variants in POS tab.
* POS Frontend validation to restrict product quantities based on "The Limit".
    """,
    'category': 'Point of Sale',
    'author': 'Abdelrahman Yousef',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'product',
    ],
    'data': [
        'views/pos_order_views_inherit.xml',
        'views/product_product_views_inherit.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_modification/static/src/components/closing_popup_extend.js',
            'pos_modification/static/src/components/closing_popup_template_inherit.xml',
            'pos_modification/static/src/components/product_screen_extend.js',
            'pos_modification/static/src/components/order_summary_extend.js',
        ],
    },
    'installable': True,
    'application': False,
}
