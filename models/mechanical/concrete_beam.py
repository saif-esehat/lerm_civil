from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class FlexuralStrengthConcreteBeam(models.Model):
    _name = "mechanical.flexural.strength.concrete.beam"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Flexural Strength of Concrete Beam")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.flexural.strength.concrete.beam.line','parent_id',string="Parameter")

    length = fields.Integer(string="Length of span ( L ) in mm", default=600)
    average_flexural_strength = fields.Float(string="Average Flexural Strength in N/mm2")


    # @api.depends('child_lines.flexural_strength', 'child_lines.flexural_strength_3')
    # def _compute_average_flexural_strength(self):
    #     for record in self:
    #         total_strength = sum(line.flexural_strength for line in record.child_lines) + sum(line.flexural_strength_3 for line in record.child_lines)
    #         total_lines = len(record.child_lines) * 2  # Counting both flexural_strength and flexural_strength_3
    #         record.average_flexural_strength = total_strength / total_lines if total_lines > 0 else 0.0

    are_child_lines_filled = fields.Boolean(compute='_compute_are_child_lines_filled', store=False)

    @api.depends('child_lines.flexural_strength', 'child_lines.flexural_strength_3')  # Replace with actual field names
    def _compute_are_child_lines_filled(self):
        for record in self:
            all_lines_filled = all(line.flexural_strength and line.flexural_strength_3 for line in record.child_lines)
            record.are_child_lines_filled = all_lines_filled



    def average_flexural_calculation(self):
        print('<<<<<<<<<<<<')
        for record in self:
            data = self.child_lines
           
            result = 0  # Initialize result before the loop
            print(data, 'data')
            line1flexural_strength = data[0].flexural_strength
            line2flexural_strength = data[1].flexural_strength
            line3flexural_strength = data[2].flexural_strength_3
            result = (line1flexural_strength+line2flexural_strength+line3flexural_strength) / 3
            print(result, 'final result')
        self.write({'average_flexural_strength': result})

 

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(FlexuralStrengthConcreteBeam, self).create(vals)
        record.parameter_id.write({'model_id':record.id})
        return record

class FlexuralStrengthConcreteBeamLine(models.Model):
    _name = "mechanical.flexural.strength.concrete.beam.line"
    parent_id = fields.Many2one('mechanical.flexural.strength.concrete.beam',string="Parent Id")

    sr_no = fields.Integer(string="ID MARK/ Location", readonly=True, copy=False, default=1)
   
    depth = fields.Float(string="Depth (d) in mm")
    width = fields.Float(string="Width (mm)")
    wt_of_sample = fields.Float(string="Weight of Sample in kgs")
    fracture_distance = fields.Float(string="Fracture Distance from neaere support in Cm")
    failure_load  = fields.Float(string="Failure Load in kN")
    flexural_strength = fields.Float(string="Flexural Strength in N/mm2", compute="_compute_flexural_strength")
    flexural_strength_3 = fields.Float(string="Flexural Strength in N/mm2", compute="_compute_flexural_strength_three")

    @api.depends('failure_load', 'parent_id.length', 'depth', 'width')
    def _compute_flexural_strength(self):
        for record in self:
            if record.parent_id.length and record.depth and record.width and record.failure_load:
                record.flexural_strength = (record.failure_load * record.parent_id.length) / (record.depth * record.width * record.width) * 1000
            else:
                record.flexural_strength = 0.0


    @api.depends('failure_load', 'parent_id.length', 'depth', 'width')
    def _compute_flexural_strength_three(self):
        for record in self:
            if record.parent_id.length and record.depth and record.width and record.failure_load:
                record.flexural_strength_3 = (record.failure_load * record.parent_id.length * 10) / (record.depth * record.width * record.width)
            else:
                record.flexural_strength_3 = 0.0


    


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(FlexuralStrengthConcreteBeamLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



   

  