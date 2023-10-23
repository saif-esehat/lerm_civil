from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math

class ConcreteSplitTensileStrength(models.Model):
    _name = "mechanical.concrete.split.tensile"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Concrete Split Tensile Strength")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")



    splite_tensile_name = fields.Char("Name",default="Concrete Split Tensile Strength")
    splite_tensile_visible = fields.Boolean("Concrete Split Tensile Strength Visible",compute="_compute_visible")
    child_lines = fields.One2many('mechanical.concrete.split.tensile.line','parent_id',string="Parameter")
    average_split_tensile = fields.Float(string="Average Split Tensile Strength (N/mm2)",compute="_compute_average_split_tensile")


    @api.depends('child_lines.split_strength')
    def _compute_average_split_tensile(self):
        for record in self:
            split_strengths = record.child_lines.mapped('split_strength')
            if split_strengths:
                record.average_split_tensile = sum(split_strengths) / len(split_strengths)
            else:
                record.average_split_tensile = 0.0


    
   
    ### Compute Visible
    @api.depends('sample_parameters')
    def _compute_visible(self):
        
        for record in self:
            record.splite_tensile_visible = False
           
           
            
            for sample in record.sample_parameters:
                print("Internal Ids",sample.internal_id)

                if sample.internal_id == "51ff18a6-226c-4dbf-9389-7cc72b090e66":
                    record.splite_tensile_visible = True

               


                




               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(ConcreteSplitTensileStrength, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record







    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        # records = self.env['lerm.eln'].search([('id','=', record.eln_id.id)]).parameters_result
        # print("records",records)
        # self.sample_parameters = records
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)



    def get_all_fields(self):
        record = self.env['mechanical.concrete.split.tensile'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values
    

class ConcreteSplitTensileStrengthLine(models.Model):
    _name = "mechanical.concrete.split.tensile.line"
    parent_id = fields.Many2one('mechanical.concrete.split.tensile',string="Parent Id")

    sr_no = fields.Integer(string="Sr.No.",readonly=True, copy=False, default=1)
    id_mark = fields.Char(string="ID MARK/ Location")
    wt_of_cylender = fields.Float(string="Weight of Cylinder Kg")
    height = fields.Float(string="Height mm")
    diameter = fields.Float(string="Diameter mm")
    breaking_load = fields.Float(string="Breaking Load KN")
    split_strength = fields.Float(string="Split Tensile Strength N/mm2",compute="_compute_split_strength")



    @api.depends('breaking_load', 'height', 'diameter')
    def _compute_split_strength(self):
        for record in self:
            if record.breaking_load and record.height and record.diameter:
                record.split_strength = (2 * record.breaking_load) / (3.14 * record.height * record.diameter) * 1000
            else:
                record.split_strength = 0.0
    

   


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(ConcreteSplitTensileStrengthLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1