from odoo import fields, models

class ChangeState(models.TransientModel):
    _name = "chang.state"
    _description = "Change State"

    property_id = fields.Many2one("property", required=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
            ('closed', 'Closed'),
        ],
        string="State",
        default="draft"
    )

    reason = fields.Char()

    def action_wizard(self):
        print("##########################")
        """تحديث حالة العقار وإضافة السجل في السجل التاريخي"""
        for rec in self:
            if rec.property_id:
                rec.property_id.write({'state': rec.state})
                rec.property_id.create_history_record(rec.property_id.state, rec.state)
