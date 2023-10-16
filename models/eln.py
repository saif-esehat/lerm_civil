from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError
from datetime import datetime
import math
from matplotlib import pyplot as plt
# import io
# from PIL import Image
# import base64



import base64
import json

class ELN(models.Model):
    _name = 'lerm.eln'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'eln_id'
    eln_id = fields.Char("ELN ID",required=True,readonly=True, default=lambda self: 'New')
    srf_id = fields.Many2one('lerm.civil.srf',string="SRF ID")
    technician = fields.Many2one('res.users',string="Technicians")
    sample_id = fields.Many2one('lerm.srf.sample',string='Sample ID')
    srf_date = fields.Date(string='SRF Date')
    kes_no = fields.Char(string="KES NO")
    discipline = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group = fields.Many2one('lerm_civil.group',string="Group")
    material = fields.Many2one('product.template',string='Material')
    witness_name = fields.Char(string="Witness Name")
    witness_description = fields.Char(string="Witness Description")
    witness_photo = fields.Binary(string="Witness Photo")
    witness_photo_name = fields.Char(string="Witness Photo Name")
    casting_date = fields.Date(string="Casting Date")
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")
    parameters = fields.One2many('eln.parameters','eln_id',string="Parameters")
    datasheets = fields.One2many('eln.spreadsheets','eln_id',string="Datasheets")
    fetch_ds_button = fields.Float(string="Fetch Datasheet")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    update_result = fields.Integer("Update Result")
    state = fields.Selection([
        ('1-draft', 'In-Test'),
        ('2-confirm', 'In-Check'),
        ('3-approved','Approved'),
        ('4-rejected','Rejected')
    ], string='State',default='1-draft')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    remarks = fields.Text("Remarks")
    parameters_result = fields.One2many('eln.parameters.result','eln_id',string="Parameters")
    parameters_input = fields.One2many('eln.parameters.inputs','eln_id',string="Parameters Inputs") 
    conformity = fields.Boolean(string="Conformity")
    has_witness = fields.Boolean(string="Witness")
    invisible_fetch_inputs = fields.Boolean(string="Fetch Inputs")
    name = fields.Char(string="Name")
    image = fields.Binary(string="Image", attachment=True)
    is_product_based_calculation = fields.Boolean(string="Product Based Calculation",compute="_compute_product_based")
    model_id = fields.Integer("Model ID")
    temperature = fields.Float("Temperature")
    instrument = fields.Char("Instrument")
    sop = fields.Html(string='SOP',compute="comput_sop")
    
    
    @api.depends("material")
    def comput_sop(self):
        for rec in self:
            rec.sop = rec.material.sop



    def get_product_base_calc_line(self,data):
        line = self.env["lerm.product.based.calculation"].search([('product_id','=',data["material_id"]),('grade','=',data["grade_id"])])
        return line


    def open_product_based_form(self):
        model_record = self.material.product_based_calculation.filtered(lambda r: r.grade.id == self.grade_id.id)
        model = model_record.ir_model.model

        print("material ",self.material.product_based_calculation)
        print("model ",model)

        if self.model_id != 0:
            # import wdb; wdb.set_trace()
            return {
                'view_mode': 'form',
                'res_model': model,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.model_id,
                'context': {
                    'default_srf_id':self.srf_id.id,
                    'default_sample_id': self.sample_id.id,
                    'default_eln_ref':self.id
                 }
            }
        
        else:
            # import wdb; wdb.set_trace()
            return {
                'view_mode': 'form',
                'res_model': model,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {
                    'default_srf_id':self.srf_id.id,
                    'default_sample_id': self.sample_id.id,
                    'default_eln_ref':self.id
                 }
                }

   


    @api.depends('material')
    def _compute_product_based(self):
        for record in self:
            record.is_product_based_calculation = record.material.is_product_based_calculation
    # def calculate_graphs(self):
    #     import wdb; wdb.set_trace()
    #     x = [1, 2, 3, 4, 5]
    #     y = [1, 4, 9, 16, 25]

    #     # Plot the line chart
    #     plt.plot(x, y)
    #     plt.xlabel('X values')
    #     plt.ylabel('Y values')
    #     plt.title('Line Chart')

    #     # Save the chart as an image file
    #     buffer = io.BytesIO()
    #     plt.savefig(buffer, format='png')
    #     buffer.seek(0)
    #     image_data = buffer.read()
    #     buffer.close()

    #     # Convert the image data to base64 format
    #     encoded_image_data = base64.b64encode(image_data)

    #     # Update the image field with the chart image
    #     self.image = encoded_image_data

    #     # Close the plot to release resources
    #     plt.close()

    def fetch_inputs(self):
        self.write({
            "invisible_fetch_inputs": True
        })

        # parameter = self.env['lerm.parameter.master'].browse(7)  # Replace 'parameter_id' with the actual ID of the parameter
        # dependent_parameters = parameter.fetch_dependent_parameters_recursive(depth=80)  # Fetch up to 3 levels of dependent parameters
        # # import wdb ; wdb.set_trace() 
        # for dependent_parameter in dependent_parameters:
        #     import wdb ; wdb.set_trace() 
        #     print(dependent_parameter.parameter_name)
        # parameters = []

        for record in self.parameters_result:
            parameter = self.env['lerm.parameter.master'].browse(record.parameter.id)
            # import wdb ; wdb.set_trace() 

            for inputs in parameter.dependent_inputs:
                self.write({"parameters_input":[(0,0,{'parameter_result':record.id,"is_parameter_dependent":inputs.is_parameter_dependent,'identifier':inputs.identifier,'inputs':inputs.id,'value':inputs.default})]})
            
            dependent_parameters = parameter.fetch_dependent_parameters_recursive(depth=80)
            for dependent_parameter in dependent_parameters:
                # import wdb ; wdb.set_trace()
                data = self.env["eln.parameters.result"].create({"eln_id":self.id,'parameter':dependent_parameter.id})
                # data = self.write({"parameters_result":[(0,0,{'parameter':dependent_parameter.id})]})
                for inputs in dependent_parameter.dependent_inputs:
                    # import wdb ; wdb.set_trace() 
                    self.write({"parameters_input":[(0,0,{'parameter_result':data.id,"is_parameter_dependent":inputs.is_parameter_dependent,'identifier':inputs.identifier,'inputs':inputs.id,'value':inputs.default})]})



            # dependent_parameters = parameter.fetch_dependent_parameters_recursive(depth=80)

            # for inputs in record.parameter.dependent_inputs:
                
            #     self.write({"parameters_input":[(0,0,{'parameter_result':record.id,'identifier':inputs.identifier,'inputs':inputs.id})]})
            #     if inputs.is_parameter_dependent:

            #         # data = self.write({"parameters_result":[(0,0,{'parameter':inputs.parameter.id})]})
            #         data = self.env["eln.parameters.result"].create({"eln_id":self.id,'parameter':inputs.parameter.id})
            #         import wdb ; wdb.set_trace()
            #         for inputs in data.parameter.dependent_inputs: 
            #             self.write({"parameters_input":[(0,0,{'parameter_result':data.id,'identifier':inputs.identifier,'inputs':inputs.id})]})

            #         self.env.cr.commit()

    def calculate_results(self):
        for record in self.parameters_result:
            inputs = self.env["eln.parameters.inputs"].search([("parameter_result","=",record.id)])
            values = {
                        'datetime':datetime
                    }
            for input in inputs:
                values[input.identifier] = input.value
            result = safe_eval(record.parameter.formula, values)
            record.write({'result':result})
            print(result) 



    def confirm_eln(self):
        self.sample_id.write({'state':'3-pending_verification'})
        # import wdb;wdb.set_trace();
        self.sample_id.parameters_result.unlink()
        for result in self.parameters_result:
            if not result.calculated:
                raise ValidationError("Not all parameters are calculated. Please ensure all parameters are calculated before proceeding.")

        for result in self.parameters_result:
            self.env["sample.parameters.result"].create({
                'sample_id':self.sample_id.id,
                'parameter': result.parameter.id,
                'result': result.result,
                'unit':result.unit.id,
                'specification':result.specification,
                'test_method':result.test_method.id
            })
        self.write({'state': '2-confirm'})

    # parameters = fields.One2many('eln_id','eln.parameters',string="Parameters")

 

    def open_result_wizard(self):
        action = self.env.ref('lerm_civil.eln_result_update_wizard')

        parameters = []
        for parameter in self.parameters:
            parameters.append((0,0,{'parameter':parameter.id}))
        
        return {
            'name': "Result Update",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eln.update.result.wizard',
            'view_id': action.id,
            'target': 'new',
            'context': {
                'default_results':parameters
            }
        }
        
    # def print_datasheet(self):
    #     eln = self
    #     template_name = eln.parameters_result.parameter[0].datasheet_report_template.report_name
    #     return {
    #         'type': 'ir.actions.report',
    #         'report_type': 'qweb-pdf',
    #         'report_name': template_name,
    #         'report_file': template_name
    #     }
    def print_datasheet(self):
        eln = self
        is_product_based = eln.is_product_based_calculation
        if is_product_based == True:
            template_name = eln.material.product_based_calculation[0].datasheet_report_template.report_name
        else:
            template_name = eln.parameters_result.parameter[0].datasheet_report_template.report_name
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-html',
            'report_name': template_name,
            'report_file': template_name
        }
    def print_report(self):
        eln = self
        is_product_based = eln.is_product_based_calculation
        if is_product_based == True:
            template_name = eln.material.product_based_calculation[0].main_report_template.report_name
        else:
            template_name = eln.parameters_result.parameter[0].main_report_template.report_name
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-html',
            'report_name': template_name,
            'report_file': template_name
        }
    def print_nabl_report(self):
        eln = self
        is_product_based = eln.is_product_based_calculation
        if is_product_based == True:
            template_name = eln.material.product_based_calculation[0].main_report_template.report_name
        else:
            template_name = eln.parameters_result.parameter[0].main_report_template.report_name
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': template_name,
            'report_file': template_name,
            'data' : {'nabl' : True}
        }
    def print_non_nabl_report(self):
        eln = self
        is_product_based = eln.is_product_based_calculation
        if is_product_based == True:
            template_name = eln.material.product_based_calculation[0].main_report_template.report_name
        else:
            template_name = eln.parameters_result.parameter[0].main_report_template.report_name
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': template_name,
            'report_file': template_name,
            'data' : {'nabl' : False}
        }

    @api.model
    def create(self,vals):
        if vals.get('eln_id', 'New') == 'New':
            vals['eln_id'] = self.env['ir.sequence'].next_by_code('lerm.eln.seq') or 'New'
            res = super(ELN, self).create(vals)
            return res




    @api.onchange('sample_id')
    def compute_kes_no(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).kes_no
                record.kes_no = sample_record
            else:
                record.kes_no = None
    
    @api.onchange('sample_id')
    def compute_discipline(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).discipline_id
                record.discipline = sample_record
            else:
                record.discipline = None

    @api.onchange('sample_id')
    def compute_group(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).group_id
                record.group = sample_record
            else:
                record.group = None
    
    @api.onchange('sample_id')
    def compute_material(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).material_id
                record.material = sample_record
            else:
                record.material = None

    @api.onchange('sample_id')
    def compute_witness(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).witness
                record.witness_name = sample_record
            else:
                record.witness_name = None

    @api.onchange('sample_id')
    def compute_casting_date(self):
        for record in self:
            if record.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.sample_id.id)]).casting_date
                record.casting_date = sample_record
            else:
                record.casting_date = None

    @api.onchange('srf_id')
    def compute_srf_date(self):
        for record in self:
            if record.srf_id:
                srf_record = self.env['lerm.civil.srf'].search([('id','=', record.srf_id.id)]).srf_date
                record.srf_date = srf_record
            else:
                record.srf_date = None

class ParameteResultCalculationWizard(models.TransientModel):
    _name = 'parameter.calculation.wizard'
    parameter = fields.Many2one('lerm.parameter.master',string="Parameter")
    time_based = fields.Boolean("Time Based",compute="compute_is_time")
    inputs_lines = fields.One2many('input.line.wizard', 'wizard_id', string='Inputs')
    nabl_status = fields.Selection([
        ('nabl', 'NABL'),
        ('non-nabl', 'Non-NABL')
    ],compute="compute_nabl_status", string='NABL Status')
    conformity_status = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ],compute="compute_conformity_status",string='Conformity Status')
    result = fields.Float(string="Result",compute="compute_result",digits=(16, 5))
    # result_char = fields.Char(string="Result")

    @api.depends('parameter')
    def compute_is_time(self):
        for rec in self:
            rec.time_based = rec.parameter.time_based

    @api.depends('result')
    def compute_conformity_status(self):
        for record in self:
            # import wdb;wdb.set_trace()
            material_table = self.parameter.parameter_table.filtered(lambda rec: rec.grade.id == self.env.context.get('grade_id') and rec.material.id == self.env.context.get('material_id') and rec.size.id == self.env.context.get('size_id'))
            req_min = material_table.req_min
            req_max = material_table.req_max
            mu_neg = record.result - record.result*record.parameter.mu_value
            print("mu_val")
            print(record.parameter.mu_value)
            print("req_min")
            print(req_min)
            print("req_max")
            print(req_max)
            print("mu_neg")
            print(mu_neg)
            mu_pos = record.result + record.result*record.parameter.mu_value
            print("mu_pos")
            print(mu_pos)
            print("req_min <= mu_neg <= req_max")
            print(req_min <= mu_neg <= req_max)
            print("req_min <= mu_pos <= req_max")
            print(req_min <= mu_pos <= req_max)
        
            if req_min <= mu_neg <= req_max and req_min <= mu_pos <= req_max:
                record.conformity_status = "pass"
            else:
                record.conformity_status = "fail"


    @api.depends('result')
    def compute_nabl_status(self):
        for record in self:
            if record.parameter.lab_min_value <= record.result <= record.parameter.lab_max_value:
                record.nabl_status = 'nabl'
            elif record.parameter.lab_min_value <= record.result and record.parameter.lab_max_value == 0:
                record.nabl_status = 'nabl'
            else:
                record.nabl_status = 'non-nabl'

    

    def update_result(self):
        # import wdb; wdb.set_trace()
        result_id = self.env.context.get('result_id')
        result_id = self.env["eln.parameters.result"].search([('id','=',result_id)])
        self.env["eln.parameters.inputs"].search([('eln_id','=',self.env.context.get('eln_id'))])
        self.env["eln.parameters.inputs"].sudo().search([('eln_id','=',self.env.context.get('eln_id')),('inputs.label','=',self.parameter.parameter_name)]).write({'value':self.result})
        for input in self.inputs_lines:
            # import wdb; wdb.set_trace()
            self.env["eln.parameters.inputs"].search([('eln_id','=',self.env.context.get('eln_id')),('id','=',input.inputs_id.id)]).write({'value':input.value,'date_time':input.date_time})




        result_id.sudo().write({'result':self.result,'calculated':True,'nabl_status':self.nabl_status,'conformity_status':self.conformity_status})

        return {'type': 'ir.actions.act_window_close'}

    # def calculate(self):
    #     values = {}
    #     for input in self.inputs_lines:
    #         values[input.identifier] = input.value
        

    #     result_id = self.env.context.get('result_id')
    #     result_id = self.env["eln.parameters.result"].search([('id','=',result_id)])
    #     result = safe_eval(result_id.parameter.formula, values)
    #     # import wdb; wdb.set_trace()
    #     self.write({'result':result})

    @api.depends('inputs_lines.value')
    def compute_result(self):
        for record in self:
            values = {
                        'datetime':datetime
                                            
                    }
            try:
                for input in self.inputs_lines:
                    if record.time_based:
                        values[input.identifier] = input.date_time
                    else:
                        values[input.identifier] = input.value

                
                result_id = self.env.context.get('result_id')
                result_id = self.env["eln.parameters.result"].search([('id','=',result_id)])
                result = safe_eval(result_id.parameter.formula, values)
                if record.time_based:
                    record.result = result.total_seconds() / 60
                else:
                    record.result = result
            except:
                record.result = 0
                pass

        # print(input)


class InputLines(models.TransientModel):
    _name = 'input.line.wizard'
    wizard_id = fields.Many2one('parameter.calculation.wizard', string='Wizard')
    inputs_id = fields.Many2one('eln.parameters.inputs', string='Inputs ID')
    parameter_result = fields.Many2one('eln.parameters.result',string="Parameter")
    is_parameter_dependent = fields.Boolean("Parameter Dependent")
    identifier = fields.Char(string="Identifier")
    inputs = fields.Many2one('lerm.dependent.inputs',string="Inputs")
    value = fields.Float(string="Value",digits=(12, 5))
    date_time = fields.Datetime("Time") 
    
    @api.onchange('value')
    def _onchange_value(self):
        decimal_digits_limit = self.inputs.decimal_place

        for record in self:
            decimal_part = str(record.value).split('.')[1] if '.' in str(record.value) else ''
            if len(decimal_part) > decimal_digits_limit:
                raise ValidationError("Number of digits after decimal should not exceed %s." % decimal_digits_limit)




  
                


class ELNSpreadsheet(models.Model):
    _name = 'eln.spreadsheets'
    _rec_name = 'datasheet'
    eln_id = fields.Many2one('lerm.eln',string="ELN ID")
    datasheet = fields.Many2one('documents.document',string="Datasheet")
    spreadsheet_template = fields.Many2one("spreadsheet.template",string="Spreadsheet Template")
    related_parameters = fields.Many2many("eln.parameters",string="Related Parameters")
    fill_datasheet = fields.Integer("Fill Spreadsheet")


class ELNParametersResult(models.Model):
    _name = 'eln.parameters.result'
    _rec_name = 'parameter'
    eln_id = fields.Many2one('lerm.eln',string="ELN ID")
    parameter = fields.Many2one('lerm.parameter.master',string="Parameter")
    unit = fields.Many2one('uom.uom',string="Unit")
    context_data = fields.Text("Context Data")
    calculated = fields.Boolean("Calculated")
    calculation_type = fields.Selection([('parameter_based', 'Parameter Based'), ('form_based', 'Form Based')],compute='_compute_calculation_type',string='Calculation Type')
    test_method = fields.Many2one('lerm_civil.test_method',string="Specification")
    specification_permissible_limit = fields.Text(string="Specification",compute='_compute_specification')
    specification = fields.Text(string="Test Method", compute='_compute_specification')
    nabl_status = fields.Selection([
        ('nabl', 'NABL'),
        ('non-nabl', 'Non-NABL')

    ], string='NABL Status')
    conformity_status = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')
    ],string='Conformity Status')
    model_id = fields.Integer(string="Model Id")
    result = fields.Float(string="Result",digits=(16,5))


    # @api.depends('result')
    # def compute_nabl_status(self):
    #     for record in self:
    #         if record.parameter.lab_min_value <= record.result <= record.parameter.lab_max_value:
    #             record.nabl_status = 'nabl'
    #         elif record.parameter.lab_min_value <= record.result and record.parameter.lab_max_value == 0:
    #             record.nabl_status = 'nabl'
    #         else:
    #             record.nabl_status = 'non-nabl'

    @api.depends('parameter.calculation_type')
    def _compute_calculation_type(self):
        for record in self:
            record.calculation_type = record.parameter.calculation_type


    @api.depends('eln_id.material', 'eln_id.grade_id', 'eln_id.size_id','parameter')
    def _compute_specification(self):
        for record in self:
            # import wdb; wdb.set_trace()
            material_id = record.eln_id.material.id
            grade_id = record.eln_id.grade_id.id
            size_id = record.eln_id.size_id.id
            parameter_id = record.parameter.id
            specification = self.env['lerm.parameter.master.table'].search([('material','=',material_id),('size','=',size_id),('grade','=',grade_id),('parameter_id','=',parameter_id)]).specification
            print("specsi")
            print(specification)
            table_record = self.env['lerm.parameter.master.table'].search([('material','=',material_id),('size','=',size_id),('grade','=',grade_id),('parameter_id','=',parameter_id)])
            record.specification = specification
            record.specification_permissible_limit = table_record.permissable_limit

    def open_form(self):
        # import wdb; wdb.set_trace()
        if self.model_id != 0:
            return {
                'view_mode': 'form',
                'res_model': self.parameter.ir_model.model,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': self.model_id,
                'context': {
                    'default_srf_id':self.eln_id.srf_id.id,
                    'default_sample_id': self.eln_id.sample_id.id,
                    'default_parameter_id':self.id,
                    'default_eln_ref':self.eln_id.id
                 }
            }
        else:
            return {
                'view_mode': 'form',
                'res_model': self.parameter.ir_model.model,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {
                    'default_srf_id':self.eln_id.srf_id.id,
                    'default_sample_id': self.eln_id.sample_id.id,
                    'default_parameter_id':self.id,
                    'default_eln_ref':self.eln_id.id

                 }
                }



    def open_calculation_wizard(self):
        # wizard = self.env['parameter.calculation.wizard'].create({})
        action = self.env.ref('lerm_civil.parameter_calculation_wizard')

        inputs =self.env["eln.parameters.inputs"].search([("eln_id","=",self.eln_id.id),("parameter_result","=",self.id)])
        parameters_inputs=[]
        for input in inputs:
            # import wdb; wdb.set_trace()
            parameters_input = (0,0,{'inputs_id':input.id,'parameter_result':input.parameter_result.id,"is_parameter_dependent":input.is_parameter_dependent,'identifier':input.identifier,'inputs':input.inputs.id,'value':input.value})
            parameters_inputs.append(parameters_input)
        # import wdb; wdb.set_trace()


        return {
            'name': "Calculation",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'parameter.calculation.wizard',
            'view_id': action.id,
            'target': 'new',
            'context':{
                'default_parameter':self.parameter.id,
                'default_inputs_lines': parameters_inputs,
                'material_id':self.eln_id.material.id,
                'size_id':self.eln_id.size_id.id,
                'grade_id':self.eln_id.grade_id.id,
                'result_id':self.id,
                'eln_id':self.eln_id.id
            }
            }


    

class ELNParametersInputs(models.Model):
    _name = 'eln.parameters.inputs'
    eln_id = fields.Many2one('lerm.eln',string="ELN ID")
    parameter_result = fields.Many2one('eln.parameters.result',string="Parameter")
    is_parameter_dependent = fields.Boolean("Parameter Dependent")
    identifier = fields.Char(string="Identifier")
    inputs = fields.Many2one('lerm.dependent.inputs',string="Inputs")
    value = fields.Float(string="Value",digits=(12, 5))
    date_time = fields.Datetime("Time") 






class ELNParameters(models.Model):
    _name = 'eln.parameters'
    _rec_name = 'parameter'
    eln_id = fields.Many2one('lerm.eln',string="ELN ID")
    parameter = fields.Many2one('lerm.parameter.master',string="Parameter")
    specification = fields.Text(string="Specification")
    test_method = fields.Many2one('lerm_civil.test_method',compute="compute_method",string="Test Method")
    datasheet = fields.Many2one('documents.document',string="Datasheet")
    result = fields.Float(string="Result")
    button = fields.Float(string="Button")
    result_json = fields.Text(string="Result JSON")
    spreadsheet_template = fields.Many2one("spreadsheet.template",string="Spreadsheet Template")
    set_result_button = fields.Float(string="Button")


    def set_result(self):
        binary_data = base64.b64decode(self.datasheet.datas)
        json_data = json.loads(binary_data.decode('utf-8'))
        print(json_data)
        # sheet_name = self.parameter.sheets
        # cell = self.parameter.cell
        # filtered_sheet = next((sheet for sheet in json_data["sheets"] if sheet["name"] == sheet_name), None)
        # if filtered_sheet:
        #     print(filtered_sheet)

        
    @api.depends('parameter')
    def compute_method(self):
        for record in self:
            record.test_method = record.parameter.test_method.id

    

class UpdateResult(models.TransientModel):
    _name = 'eln.update.result.wizard'

    results = fields.One2many('eln.result.child','wizard_id',string="Parameters")



    def update_result(self):
        print("working")



class UpdateResultChild(models.TransientModel):
    _name ="eln.result.child"
    wizard_id = fields.Many2one('eln.update.result.wizard')
    parameter = fields.Many2one('eln.parameters',string="Parameter")
    result = fields.Float(string="Result")


