

{
    'name': 'app_one',
    'author': 'Ashraf Mohamed',
    'version': '17.0.0.1.0',
    'sequence': -100,
    'category': 'Tools',
    'summary': 'نظام إدارة ',
    'description': """
    This custom module 
    """,
    'depends': ['base','sale_management','account_accountant','mail','sale'],
    'data': [
        # "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/paper_base.xml",
        "wizard/chang_state_wizard.xml",
        "views/owner_view.xml",
        "views/paper_view.xml",
        "views/property_history.xml",
        "views/property_view.xml",
        "views/tag_view.xml",
        "reports/paper_creak_report.xml",
        "views/sale_order_view.xml",
        "views/env_find.view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/property.css',],
        'web.report_assets_common':['app_one/static/src/css/font.css',]
    },

    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3'
}
