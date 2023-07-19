from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class SoilCBR(models.Model):
    _name = "mechanical.soil.cbr"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="California Bearing Ratio")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.soil.cbr.line','parent_id',string="Parameter")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(SoilCBR, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record



class SoilCBRLine(models.Model):
    _name = "mechanical.soil.cbr.line"
    parent_id = fields.Many2one('mechanical.soil.cbr',string="Parent Id")

    penetration = fields.Float(string="Penetration in mm")
    proving_reading = fields.Float(string="Proving Ring Reading")
    load = fields.Float(string="Load in Kg", compute="_compute_load")


    @api.depends('proving_reading')
    def _compute_load(self):
        for record in self:
            record.load = record.proving_reading * 6.96


  

   