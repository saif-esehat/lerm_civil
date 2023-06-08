from odoo import api, fields, models
import base64
import json

class ELN(models.Model):
    _name = 'lerm.eln'
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
    update_result = fields.Integer("Update Result")
    state = fields.Selection([
        ('1-draft', 'Draft'),
        ('2-confirm', 'Confirm'),
    ], string='State',default='1-draft')

    def confirm_eln(self):
        self.sample_id.write({'state':'3-in_report'})
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


class ELNSpreadsheet(models.Model):
    _name = 'eln.spreadsheets'
    _rec_name = 'datasheet'
    eln_id = fields.Many2one('lerm.eln',string="ELN ID")
    datasheet = fields.Many2one('documents.document',string="Datasheet")
    spreadsheet_template = fields.Many2one("spreadsheet.template",string="Spreadsheet Template")
    related_parameters = fields.Many2many("eln.parameters",string="Related Parameters")
    fill_datasheet = fields.Integer("Fill Spreadsheet")


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


