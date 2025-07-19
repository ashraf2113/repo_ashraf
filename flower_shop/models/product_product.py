from odoo import models, fields, api
from collections import defaultdict

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_flower = fields.Boolean(string="Is a Flower")
    flower_id = fields.Many2one('flower.flower', string="Flower")
    needs_watering = fields.Boolean(string="Needs Watering", default=False)
    sequence_id = fields.Many2one('ir.sequence', string="Flower Sequence")
    user_ids = fields.Many2many('res.users', string="Assigned Gardeners")

    def action_needs_watering(self):
        serials = self.env['stock.lot'].search([('product_id', 'in', self.ids)])
        lot_vals = defaultdict(bool)
        today = fields.Date.today()

        for serial in serials:
            if serial.water_ids:
                last_watered_date = serial.water_ids[0].date
                frequency = serial.product_id.flower_id.watering_frequency
                needs_watering = (today - last_watered_date).days >= frequency
                lot_vals[serial.product_id.id] |= needs_watering
            else:
                lot_vals[serial.product_id.id] = True

        for flower in self:
            flower.needs_watering = lot_vals[flower.id]

    @api.model
    def assign_user_to_group(self):
        user = self.env.ref('base.user_admin')  # أو أي يوزر تاني
        group = self.env.ref('flower_shop.group_gardener')  # غيّر الـ external ID لو مختلف

        if group not in user.groups_id:
            user.groups_id = [(4, group.id)]
