from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class CompressiveStrengthConcreteManHole(models.Model):
    _name = "compressive.strength.concrete.man.hole"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Compressive strength")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('compressive.strength.concrete.man.hole.line','parent_id',string="Parameter")
    average_compressive_strength = fields.Float(string="Average Compressive Strength N/mm2",compute="_compute_average_compressive_strength")


    @api.depends('child_lines.compressive_strength')
    def _compute_average_compressive_strength(self):
        for record in self:
            child_lines = record.child_lines.filtered(lambda line: line.compressive_strength)
            if child_lines:
                record.average_compressive_strength = sum(child_lines.mapped('compressive_strength')) / len(child_lines)
            else:
                record.average_compressive_strength = 0.0


    

    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CompressiveStrengthConcreteManHole, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

   

class CompressiveStrengthConcreteManHoleLine(models.Model):
    _name = "compressive.strength.concrete.man.hole.line"
    parent_id = fields.Many2one('compressive.strength.concrete.man.hole',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    crossectional_area = fields.Integer(string="Crosssectional area ( A ) mm2",  default=150 * 150, readonly=True)
    load = fields.Float(string="Load ( P ) KN")
    compressive_strength = fields.Float(string="Compressive strength",compute="_compute_compressive_strength")




    @api.depends('load', 'crossectional_area')
    def _compute_compressive_strength(self):
        for record in self:
            if record.load and record.crossectional_area:
                record.compressive_strength = (record.load * 1000) / record.crossectional_area
            else:
                record.compressive_strength = 0.0

   


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(CompressiveStrengthConcreteManHoleLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1