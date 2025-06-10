

{
    'name': 'flower_watering',
    'author': 'Ashraf Mohamed',
    'version': '17.0.0.0',
    'sequence': -100,
    'category': 'Inventory',
    'summary': 'Track and manage flower watering using serial numbers',
    'description': """
        This module allows tracking watering times for flowers
        identified by serial numbers (lots).
    """,
    'depends': ['base','stock', 'sale', 'sale_stock'],
    'data': [
        "security/ir.model.access.csv",
        "views/flower_base.xml",
        "data/server_actions.xml",
        "views/flower_view.xml",
        "views/stock_lot.xml",
        "reports/report_screen_stock_lot.xml",
        "reports/report_screen_flower_water.xml",
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3'
}
