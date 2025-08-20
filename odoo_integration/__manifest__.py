{
    'name': "Odoo Synchronization (Odoo 17 & Odoo 18)",
    'version': '17.0.1.0',
    'summary': "Bidirectional synchronization of Project data between Odoo 17 and Odoo 18",
    'category': 'Project',
    'author': "Abdelrahman Yousef",
    'website': "https://zadsolutions.com",
    'depends': [
        'base',
        'project',
        'mail',
    ],

    'data': [

        'views/res_config_settings_views_inherit.xml',

    ],
    'assets': {
    },
    'installable': True,
    'application': False,
}
