{
    'name': 'Website Signup Custom Fields',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Add Mobile and Phone fields to website signup form',
    'description': '''
        This module extends the website signup form to include:
        - Mobile field (required, numbers only)
        - Phone field (required, numbers only)
        - Data is automatically saved to the partner record
    ''',
    'author': 'Zad Solutions',
    'website': 'https://www.zadsolutions.com',
    'depends': [
        'contacts',
        'website',
    ],
    'data': [
        'views/signup_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
