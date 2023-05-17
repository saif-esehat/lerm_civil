from odoo import api, fields, models

class ELN(models.Model):
    _name = 'lerm.eln'

    srf_id = fields.Many2one('lerm.civil.srf',string="SRF ID")
    sample_id = fields.Many2one('lerm.srf.sample',string='Sample ID')
    srf_date = fields.Date(string='SRF Date')
    kes_no = fields.Char(string="KES NO")
    discipline = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group = fields.Many2one('lerm_civil.group',string="Group")
    material = fields.Many2one('product.template',string='Material')
    witness_name = fields.Char(string="Witness Name")
    casting_date = fields.Date(string="Casting Date")
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")

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