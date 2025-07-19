from odoo import fields, models, api

class Paper(models.Model):
    _name = "paper"

    owner = fields.Char("owner",translate=True)
    phone = fields.Char("phone",translate=True)
    


    soso =fields.Char(string="soso")
    lolo =fields.Char(string="lolo")
