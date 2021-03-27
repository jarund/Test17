# -*- coding: utf-8 -*-
{
    'name': "Talus ERP Help Extension for CMC",
    'summary': """
        This module will add a help menu item to provide help files in certain modules.""",
    'description': """
        This module will add a help menu item to provide help files in certain modules.
    """,
    'author': "Talus ERP",
    'website': "http://www.taluserp.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.6',
    # any module necessary for this one to work correctly
    'depends': ['base','stock'],
    # always loaded
    'data': [
        'data/help_url.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        'static/src/xml/talus_iorad.xml',
    ]
}
