{
    'name': 'POS PIN Dashboard',
    'version': '19.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Restrict POS Dashboard access using Employee PIN',
    'description': """
        This module requires users to enter their employee PIN before accessing the POS Dashboard.
        It filters the visible POS configurations based on the employee's permissions.
    """,
    'author': 'Antigravity',
    'depends': ['point_of_sale', 'hr', 'pos_hr'],
    'data': [
        'views/actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_pin_restriction/static/src/css/pin_screen.css',
            'pos_pin_restriction/static/src/js/pin_screen.js',
            'pos_pin_restriction/static/src/xml/pin_screen.xml',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
