from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
from datetime import datetime , timedelta


class MechanicalConcreteCube(models.Model):
    _name = "mechanical.concrete.cube"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Compressive Strength of Concrete Cube")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    child_lines = fields.One2many('mechanical.concrete.cube.line','parent_id',string="Parameter")
    average_strength = fields.Float(string="Average Compressive Strength in N/mm2", compute="_compute_average_strength",digits=(12,2))
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
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
    ], string='Confirmity', default='fail',compute="_compute_confirmity")
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    
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
            

    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id


    @api.depends('average_strength','eln_ref','grade','age_of_days')
    def _compute_confirmity(self):
        for record in self:
            record.confirmity = 'fail'
            line = self.env['lerm.parameter.master'].search([('internal_id','=','eb26db03-17c1-48ac-8462-9671e4d3d09f')])
            materials = self.env['lerm.parameter.master'].search([('internal_id','=','eb26db03-17c1-48ac-8462-9671e4d3d09f')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    if record.age_of_days == "3days":
                        req_min = req_min * 0.5
                        req_max = req_max* 0.5
                    if record.age_of_days == "7days":
                        req_min = req_min * 0.7
                        req_max = req_max* 0.7
                    if record.age_of_days == "14days":
                        req_min = req_min * 0.9
                        req_max = req_max* 0.9
                    lower = record.average_strength - record.average_strength*mu_value
                    upper = record.average_strength + record.average_strength*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.confirmity = 'pass'
                        break
                    else:
                        record.confirmity = 'fail'


    

    @api.depends('child_lines.compressive_strength')
    def _compute_average_strength(self):
        for record in self:
            total_strength = sum(line.compressive_strength for line in record.child_lines)
            record.average_strength = total_strength / len(record.child_lines) if len(record.child_lines) > 0 else 0.0


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id


    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(MechanicalConcreteCube, self).create(vals)
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
        record = self.env['mechanical.concrete.cube'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values



class MechanicalConcreteCubeLine(models.Model):
    _name = "mechanical.concrete.cube.line"
    parent_id = fields.Many2one('mechanical.concrete.cube',string="Parent Id")

    sr_no = fields.Integer(string="Sr.No.",readonly=True, copy=False, default=1)
    length = fields.Float(string="Length (mm)")
    width = fields.Float(string="Width (mm)")
    area = fields.Float(string="Area (mm²)",compute="_compute_area" ,digits=(12,1))
    id_mark = fields.Char(string="ID Mark/Location")
    wt_sample = fields.Float(string="Weight of Sample in kgs")
    crushing_load = fields.Float(string="Crushing Load in kN")
    compressive_strength = fields.Float(string="Compressive Strength N/mm²",compute="_compute_compressive_strength" ,digits=(12,2))
   

    @api.depends('length', 'width')
    def _compute_area(self):
        for record in self:
            record.area = round((record.length * record.width) , 4)


    @api.depends('crushing_load', 'area')
    def _compute_compressive_strength(self):
        for record in self:
            if record.area != 0:
                record.compressive_strength = record.crushing_load / record.area * 1000
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

        return super(MechanicalConcreteCubeLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1