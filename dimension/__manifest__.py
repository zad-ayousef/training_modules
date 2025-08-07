{
    'name': "Product Dimension",
    'version': '18.0.1.0',
    'summary': "Add and manage product dimensions through Sales, Inventory, and Invoicing",
    'category': 'Sales',
    'author': "Abdelrahman Yousef",
    'website': "https://zadsolutions.com",
    'depends': [
        'product',
        'sale',
        'stock',
        'account',
    ],
    'data': [
        'views/product_template_inherit_views.xml',
        'views/sale_order_line_inherit_views.xml',
        'views/stock_move_inherit_views.xml',
        'views/account_move_line_inherit_views.xml',
    ],
    'installable': True,
    'application': False,
}
