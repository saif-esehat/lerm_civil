from odoo import api, fields, models
from decimal import Decimal


class CementCompatablity(models.Model):
    _name = "mechanical.cement.compatiblity"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="Compatiblity")
    
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    temp_percent_normal = fields.Float("Temperature °C")
    humidity_percent_normal = fields.Float("Humidity %")
    start_date_normal = fields.Date("Start Date")
    end_date_normal = fields.Date("End Date")
    child_lines = fields.One2many('mechanical.cement.compatiblity.lines','parent_id',string="Parameters")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CementCompatablity, self).create(vals)
        record.eln_ref.write({'model_id':record.id})
        return record


class CementCompatablityLines(models.Model):
    _name = "mechanical.cement.compatiblity.lines"
    parent_id = fields.Many2one('mechanical.cement.compatiblity',string="Parent Id")
    water_cement_ratio = fields.Float("Water Cement Ratio (w/c)",compute="_compute_water_cement_ratio")
    admixture_dosage_percent = fields.Float("Admixture Dosage %")
    wt_of_cement = fields.Float("Wt. of  Cement (g)")
    wt_of_water = fields.Float("Wt.of water  (g)")
    wt_of_admixture = fields.Float("Wt. of Admixture (g)",compute="_compute_wt_of_admixture")
    flow_sec = fields.Float("Flow (Sec)")
    flow_30_min = fields.Float("Flow at 30 Min (Sec)")
    flow_60_min = fields.Float("Flow at 60 Min (Sec)")



    @api.depends('wt_of_water', 'wt_of_cement')
    def _compute_water_cement_ratio(self):
        for record in self:
            if record.wt_of_cement != 0:
                record.water_cement_ratio = Decimal(record.wt_of_water) / Decimal(record.wt_of_cement)
            else:
                record.water_cement_ratio = 0

    @api.depends('admixture_dosage_percent', 'wt_of_cement')
    def _compute_wt_of_admixture(self):
        for record in self:
            if record.admixture_dosage_percent != 0:
                record.wt_of_admixture = Decimal(record.wt_of_cement) / (Decimal(record.admixture_dosage_percent) * 100)
            else:
                record.wt_of_admixture = 0
    


