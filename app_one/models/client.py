from odoo import fields, models, api

class Client(models.Model):
    _name="client"
    _inherit = "owner"
