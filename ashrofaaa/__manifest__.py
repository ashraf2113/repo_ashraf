# -*- Coding: utf-8 -*-

{
    'name': 'ASHROFAAA',
    'version': '1.0.0',
    'category': 'BASHMOHANDES',
    'author': 'GZ SWEET',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['base', 'mail', 'product', 'sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        "data/access_wizard_report.xml",
        "data/data_fam_pat.xml",
        "data/sequence_ash.xml",
        # "data/data_pat_a.csv",
        "views/menu.xml",  # يتم تحميل تعريف القوائم أولاً
        "reports/hanafy_static_report.xml",
        "reports/hanafy_account_report.xml",
        "wizard/cancel_in_wizard.xml",
        "wizard/wizard_report.xml",
        "views/customers_view.xml",
        "views/hanafy_borse_view.xml",
        "views/lawyers_view.xml",
        "views/patients_view.xml",
        "views/females_patients_view.xml",
        "views/inhe_mod.xml",
        "views/plays_ground.xml",
        # "views/report_inherits.xml",

    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
