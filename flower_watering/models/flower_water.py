# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.exceptions import UserError

class FlowerWater(models.Model):
    _name = 'flower.water'
    _description = 'Flower Watering Record'
    _order = 'watering_date desc'

    lot_id = fields.Many2one(
        comodel_name='stock.lot',
        string='Flower (Serial Number)',
        required=True,
        ondelete='cascade'
    )

    # بدل الحقل القديم ده:
    # warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)

    # ✅ نعمله related من lot_id:
    warehouse_id = fields.Many2one(
        related='lot_id.warehouse_id',
        comodel_name='stock.warehouse',
        string='Warehouse',
        store=True,
        readonly=True
    )

    # ✅ نعمل حقل city برضو related:
    city = fields.Char(
        related='lot_id.warehouse_id.partner_id.city',
        string='City',
        store=True,
        readonly=True
    )

    watering_date = fields.Datetime(
        string='Watering Date',
        default=None,  # اجعلها فارغة للسماح للمستخدم بالإدخال
        required=True
    )

    name_plant=fields.Char("Name Plant")
    note = fields.Text(string='Note')
    # sellected=fields.Boolean("Sellected")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Watered By',
        default=lambda self: self.env.user
    )

    next_watering_date = fields.Datetime(
        string='Next Watering Date',
        compute='_compute_next_watering_date',
        store=True
    )

    watering_frequency = fields.Integer(
        string='Watering Frequency (Days)',
        default=7,
        help='Minimum number of days between watering'
    )
    weather_datetime = fields.Datetime(string='Weather Time', required=True)
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    pressure = fields.Float(string='Pressure (hPa)')
    rain_mm = fields.Float(string='Rain Volume (mm)')
    @api.depends('watering_date', 'watering_frequency')
    def _compute_next_watering_date(self):
        for record in self:
            if record.watering_date and record.watering_frequency:
                record.next_watering_date = record.watering_date + timedelta(days=record.watering_frequency)

    @api.constrains('watering_date', 'lot_id')
    def _check_watering_frequency(self):
        for record in self:
            if not record.lot_id:
                continue
            # احصل على آخر تاريخ سقي سابق للزهرة (بدون السجل الحالي)
            last_record = self.env['flower.water'].search([
                ('lot_id', '=', record.lot_id.id),
                ('id', '!=', record.id)
            ], order='watering_date desc', limit=1)

            if last_record and last_record.watering_date:
                min_date = last_record.watering_date + timedelta(days=last_record.watering_frequency)
                if record.watering_date < min_date:
                    raise ValidationError(_(
                        "Too early! The last watering was on %s. You should wait until at least %s.",
                        last_record.watering_date.strftime('%Y-%m-%d %H:%M'),
                        min_date.strftime('%Y-%m-%d %H:%M')
                    ))

    def action_fetch_weather(self):
        # self.env['stock.warehouse'].action_fix_partner_city()
        self.env['stock.warehouse'].fetch_and_process_weather()
        raise UserError("✅ تم تحديث بيانات الطقس وربط المدن بنجاح.")

