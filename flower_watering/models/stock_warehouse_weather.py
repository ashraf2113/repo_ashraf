from odoo.exceptions import UserError
from odoo import models, fields
from datetime import timedelta
class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = 'Warehouse Weather Info'

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    weather_datetime = fields.Datetime(string='Weather Time', required=True)
    temperature = fields.Float(string='Temperature (°C)')
    humidity = fields.Float(string='Humidity (%)')
    pressure = fields.Float(string='Pressure (hPa)')
    rain_mm = fields.Float(string='Rain Volume (mm)')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather_api_key = fields.Char(string="Weather API Key", config_parameter="flower_watering.weather_api_key")
