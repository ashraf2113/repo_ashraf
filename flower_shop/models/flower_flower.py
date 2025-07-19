from odoo import models, fields

class FlowerFlower(models.Model):
    _name = 'flower.flower'
    _description = 'Flower'

    name = fields.Char(string="Flower Name", required=True)
    watering_frequency = fields.Integer(string="Watering Frequency (Days)", default=7, help="Number of days between watering")
