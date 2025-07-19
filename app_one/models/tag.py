from odoo import fields, models, api

class Paper(models.Model):
    _name = "tag"

    name = fields.Char(translate=True)


