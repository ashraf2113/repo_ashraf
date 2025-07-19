from odoo import fields, models, api, _


class Property(models.Model):
    _name = "property.history"
    # _log_access=False
    # rec_name="postcode"
    user_id=fields.Many2one("res.users")
    property_id=fields.Many2one('property')
    old_state=fields.Char()
    new_state = fields.Char()
    line_ids=fields.One2many("property.history.line","history_id")
    reason = fields.Char()

class PropertyLine(models.Model):
    _name = "property.history.line"
    history_id=fields.Many2one("property.history")
    description = fields.Text()
    area = fields.Float()





