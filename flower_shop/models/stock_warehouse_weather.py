from odoo import models, fields

class StockWarehouseWeather(models.Model):
    _name = 'stock.warehouse.weather'
    _description = "Warehouse Weather Information"

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True)
    description = fields.Char(string="Weather Description")
    pressure = fields.Float(string="Pressure (hPa)")
    temperature = fields.Float(string="Temperature (°C)")
    humidity = fields.Float(string="Humidity")
    wind_speed = fields.Float(string="Wind Speed (m/s)")
    rain_volume = fields.Float(string="Rain Volume (mm)")
    capture_time = fields.Datetime(string="Capture Time", default=fields.Datetime.now)
