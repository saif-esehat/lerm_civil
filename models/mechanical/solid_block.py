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


class BlockDensity(models.Model):
    _name = "mechanical.block.density"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Block Density")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.block.density.line','parent_id',string="Parameter")
    average_block = fields.Float(string="Average", compute="_compute_average_block")


    @api.depends('child_lines.block_density')
    def _compute_average_block(self):
        for record in self:
            block_densities = record.child_lines.mapped('block_density')
            if block_densities:
                record.average_block = sum(block_densities) / len(block_densities)
            else:
                record.average_block = 0.0


  

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(BlockDensity, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class BlockDensityLine(models.Model):
    _name = "mechanical.block.density.line"
    parent_id = fields.Many2one('mechanical.block.density',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    length = fields.Float(string="Length (mm)")
    heigth = fields.Float(string="Height (mm)")
    thickness = fields.Float(string="Thickness (mm)")
    volume = fields.Float(string="Volume (Cm3)", compute="_compute_volume")
    intial_wt = fields.Float(string="Initial Weight of the Specimen (kg)")
    final_wt = fields.Float(string="Final Weight of the Specimen after Oven Dry (kg) (Constant)")
    block_density = fields.Float(string="Block Density (kg/M³)", compute="_compute_block_density")

    

    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(BlockDensityLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1


   



    @api.depends('length','heigth','thickness')
    def _compute_volume(self):
        for record in self:
            record.volume = record.length * record.heigth * record.thickness


    @api.depends('final_wt','volume')
    def _compute_block_density(self):
        for record in self:
            if record.volume != 0:
                record.block_density = record.final_wt / record.volume * 1000000
            else:
                record.block_density = 0.0
   



   




