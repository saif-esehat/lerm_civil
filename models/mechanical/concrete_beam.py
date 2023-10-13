from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
from datetime import datetime , timedelta


class FlexuralStrengthConcreteBeam(models.Model):
    _name = "mechanical.flexural.strength.concrete.beam"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Flexural Strength of Concrete Beam")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines = fields.One2many('mechanical.flexural.strength.concrete.beam.line','parent_id',string="Parameter")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
    
    average_flexural_strength = fields.Float(string="Average Flexural Strength in N/mm2",compute="_compute_average_flexural_strength")


    age_of_days = fields.Selection([
        ('3days', '3 Days'),
        ('7days', '7 Days'),
        ('14days', '14 Days'),
        ('28days', '28 Days'),
    ], string='Age', default='28days',required=True)
    date_of_casting = fields.Date(string="Date of Casting")
    date_of_testing = fields.Date(string="Date of Testing",compute="_compute_testing_date")
    confirmity = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ], string='Confirmity', default='fail',compute="_compute_average_flexural_strength_conformity")


    @api.depends('date_of_casting','age_of_days')
    def _compute_testing_date(self):
        for record in self:
            if record.date_of_casting:
                if record.age_of_days == "3days":
                    cast_date = fields.Datetime.from_string(record.date_of_casting)
                    testing_date = cast_date + timedelta(days=3)
                    record.date_of_testing = fields.Datetime.to_string(testing_date)
                elif record.age_of_days == "7days":
                    cast_date = fields.Datetime.from_string(record.date_of_casting)
                    testing_date = cast_date + timedelta(days=7)
                    record.date_of_testing = fields.Datetime.to_string(testing_date)
                elif record.age_of_days == "14days":
                    cast_date = fields.Datetime.from_string(record.date_of_casting)
                    testing_date = cast_date + timedelta(days=14)
                    record.date_of_testing = fields.Datetime.to_string(testing_date)
                elif record.age_of_days == "28days":
                    cast_date = fields.Datetime.from_string(record.date_of_casting)
                    testing_date = cast_date + timedelta(days=28)
                    record.date_of_testing = fields.Datetime.to_string(testing_date)
                else:
                    record.date_of_testing = False
            else:
                record.date_of_testing = False

    @api.depends('average_flexural_strength','eln_ref')
    def _compute_average_flexural_strength_conformity(self):
        for record in self:
            record.confirmity = 'fail'
            line = self.env['lerm.parameter.master'].search([('internal_id','=','19edc74f-c7b2-45b6-8696-e97c19e81993')])
            materials = self.env['lerm.parameter.master'].search([('internal_id','=','19edc74f-c7b2-45b6-8696-e97c19e81993')]).parameter_table
            for material in materials:
                
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    
                    lower = record.average_flexural_strength - record.average_flexural_strength*mu_value
                    upper = record.average_flexural_strength + record.average_flexural_strength*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.confirmity = 'pass'
                        break
                    else:
                        record.confirmity = 'fail'


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        for record in self:
            if record.eln_ref:
                grade = record.eln_ref.grade_id.id
                print("Grade beam",grade)
                record.grade = record.eln_ref.grade_id.id

    @api.depends('child_lines.flexural_strength')
    def _compute_average_flexural_strength(self):
        for record in self:
            total_strength = sum(line.flexural_strength for line in record.child_lines)
            total_lines = len(record.child_lines)
            record.average_flexural_strength = total_strength / total_lines if total_lines > 0 else 0.0


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(FlexuralStrengthConcreteBeam, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        test = record.eln_ref
        print("test",test)

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
        record = self.env['mechanical.flexural.strength.concrete.beam'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values
    




    
class FlexuralStrengthConcreteBeamLine(models.Model):
    _name = "mechanical.flexural.strength.concrete.beam.line"
    parent_id = fields.Many2one('mechanical.flexural.strength.concrete.beam',string="Parent Id")

    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    id_mark = fields.Integer(string="ID MARK/ Location")
    length = fields.Integer(string="Length of span ( L ) in mm")
    depth = fields.Float(string="Depth (d) in mm")
    width = fields.Float(string="Width (mm)")
    wt_of_sample = fields.Float(string="Weight of Sample in kgs")
    fracture_distance = fields.Float(string="Fracture Distance from neaere support in Cm")
    failure_load  = fields.Float(string="Failure Load in kN")
    flexural_strength = fields.Float(string="Flexural Strength in N/mm2", compute="_compute_flexural_strength")
    # flexural_strength_3 = fields.Float(string="Flexural Strength in N/mm2", compute="_compute_flexural_strength_three")

    @api.depends('failure_load', 'length', 'depth', 'width')
    def _compute_flexural_strength(self):
        for record in self:
            if record.length and record.depth and record.width and record.failure_load:
                record.flexural_strength = (record.failure_load * record.length) / (record.depth * record.width * record.width) * 1000
            else:
                record.flexural_strength = 0.0

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