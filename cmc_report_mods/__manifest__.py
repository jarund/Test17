# -*- coding: utf-8 -*-
{
    'name': "CMC Report Mods",

    'summary': """
        Report modifications at cleints request""",

    'description': """
        Report modifications at cleints request, adding fields to the delivery order.  
        Adding a new version of the Delivery Report Shipping Report showing adjusted Qty.
    """,

    'author': "Talus ERP",
    'website': "http://www.taluserp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/report_deliveryslip_inherit.xml',
        'reports/report_ship.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
