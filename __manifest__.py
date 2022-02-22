# -*- coding: utf-8 -*-
{
    'name': "Purchase Request",
    'summary': """new request""",
    'sequence': 10,
    'description': """Long description of module's purpose""",
    'website': "http://www.yourcompany.com",
    'category': 'Purchase',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/rejection.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': ['demo/demo.xml',
             ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
