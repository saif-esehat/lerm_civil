from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class CompressiveStrength(models.Model):
    _name = "mechanical.compressive.strength"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Compressive Strength")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.compressives.strength.line','parent_id',string="Parameter")
    average_strength = fields.Float(string="Average", compute="_compute_average_strength")


    @api.depends('child_lines.compressive_strength')
    def _compute_average_strength(self):
        for record in self:
            total_strength = sum(line.compressive_strength for line in record.child_lines)
            record.average_strength = total_strength / len(record.child_lines) if len(record.child_lines) > 0 else 0.0



    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CompressiveStrength, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class CompressiveStrengthLine(models.Model):
    _name = "mechanical.compressives.strength.line"
    parent_id = fields.Many2one('mechanical.compressive.strength',string="Parent Id")

    sr_no = fields.Integer(string="Sr.No.")
    length = fields.Integer(string="Length (mm)")
    width = fields.Integer(string="Width (mm)")
    thickness = fields.Integer(string="Thickness (mm)")
    area = fields.Integer(string="Area (mm²)", compute="_compute_area")
    load = fields.Float(string="Load (N)")
    compressive_strength = fields.Float(string="Compressive Strength N/mm²", compute="_compute_compressive_strength")
   


    @api.depends('width', 'thickness')
    def _compute_area(self):
        for record in self:
            record.area = record.width * record.thickness


    @api.depends('load', 'area')
    def _compute_compressive_strength(self):
        for record in self:
            if record.area != 0:
                record.compressive_strength = record.load / record.area * 1000
            else:
                record.compressive_strength = 0.0

   




