from datetime import date
from odoo import api, fields, models


class HanyBorse(models.Model):
    _name = "hanafy.borse"
    _description = "Hanafy borse"

    move_id = fields.Many2one('account.move', string='Hanafy borse')
    number = fields.Char(string="Number")
    invoice_date = fields.Date(string="Invoice Date")
    invoice_date_due = fields.Date(string="Invoice Date Due")
    total_ashraf = fields.Monetary(string="Total")
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.company.currency_id.id
    )
    @api.model
    def call_wizard_by_his_name(self):
        return{
            'type':'ir.actions.act.window',
            'name': 'Wizard Report',
            'res_model': 'wizard.report',
            'view_mode': 'form',
            'target': 'new',
        }
    def action_account_move(self):
        """يمسح السجلات القديمة ويجلب الفواتير المنشورة من نوع Customer Invoices"""
        self.search([]).unlink()

        hommos = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('journal_id.name', '=', 'Customer Invoices')
        ])

        records_to_create = []
        for rec in hommos:
            records_to_create.append({
                'move_id': rec.id,
                'number': rec.name or '',
                'invoice_date': rec.invoice_date,
                'invoice_date_due': rec.invoice_date_due or False,
                'total_ashraf': rec.amount_total_signed or 0.0,
                'currency_id': rec.currency_id.id or self.env.company.currency_id.id,
            })

        if records_to_create:
            recrods2 =    self.env['hanafy.borse'].create(records_to_create)
            return recrods2

    # def call_report_hanafy(self):
    #     """يفتح تقرير QWeb للسجلات المختارة"""
    #     # records = self.env['hanafy.borse'].browse(self.env.context.get('active_ids', []))
    #     records = self.action_account_move()
    #     return self.env.ref('ashrofaaa.hanafy_account_a_report').report_action(records)

    def print_report(self):
        records = self.action_account_move()
        return self.env.ref('ashrofaaa.hanafy_abb_report').report_action(records)

        # عرض النتيجة
        # return {
        #     'name': 'Hanafy Borse Records',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hanafy.borse',
        #     'view_mode': 'tree,form',
        #     'target': 'current',
        # }

    # def create_attendance(self):
    #     attendance = self.search([])
    #     for att in attendance:
    #         # Assuming you have a field that references the employee in hr.attendance
    #         employee_id = att.employee_id  # Adjust this to the correct field
    #
    #         if employee_id:  # Check if the employee_id is set
    #             vals = {
    #                 'attendance_employee_id': employee_id.id,  # Ensure this matches your attendance.history model
    #                 'daily_late_hours': att.daily_late_hours,
    #                 'daily_overtime': att.daily_overtime,
    #                 'monthly_late_hours': att.monthly_late_hours,
    #                 'monthly_overtime': att.monthly_overtime,
    #                 'check_in': att.check_in,
    #                 'check_out': att.check_out,
    #                 'worked_hours': att.worked_hours,
    #             }
    #             self.env['attendance.history'].create(vals)