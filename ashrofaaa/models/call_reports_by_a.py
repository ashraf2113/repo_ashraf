from odoo import api, models

class CallReportByA(models.AbstractModel):
    _name = "report.ashrofaaa.hanafy_account_report_template"
    _description = "Hanafy Account Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [
            ('state', '=', 'posted'),
            ('journal_id.name', '=', 'Customer Invoices')
        ]
        all_lines = self.env['account.move'].search(domain)
        print(f"Found {len(all_lines)} records to print.")

        unique_moves = {}
        for rec in all_lines:
            if rec.name not in unique_moves:
                unique_moves[rec.name] = rec

        records = list(unique_moves.values())

        return {
            'doc_ids': [r.id for r in records],
            'doc_model': 'account.move',
            'docs': records,
            'data': data or {},
        }

    def call_report_hanafy(self):
        records = self._get_report_values(docids=[])
        return self.env.ref('ashrofaaa.hanafy_account_a_report').report_action(records['doc_ids'])

    def print_report(self):
        records = self._get_report_values(docids=[])
        return self.env.ref('ashrofaaa.hanafy_abb_report').report_action(records['doc_ids'])
