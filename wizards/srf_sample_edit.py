from odoo import api, fields, models,_
from odoo.exceptions import UserError
import logging



class SRFSampleEditWizard(models.TransientModel):
    _name = "edit.lerm.civil.srf.sample"
    _description = 'Edit SRF Sample Wizard'

    srf_id = fields.Many2one('lerm.civil.srf' , string="Srf Id")
    sample_id = fields.Char(string="Sample Id")
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
   
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    size_ids = fields.Many2many('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.grade.line',string="Grade")
    
    grade_ids = fields.Many2many('lerm.grade.line',string="Grades")
    grade_required = fields.Boolean(string="Grade Required",compute="compute_grade_required")

    sample_qty = fields.Integer(string="Sample Quantity",default=1)
    received_by_id = fields.Many2one('res.users',string="Received By",default=lambda self: self.env.user)
    sample_received_date = fields.Date(string="Sample Received Date")
    sample_condition = fields.Selection([
        ('satisfactory', 'Satisfactory'),
        ('non_satisfactory', 'Non-Satisfactory'),
    ], string='Sample Condition', default='satisfactory')
    location = fields.Char(string="Location")
    sample_reject_reason = fields.Char(string="Sample Reject Reason")
    has_witness = fields.Boolean(string="Witness")
    witness = fields.Char(string="Witness name")
    scope = fields.Selection([
        ('nabl', 'NABL'),
        ('non_nabl', 'Non-NABL'),
    ], string='Scope', default='nabl')
    sample_description = fields.Text(string="Sample Description")
    group_ids = fields.Many2many('lerm_civil.group',string="Group Ids")
    material_ids = fields.Many2many('product.template',string="Material Ids")
    client_sample_id = fields.Char(string="Client Sample Id")
    days_casting = fields.Selection([
        ('3', '3 Days'),
        ('7', '7 Days'),
        ('14', '14 Days'),
        ('28', '28 Days'),
    ], string='Days of casting', default='3')
    date_casting = fields.Date(string="Date of Casting")
    customer_id = fields.Many2one('res.partner' , string="Customer")
    product_aliases = fields.Many2many('product.product',string="Product Aliases")
    product_alias = fields.Many2one('product.product',string="Product Alias")
    parameters = fields.Many2many('lerm.parameter.master',string="Parameter")
    conformity = fields.Boolean(string="Conformity Requested")
    volume = fields.Char(string="Volume")
    product_name = fields.Many2one('product.template',string="Product Name")
    pricelist = fields.Many2one('product.pricelist',string='Pricelist')
    main_name = fields.Char(string="Product Name",compute='compute_main_name',store=True)
    price = fields.Float(string="Price",compute='compute_price',store=True)
    
    
    def edit_sample(self):
        
        self.id.write({
            'discipline_id': self.discipline_id.id,
            'group_id': self.group_id.id,
            'material_id': self.material_id.id,
            'brand': self.brand,
            'size_id': self.size_id.id,
            'grade_id': self.grade_id.id,
            'sample_qty': self.sample_qty,
            'received_by_id': self.received_by_id.id,
            'sample_received_date':self.sample_received_date,
            'sample_condition':self.sample_condition,

            'sample_reject_reason': self.sample_reject_reason,
            'location': self.location,
            'received_by_id': self.received_by_id.id,
            'sample_received_date':self.sample_received_date,

            'witness':self.witness,
            'scope':self.scope,
            'sample_description':self.sample_description,
            'client_sample_id':self.client_sample_id,
            'days_casting':self.days_casting,

            'date_casting':self.date_casting,
            'customer_id':self.customer_id.id,
            'product_aliases':self.product_aliases.ids,

            'product_alias':self.product_alias.id,
            'conformity':self.conformity,
            'product_name':self.product_name.id,
            'pricelist':self.pricelist.id,
            'main_name':self.main_name,
            'price':self.price,




        })