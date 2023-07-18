from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class CoverMeter(models.Model):
    _name = "ndt.cover.meter"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Cover Meter")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('ndt.cover.meter.line','parent_id',string="Parameter")

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CoverMeter, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CrackDepthLine(models.Model):
    _name = "ndt.cover.meter.line"
    parent_id = fields.Many2one('ndt.cover.meter',string="Parent Id")
    member = fields.Char(string="Member")
    location = fields.Char(string="Location")
    level = fields.Char(string="Level")
    cover = fields.Float(string='Cover in mm')
    


                


