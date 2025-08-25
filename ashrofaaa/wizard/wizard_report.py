
from odoo import models, fields, api, _


class WizardReport(models.TransientModel):
    _name = "wizard.report"
    _description = "Wizard Report"
    _rec_name = "name"

    name = fields.Char(string="Name")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    def action_confirm(self):
        # هنا ممكن تضيف أي logic قبل الإغلاق
        return {'type': 'ir.actions.act_window_close'}
    def print_report(self):
        return self.env.ref('ashrofaaa.hanafy_abb_report').report_action(self)