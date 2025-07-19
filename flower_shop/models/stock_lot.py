from odoo import models, fields, api

class StockLot(models.Model):
    _inherit = 'stock.lot'
    flower_id = fields.Many2one(
        'flower.flower',
        related='product_id.flower_id',
        store=True,
        string='Flower'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product = self.env['product.product'].browse(vals['product_id'])
            if product.sequence_id:
                vals['name'] = product.sequence_id.next_by_id()
        return super().create(vals_list)
