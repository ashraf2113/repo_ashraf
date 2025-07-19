from datetime import date
from odoo import api, fields, models



class Customers(models.Model):
    _name = "customers"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = "CUSTOMERS "
    _rec_name="name"

    name = fields.Char(string="Name")
    image=fields.Image(string="Image")
    note=fields.Html(string="Note")
    age=fields.Integer(string="Age")
    gender=fields.Selection([('male','Male'),('female','Female')],string="Gender")
    refs = fields.Char(string="Reference")
    booking_date = fields.Date(string="booking Date" ,default=fields.Date.context_today)
    prescription=fields.Html("Prescription")
    appoint_time=fields.Datetime("Appoint Time",default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', string='Partner')

    hide_field_from_here=fields.Boolean("Hide Field From Here")

    customers_lines_ids=fields.One2many("customers.lines","customers_id",string="Pharmacy")

class CustomersLines(models.Model):
    _name = "customers.lines"
    _description = "Customers Lines "    

    customers_id=fields.Many2one("customers")

    product_id=fields.Many2one("product.product",string="Product")

    
    qty=fields.Integer("Quantity")
    price=fields.Float(related="product_id.standard_price", string="Price")

    other_product_id=fields.Many2one("sale.order.line",string="Other Product")
    qtys=fields.Integer("Quantity Other product")
    prices=fields.Float(related="other_product_id.price_unit" ,string="Price Other Product")

 