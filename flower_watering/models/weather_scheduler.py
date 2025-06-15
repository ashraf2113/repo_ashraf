import requests
from odoo import models, fields, api
from datetime import datetime, timedelta

class WeatherScheduler(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def fetch_and_process_weather(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('flower_watering.weather_api_key')
        if not api_key:
            return

        for warehouse in self.search([]):
            if not warehouse.partner_id or not warehouse.partner_id.city:
                continue

            city = warehouse.partner_id.city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            try:
                response = requests.get(url)
                data = response.json()
            except Exception:
                continue

            rain = data.get('rain', {}).get('1h', 0.0)  # مطر الساعة الأخيرة
            weather_time = fields.Datetime.now()

            self.env['stock.warehouse.weather'].create({
                'warehouse_id': warehouse.id,
                'weather_datetime': weather_time,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'rain_mm': rain
            })

            # تنفيذ الري لو كان المطر > 0.2mm
            if 9 <= weather_time.hour <= 18 and rain > 0.2:
                lots = self.env['stock.lot'].search([('warehouse_id', '=', warehouse.id)])
                for lot in lots:
                    self.env['flower.water'].create({
                        'lot_id': lot.id,
                        'watering_date': weather_time,
                        'note': f"Auto watering from weather at {city}",
                        'name_plant': lot.name_plant,
                        'user_id': self.env.uid
                    })
