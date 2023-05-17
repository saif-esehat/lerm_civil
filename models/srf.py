from odoo import api, fields, models
from odoo.exceptions import UserError

class Discipline(models.Model):
    _name = "lerm_civil.discipline"
    _description = "Lerm Discipline"
    _rec_name = 'discipline'

    discipline = fields.Char(string="Discipline", required=True)
    hod = fields.Many2one('res.users',string="Head of Department")

    def __str__(self):
        return self.discipline

class Group(models.Model):
    _name = "lerm_civil.group"
    _description = "Lerm Group"
    _rec_name = 'group'

    discipline = fields.Many2one('lerm_civil.discipline', string="Discipline", required=True)
    group = fields.Char(string="Group", required=True)


    def __str__(self):
        return self.group
    

class TestMethod(models.Model):
    _name = "lerm_civil.test_method"
    _description = "Lerm Test Method"
    _rec_name = 'test_method'

    test_method = fields.Char(string="Test Method", required=True)


    def __str__(self):
        return self.test_method


class SrfForm(models.Model):
    _name = "lerm.civil.srf"
    _description = "SRF"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'srf_id'

    srf_id = fields.Char(string="SRF ID")
    # job_no = fields.Char(string="Job NO.")
    srf_date = fields.Date(string="SRF Date")
    job_date = fields.Date(string="JOB Date")
    customer = fields.Many2one('res.partner',string="Customer")
    billing_customer = fields.Many2one('res.partner',string="Billing Customer")
    contact_person = fields.Many2one('res.partner',string="Contact Person")
    site_address = fields.Many2one('res.partner',string="Site Address")
    name_work = fields.Char(string="Name of Work")
    client_refrence = fields.Char(string="Client Reference Letter")
    samples = fields.One2many('lerm.srf.sample' , 'srf_id' , string="Samples")
    contact_other_ids = fields.Many2many('res.partner',string="Other Ids",compute="compute_other_ids")
    contact_contact_ids = fields.Many2many('res.partner',string="Contact Ids",compute="compute_contact_ids")
    contact_site_ids = fields.Many2many('res.partner',string="Site Ids",compute="compute_site_ids")
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")
    state = fields.Selection([
        ('1-draft', 'Draft'),
        ('2-confirm', 'Confirm')
    ], string='State', default='1-draft')


    def confirm_srf(self):
        
        for record in self.samples:
            # if vals.get('sample_no', 'New') == 'New' and vals.get('kes_no', 'New') == 'New':
            sample_id = self.env['ir.sequence'].next_by_code('lerm.srf.sample') or 'New'
            kes_no = self.env['ir.sequence'].next_by_code('lerm.srf.sample.kes') or 'New'
            # res = super(LermSampleForm, self).create(vals)
            #     return res
            record.write({'status':'2-confirmed','sample_no':sample_id,'kes_no':kes_no})
        
        self.write({'state': '2-confirm'})
        # for record in self:

    # name_of_work = fields.Many2one('res.partner.project',string='Name of Work')

    @api.depends('customer')
    def compute_contact_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','contact')])
            record.contact_contact_ids = contact_ids

    @api.depends('customer')
    def compute_other_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','other')])
            record.contact_other_ids = contact_ids

    @api.depends('customer')
    def compute_site_ids(self):
        for record in self:
            contact_ids = self.env['res.partner'].search([('parent_id', '=', record.customer.id),('type','=','delivery')])
            record.contact_site_ids = contact_ids
    
    def open_sample_add_wizard(self):

        samples = self.env["lerm.srf.sample"].search([("srf_id","=",self.id)])
        # print("Samples "+ str(samples))


        action = self.env.ref('lerm_civil.srf_sample_wizard_form')
        if len(samples) > 0:
            print(samples[0].material_id.id , 'error')
            material_id = samples[0].material_id.id
            group_id = samples[0].group_id.id
            alias = samples[0].alias
            brand = samples[0].brand
            size_id = samples[0].size_id.id
            grade_id = samples[0].grade_id.id
            sample_received_date = samples[0].sample_received_date
            location = samples[0].location
            sample_condition = samples[0].sample_condition
            sample_reject_reason = samples[0].sample_reject_reason
            witness = samples[0].witness
            scope = samples[0].scope
            sample_description = samples[0].sample_description

            return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.srf.sample.wizard',
            'view_id': action.id,
            'target': 'new',
            'context': {
            'default_material_id' : material_id,
            'default_alias':alias,
            'default_brand':brand,
            'default_size_id':size_id,
            'default_grade_id':grade_id,
            'default_sample_received_date': sample_received_date,
            'default_location':location,
            'default_sample_condition':sample_condition,
            'default_sample_reject_reason':sample_reject_reason,
            'default_witness':witness,
            'default_scope':scope,
            'default_sample_description':sample_description,
            'default_group_id':group_id

            }
            }
        else:
            return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.srf.sample.wizard',
            'view_id': action.id,
            'target': 'new'
            }


class LermSampleForm(models.Model):
    _name = "lerm.srf.sample"
    _description = "Sample"
    _rec_name = 'sample_no'
    srf_id = fields.Many2one('lerm.civil.srf' , string="Srf Id" )
    sample_no = fields.Char(string="Sample ID." ,required=True,readonly=True, default=lambda self: 'New')
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    qty_id = fields.Many2one('lerm.qty.line',string="Quantity")
    sample_quantity = fields.Integer(string="Sample Quantity")
    received_by_id = fields.Many2one('res.partner',string="Received By")
    sample_received_date = fields.Date(string="Sample Received Date")
    sample_condition = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non_satisfactory', 'Non-Satisfactory'),
    ], string='Sample Condition', default='satisfactory')
    location = fields.Char(string="Location")
    sample_reject_reason = fields.Char(string="Sample Reject Reason")
    witness = fields.Char(string="Witness")
    scope = fields.Selection([
        ('nabl', 'NABL'),
        ('non_nabl', 'Non-NABL'),
    ], string='Scope', default='nabl')
    sample_description = fields.Text(string="Sample Description")
    group_ids = fields.Many2many('lerm_civil.group',string="Group Ids",compute="compute_group_ids")
    material_ids = fields.Many2many('product.template',string="Material Ids",compute="compute_material_ids")
    size_ids = fields.Many2many('lerm.size.line',string="Size Ids",compute="compute_size_ids")
    grade_ids = fields.Many2many('lerm.grade.line',string="Grade Ids",compute="compute_grade_ids")
    qty_ids = fields.Many2many('lerm.qty.line',string="Qty Ids",compute="compute_qty_ids")
    days_casting = fields.Selection([
        ('3', '3 Days'),
        ('7', '7 Days'),
        ('14', '14 Days'),
        ('28', '28 Days'),
    ], string='Days of casting', default='3')
    customer_id = fields.Many2one('res.partner' , string="Customer")
    alias = fields.Char(stirng="Alias")
    parameters = fields.Many2many('lerm.parameter.master',stirng="Parameter")
    # parameters_ids = fields.Many2many('lerm.datasheet.line',string="Parameter" , compute="compute_param_ids")
    kes_no = fields.Char("KES No",required=True,readonly=True, default=lambda self: 'New')
    casting_date = fields.Date(string="Casting Date")
    
    status = fields.Selection([
        ('1-pending', 'Pending'),
        ('2-confirmed', 'Confirmed'),
    ], string='Status', default='1-pending')

    state = fields.Selection([
        ('1-allotment_pending', 'Allotment Pending'),
        ('2-alloted', 'Alloted'),
        ('3-in_report', 'In-Report'),
    ], string='State',default='1-allotment_pending')

    def open_sample_allotment_wizard(self):
        action = self.env.ref('lerm_civil.srf_sample_allotment_wizard')

        return {
            'name': "Add Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sample.allotment.wizard',
            'view_id': action.id,
            'target': 'new'
            }
        

    # @api.model
    # def create(self, vals):
    #     if vals.get('sample_no', 'New') == 'New' and vals.get('kes_no', 'New') == 'New':
    #         vals['sample_no'] = self.env['ir.sequence'].next_by_code('lerm.srf.sample') or 'New'
    #         vals['kes_no'] = self.env['ir.sequence'].next_by_code('lerm.srf.sample.kes') or 'New'
    #         res = super(LermSampleForm, self).create(vals)
    #         return res


    # @api.depends('material_id')
    # def compute_param_ids(self):
    #     for record in self:
    #         parameters_ids = self.env['lerm.datasheet.line'].search([('datasheet_id','=', record.material_id.data_sheet_format_no.id)])
    #         print("sas",parameters_ids)
    #         record.parameters_ids = parameters_ids
                

    @api.onchange('material_id.casting_required','material_id')
    def onchange_material_id(self):
        for record in self:
            if record.material_id.casting_required:
                record.casting = True
            else:
                record.casting = False

    @api.onchange('material_id.alias' ,'customer_id', 'material_id')
    def onchange_material_id(self):
        for record in self:
            result = self.env['lerm.alias.line'].search([('customer', '=', record.customer_id.id),('product_id', '=', record.material_id.id)])
            record.alias = result.alias


    
    @api.depends('discipline_id')
    def compute_group_ids(self):
        for record in self:
            group_ids = self.env['lerm_civil.group'].search([('discipline','=', record.discipline_id.id)])
            record.group_ids = group_ids

    @api.depends('discipline_id' , 'group_id')
    def compute_material_ids(self):
        for record in self:
            if record.discipline_id and record.group_id:
                material_ids = self.env['product.template'].search([('discipline','=', record.discipline_id.id) , ('group','=', record.group_id.id)])
                record.material_ids = material_ids
            else:
                record.material_ids = None

    @api.depends('material_id')
    def compute_size_ids(self):
        for record in self:
            if record.material_id:
                size_ids = self.env['lerm.size.line'].search([('product_id','=', record.material_id.id)])
                record.size_ids = size_ids
            else:
                record.size_ids = None

    @api.depends('material_id')
    def compute_grade_ids(self):
        for record in self:
            if record.material_id:
                grade_ids = self.env['lerm.grade.line'].search([('product_id','=', record.material_id.id)])
                record.grade_ids = grade_ids
            else:
                record.grade_ids = None

    @api.depends('material_id')
    def compute_qty_ids(self):
        for record in self:
            if record.material_id:
                qty_ids = self.env['lerm.qty.line'].search([('product_id','=', record.material_id.id)])
                record.qty_ids = qty_ids
            else:
                record.qty_ids = None
    


class SampleParameter(models.Model):
    _name = "lerm.srf.sample.parameter"
    _description = "Sample Parameter"
    sample_id = fields.Many2one('',string="Sample Id")
    product_id = fields.Many2one('product.template' , string="Product Id")
    paramter = fields.Many2one('lerm.parameter.master' , string="Parameter")



class CreateSampleWizard(models.TransientModel):
    _name = 'create.srf.sample.wizard'
    
    srf_id = fields.Many2one('lerm.civil.srf' , string="Srf Id")
    sample_id = fields.Char(string="Sample Id")
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    # qty_id = fields.Many2one('lerm.qty.line',string="Quantity")
    qty_id = fields.Integer(string="Sample Quantity")
    # sample_qty_id = fields.Integer(string="Sample Quantity")
    received_by_id = fields.Many2one('res.partner',string="Received By")
    sample_received_date = fields.Date(string="Sample Received Date")
    sample_condition = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non_satisfactory', 'Non-Satisfactory'),
    ], string='Sample Condition', default='satisfactory')
    location = fields.Char(string="Location")
    sample_reject_reason = fields.Char(string="Sample Reject Reason")
    witness = fields.Char(string="Witness")
    scope = fields.Selection([
        ('nabl', 'NABL'),
        ('non_nabl', 'Non-NABL'),
    ], string='Scope', default='nabl')
    sample_description = fields.Text(string="Sample Description")
    # group_ids = fields.Many2many('lerm_civil.group',string="Group Ids")
    # material_ids = fields.Many2many('product.template',string="Material Ids")
    # size_ids = fields.Many2many('lerm.size.line',string="Size Ids")
    # grade_ids = fields.Many2many('lerm.grade.line',string="Grade Ids")
    # qty_ids = fields.Many2many('lerm.qty.line',string="Qty Ids")
    days_casting = fields.Selection([
        ('3', '3 Days'),
        ('7', '7 Days'),
        ('14', '14 Days'),
        ('28', '28 Days'),
    ], string='Days of casting', default='3')
    customer_id = fields.Many2one('res.partner' , string="Customer")
    alias = fields.Char(stirng="Alias")
    parameters = fields.Many2many('lerm.parameter.master',string="Parameter")


    @api.onchange('material_id')
    def compute_parameters(self):
        for record in self:
            if record.material_id:
                product_record = self.env['product.template'].search([('id','=', record.material_id.id)]).parameter_table1
                record.parameters = product_record
            else:
                record.parameters = None

   

    def add_sample(self):
        group_id =  self.group_id.id
        alias = self.alias
        material_id = self.material_id.id
        size_id = self.size_id.id
        brand = self.brand
        grade_id = self.grade_id.id
        sample_received_date = self.sample_received_date
        location = self.location
        sample_condition = self.sample_condition
        sample_reject_reason = self.sample_reject_reason
        witness = self.witness
        scope = self.scope
        sample_description =self.sample_condition
        parameters = self.parameters

        if self.qty_id > 0:

            for i in range(self.qty_id):
                self.env["lerm.srf.sample"].create({
                    'srf_id': self.env.context.get('active_id'),
                    'group_id':group_id,
                    'alias':alias,
                    'material_id' : self.material_id.id,
                    'size_id':size_id,
                    'brand':brand,
                    'grade_id':grade_id,
                    'sample_received_date':sample_received_date,
                    'location':location,
                    'sample_condition':sample_condition,
                    'sample_reject_reason':sample_reject_reason,
                    'witness':witness,
                    'scope':scope,
                    'sample_description':sample_description,
                    'parameters':parameters
                })        

            print("Parameters "+ str(self.parameters))

            return {'type': 'ir.actions.act_window_close'}
        else:
            raise UserError("Sample Quantity Must be Greater Than Zero")

    def close_sample_wizard(self):
        return {'type': 'ir.actions.act_window_close'}


    
    class AllotSampleWizard(models.TransientModel):
        _name = "sample.allotment.wizard"

        technicians = fields.Many2one("res.users",string="Technicians")


