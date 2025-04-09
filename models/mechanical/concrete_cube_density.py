from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math
from datetime import datetime , timedelta


class MechanicalConcreteCubeDensity(models.Model):
    _name = "mechanical.concrete.cube.density"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="  Concrete Cube Density")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="ELN")
    
    # age_of_days = fields.Selection([
    #     ('3days', '3 Days'),
    #     ('7days', '7 Days'),
    #     ('14days', '14 Days'),
    #     ('21days', '21 Days'),
    #     ('28days', '28 Days'),
    #     ('45days', '45 Days'),
    #     ('56days', '56 Days'),
    #     ('112days', '112 Days'),
    # ], string='Age', default='28days',required=True,compute="_compute_age_of_days")
    date_of_casting = fields.Date(string="Date of Casting",compute="compute_date_of_casting")
    # date_of_testing = fields.Date(string="Date of Testing")

    child_lines_core_density = fields.One2many('mechanical.concrete.cube.density.line','parent_id',string="Parameter")

    average_core_density = fields.Float(string="Avg (kg/m3)",compute="_compute_average_core_density")


    average_core_density_conformity = fields.Selection([
            ('pass', 'Pass'),
            ('fail', 'Fail')], string="Conformity", compute="_compute_average_core_density_conformity", store=True)



    @api.depends('average_core_density','eln_ref','grade')
    def _compute_average_core_density_conformity(self):
        
        for record in self:
            record.average_core_density_conformity = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','235487yt5-7a9c-4616-bad5-88eb1b29087y')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','235487yt5-7a9c-4616-bad5-88eb1b29087y')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    req_min = material.req_min
                    req_max = material.req_max
                    mu_value = line.mu_value
                    
                    lower = record.average_core_density - record.average_core_density*mu_value
                    upper = record.average_core_density + record.average_core_density*mu_value
                    if lower >= req_min and upper <= req_max:
                        record.average_core_density_conformity = 'pass'
                        break
                    else:
                        record.average_core_density_conformity = 'fail'

    average_core_density_nabl = fields.Selection([
        ('pass', 'NABL'),
        ('fail', 'Non-NABL')], string="NABL", compute="_compute_average_core_density_nabl", store=True)

    @api.depends('average_core_density','eln_ref','grade')
    def _compute_average_core_density_nabl(self):
        
        for record in self:
            record.average_core_density_nabl = 'fail'
            line = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','235487yt5-7a9c-4616-bad5-88eb1b29087y')])
            materials = self.env['lerm.parameter.master'].sudo().search([('internal_id','=','235487yt5-7a9c-4616-bad5-88eb1b29087y')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    lab_min = line.lab_min_value
                    lab_max = line.lab_max_value
                    mu_value = line.mu_value
                    
                    lower = record.average_core_density - record.average_core_density*mu_value
                    upper = record.average_core_density + record.average_core_density*mu_value
                    if lower >= lab_min and upper <= lab_max:
                        record.average_core_density_nabl = 'pass'
                        break
                    else:
                        record.average_core_density_nabl = 'fail'



    @api.depends('child_lines_core_density.density')
    def _compute_average_core_density(self):
        for record in self:
            total_value = sum(record.child_lines_core_density.mapped('density'))
            record.average_core_density = round((total_value / len(record.child_lines_core_density) if record.child_lines_core_density else 0.0),2)

   
   
    
    @api.onchange('eln_ref')
    def compute_date_of_casting(self):
        for record in self:
            if record.eln_ref.sample_id:
                sample_record = self.env['lerm.srf.sample'].sudo().search([('id','=', record.eln_ref.sample_id.id)]).date_casting
                record.date_of_casting = sample_record
            else:
                record.date_of_casting = None



    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id



     
    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(MechanicalConcreteCubeDensity, self).create(vals)
        # record.get_all_fields()
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
        record = self.env['mechanical.concrete.core.density'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values




class ConcreteCubeDensityLine(models.Model):
    _name = "mechanical.concrete.cube.density.line"
    parent_id = fields.Many2one('mechanical.concrete.cube.density',string="Parent Id")

    sr_no = fields.Integer(string="Sample",readonly=True, copy=False, default=1)
    id_location = fields.Char(string="ID MARK/ Location")
    weight = fields.Float(string="Weight ( Kg )",digits=(12,3))
    length = fields.Float(string="Length ( mm )",digits=(12,2))
    width = fields.Float(string="Width ( mm )",digits=(12,2))
    height = fields.Float(string="Height  ( mm )",digits=(12,2))
    volume = fields.Float(string="Volume (mm3)",compute="_compute_volume_and_density", store=True)
    density = fields.Float(string="Density (Kg/m3 )",compute="_compute_volume_and_density", store=True,digits=(16,2))


    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        for record in self:
            parent = record.parent_id.sudo()
            sample_id = parent.eln_ref.sample_id.client_sample_id
            if sample_id:
                record.id_location = sample_id
            else:
                record.id_location = ""

    @api.onchange('id_location')
    def _onchange_id_location(self):
        for record in self:
            if record.id_location and not record.parent_id.eln_ref.sample_id.client_sample_id:
                record.parent_id.eln_ref.sample_id.client_sample_id = record.id_location


    @api.depends('length', 'height', 'width','weight')
    def _compute_volume_and_density(self):
        for record in self:
            if record.length and record.height and record.width:
                # Calculate volume in mm³ using the formula: π/4 * d^2 * h
                record.volume = (record.length * record.width * record.height)
            else:
                record.volume = 0.0

            if record.volume > 0 and record.weight:
                # Convert volume from mm³ to m³ and compute density
                record.density = record.weight / (record.volume / 1e9)  # since 1 m³ = 1e9 mm³
            else:
                record.density = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(ConcreteCubeDensityLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



import json
import base64
import qrcode
from io import BytesIO
from lxml import etree

class ConcreteCubeDensityDatasheet(models.AbstractModel):
        _name = 'report.lerm_civil.concrete_cube_density_datasheet'
        _description = 'Concrete Cube Density DataSheet'
    
        @api.model
        def _get_report_values(self, docids, data):
            if data['fromsample'] == True:
                 if 'active_id' in data['context']:
                     eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
                 else:
                     eln = self.env['lerm.eln'].sudo().browse(docids) 
            else:
                if data['report_wizard'] == True:
                    eln = self.env['lerm.eln'].sudo().search([('id','=',data['eln'])])
                else:
                    eln = self.env['lerm.eln'].sudo().browse(data['eln_id'])
            model_id = eln.model_id
            # differnt location for product based
            # model_name = eln.material.product_based_calculation[0].ir_model.name 
            model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
            if model_name:
                general_data = self.env[model_name].sudo().browse(model_id)
            else:
                general_data = self.env['lerm.eln'].sudo().browse(docids)
            return {
                'eln': eln,
                'data' : general_data
            }



class ConcreteCubeDensityReport(models.AbstractModel):
    _name = 'report.lerm_civil.concrete_cube_density_report'
    _description = 'Concrete Cube Density Report'
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        nabl = data.get('nabl')
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        # qr.add_data(eln.kes_no)
        url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')]).value
        url = url +'/download_report/'+ str(eln.id)
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        model_id = eln.model_id
        # differnt location for product based
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'qrcode': qr_code,
            'stamp' : inreport_value,
            'nabl' : nabl
        }