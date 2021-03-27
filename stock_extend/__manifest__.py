# -*- coding: utf-8 -*-
{
    'name': "CMC Stock Extend",
    'summary': """Report modifications at cleints request""",
    'description': """
        Report modifications at cleints request
    """,
    'author': "",
    'website': "",
    'category': 'Uncategorized',
    'version': '14.0',
    'depends': [
        'stock',
        'cmc_scrap_tracking'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/stock_picking_confirm_wizard_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_production_lot_views.xml'
    ],
    'demo': [
    ],
}
