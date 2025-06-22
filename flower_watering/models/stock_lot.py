# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields
from datetime import timedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'

    water_record_ids = fields.One2many(
        comodel_name='flower.water',
        inverse_name='lot_id',
        string='Watering Records'
    )


    name_plant = fields.Char(string="اسم النبتة")  # تأكد من كتابة Char وليس Chr

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    city = fields.Char(related='warehouse_id.partner_id.city', string='City', store=True)



    watering_date = fields.Datetime(
        string='Watering Date',
        default=None,  # اجعلها فارغة للسماح للمستخدم بالإدخال
        required=True
    )
    next_watering_date = fields.Datetime(
        string='Next Watering Date',
        store=True
    )
    note = fields.Text(string='Note')
    # sellected=fields.Boolean("Sellected")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Watered By',
        default=lambda self: self.env.user
    )

    weather_datetime = fields.Datetime(string='Weather Time', required=True)
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    pressure = fields.Float(string='Pressure (hPa)')
    rain_mm = fields.Float(string='Rain Volume (mm)')

    def action_create_water_record(self):
        if len(self) != 1:
            raise UserError("يرجى تحديد سجل واحد فقط.")

        rec = self[0]
        weather_vals = {
            'weather_datetime': fields.Datetime.now(),
            'temperature': 0.0,
            'humidity': 0.0,
            'pressure': 0.0,
            'rain_mm': 0.0,
        }

        if rec.warehouse_id:
            WeatherModel = self.env['stock.warehouse.weather']
            last_weather = WeatherModel.search(
                [('warehouse_id', '=', rec.warehouse_id.id)],
                order='weather_datetime desc',
                limit=1
            )
            if last_weather:
                weather_vals = {
                    'weather_datetime': last_weather.weather_datetime,
                    'temperature': last_weather.temperature,
                    'humidity': last_weather.humidity,
                    'pressure': last_weather.pressure,
                    'rain_mm': last_weather.rain_mm,
                }

        return {
            'name': 'Water Now',
            'type': 'ir.actions.act_window',
            'res_model': 'flower.water',
            'view_mode': 'form,list',
            'context': {
                'default_lot_id': rec.id,
                'default_name_plant': rec.name_plant,
                'default_user_id': self.env.uid,
                'default_warehouse_id': rec.warehouse_id.id,
                'default_weather_datetime': weather_vals['weather_datetime'],
                'default_temperature': weather_vals['temperature'],
                'default_humidity': weather_vals['humidity'],
                'default_pressure': weather_vals['pressure'],
                'default_rain_mm': weather_vals['rain_mm'],
            },
            'target': 'current',
        }

    def action_bulk_water(self):
        FlowerWater = self.env['flower.water']
        WeatherModel = self.env['stock.warehouse.weather']

        for rec in self:
            # جلب آخر سجل ري للنبتة
            last_record = FlowerWater.search([
                ('lot_id', '=', rec.id)
            ], order='watering_date desc', limit=1)

            if last_record:
                watering_date = last_record.watering_date + timedelta(days=last_record.watering_frequency)
            else:
                watering_date = fields.Datetime.now()

            next_watering_date = watering_date + timedelta(days=7)

            # جلب بيانات الطقس للمخزن المرتبط
            weather_vals = {
                'weather_datetime': False,
                'temperature': 0.0,
                'humidity': 0.0,
                'pressure': 0.0,
                'rain_mm': 0.0,
            }

            if rec.warehouse_id:
                last_weather = WeatherModel.search(
                    [('warehouse_id', '=', rec.warehouse_id.id)],
                    order='weather_datetime desc',
                    limit=1
                )
                if last_weather:
                    weather_vals = {
                        'weather_datetime': last_weather.weather_datetime,
                        'temperature': last_weather.temperature,
                        'humidity': last_weather.humidity,
                        'pressure': last_weather.pressure,
                        'rain_mm': last_weather.rain_mm,
                    }

            # إنشاء سجل السقي مع بيانات الطقس
            FlowerWater.create({
                'lot_id': rec.id,
                'watering_date': watering_date,
                'next_watering_date': next_watering_date,
                'user_id': self.env.uid,
                'note': 'Auto watering from list view',
                'name_plant': rec.name_plant,
                'warehouse_id': rec.warehouse_id.id if rec.warehouse_id else False,
                'weather_datetime': weather_vals['weather_datetime'],
                'temperature': weather_vals['temperature'],
                'humidity': weather_vals['humidity'],
                'pressure': weather_vals['pressure'],
                'rain_mm': weather_vals['rain_mm'],
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Water Records',
            'res_model': 'flower.water',
            'view_mode': 'tree,form',
            'target': 'new',
            'domain': [('lot_id', 'in', self.ids)],
        }

    def print_custom_pdf(self):
        all_records = self.env['flower.water'].search([])
        return self.env.ref('flower_watering.report_screen_flower_water_ashraf').report_action(all_records)

    def action_fetch_weather(self):
        self.env['stock.warehouse'].action_fix_partner_city()
        self.env['stock.warehouse'].fetch_and_process_weather()

        raise UserError("تم جلب بيانات الطقس وتسجيلها بنجاح.")
