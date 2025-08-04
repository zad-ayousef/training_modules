{
    'name': "purchase request",
    'summary': """
            .
    """,
    'description': """
                 
                  """,
    'author': "Abdelrahman Yousef/Zad Solutions",
    'website': "http://zadsolutions.com",
    'category': 'Education',
    'version': '18.0.1.0.0',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/purchase_request_views.xml',
        'wizard/rejected_reason_wizard_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
