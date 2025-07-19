from odoo import fields, models, api

class Paper(models.Model):
    _name = "owner"

    name = fields.Char(translate=True)
    phone = fields.Char()
    address =fields.Char()
    property_ids=fields.One2many("property","owner_id")
