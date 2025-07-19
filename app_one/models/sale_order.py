from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    property_id=fields.Many2one("property")
    def action_confirm(self):
        res=super(SaleOrder,self).action_confirm()
        print("insid method action_confirm ashrofaaa")
        return res
    def call_print_method(self):
        pass
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    product_sequence = fields.Char(string="Ashraf Sequence", readonly=True)

    @api.model
    def create(self, vals):
        product_template_id = vals.get('product_template_id')
        if product_template_id:
            # استخدم ID الخاص بـ product.template
            sequence_code = f'product.template.sequence.{product_template_id}'
            sequence = self.env['ir.sequence'].search([('code', '=', sequence_code)], limit=1)
            if not sequence:
                # إنشاء sequence جديد لهذا المنتج إن لم يكن موجود
                template = self.env['product.template'].browse(product_template_id)
                sequence = self.env['ir.sequence'].create({
                    'name': f'Sequence for {template.name}',
                    'code': sequence_code,
                    'prefix': f'{template.name[:3].upper()}',
                    'padding': 5,
                    'number_increment': 1,
                    'implementation': 'no_gap',
                })
            vals['product_sequence'] = sequence.next_by_code(sequence_code)
        return super(SaleOrderLine, self).create(vals)
