from odoo import api, fields, models
from odoo.exceptions import UserError

class LermSampleForm(models.Model):
    _name = "lerm.srf.sample"
    _inherit = ['mail.thread','mail.activity.mixin']

    _description = "Sample"
    _rec_name = 'sample_no'
    
    srf_id = fields.Many2one('lerm.civil.srf' , string="SRF ID" )
    sample_range_id = fields.Many2one('sample.range.line',string="Sample Range")
    sample_no = fields.Char(string="Sample ID." ,required=True,readonly=True, default=lambda self: 'New')
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    # qty_id = fields.Many2one('lerm.qty.line',string="Quantity")
    sample_qty = fields.Integer(string="Sample Quantity")
    received_by_id = fields.Many2one('res.partner',string="Received By")
    sample_received_date = fields.Date(string="Sample Received Date")
    sample_condition = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non_satisfactory', 'Non-Satisfactory'),
    ], string='Sample Condition', default='satisfactory')
    technicians = fields.Many2one("res.users",string="Technicians")
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
    alias = fields.Char(string="Alias")
    parameters = fields.Many2many('lerm.parameter.master',string="Parameter")
    # parameters_ids = fields.Many2many('lerm.datasheet.line',string="Parameter" , compute="compute_param_ids")
    kes_no = fields.Char("KES No",required=True,readonly=True, default=lambda self: 'New')
    casting_date = fields.Date(string="Casting Date")
    client_sample_id = fields.Char(string='Client Sample ID')
    
    status = fields.Selection([
        ('1-pending', 'Pending'),
        ('2-confirmed', 'Confirmed'),
    ], string='Status', default='1-pending')

    state = fields.Selection([
        ('1-allotment_pending', 'Assignment Pending'),
        ('2-alloted', 'Alloted'),
        ('3-in_report', 'In-Report'),
    ], string='State',default='1-allotment_pending')


    @api.onchange('material_id')
    def compute_parameters(self):
        for record in self:
            if record.material_id:
                parameters_ids = []
                product_records = self.env['product.template'].search([('id','=', record.material_id.id)]).parameter_table1
                for rec in product_records:
                    parameters_ids.append(rec.id)
                domain = {'parameters': [('id', 'in', parameters_ids)]}
                return {'domain': domain}
            else:
                domain = {'parameters': [('id', 'in', [])]}
                return {'domain': domain}

    # def open_bulk_allotment_wizard(self):
    #     print("Workign")

    def open_sample_allotment_wizard(self):
        action = self.env.ref('lerm_civil.srf_sample_allotment_wizard')
        return {
            'name': "Allot Sample",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sample.allotment.wizard',
            'view_id': action.id,
            'target': 'new'
            }
    

    @api.model
    def create(self, vals):
        if vals.get('sample_no', 'New') == 'New' and vals.get('kes_no', 'New') == 'New':
            vals['sample_no'] = self.env['ir.sequence'].next_by_code('lerm.srf.sample') or 'New'
            vals['kes_no'] = self.env['ir.sequence'].next_by_code('lerm.srf.sample.kes') or 'New'
            res = super(LermSampleForm, self).create(vals)
            return res


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