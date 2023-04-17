from odoo import api, fields, models

class Discipline(models.Model):
    _name = "lerm_civil.discipline"
    _description = "Lerm Discipline"
    _rec_name = 'discipline'

    discipline = fields.Char(string="Discipline", required=True)

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

    srf_no = fields.Char(string="SRF No.")
    job_no = fields.Char(string="Job NO.")
    srf_date = fields.Date(string="SRF Date")
    job_date = fields.Date(string="JOB Date")
    customer = fields.Many2one('res.partner',string="Customer")
    billing_customer = fields.Many2one('res.partner',string="Billing Customer")
    contact_person = fields.Many2one('res.partner',string="Contact Person")
    site_address = fields.Many2one('res.partner',string="Site Address")
    name_work = fields.Char(string="Name of Work")
    client_refrence = fields.Char(string="Client Reference")
    samples = fields.One2many('lerm.srf.sample' , 'srf_id' , string="Samples")


class LermSampleForm(models.Model):
    _name = "lerm.srf.sample"
    _description = "Sample"
    srf_id = fields.Many2one('lerm.civil.srf' , string="Srf Id")
    sample_no = fields.Char(string="Sample No.")
    casting = fields.Boolean(string="Casting")
    discipline_id = fields.Many2one('lerm_civil.discipline',string="Discipline")
    group_id = fields.Many2one('lerm_civil.group',string="Group")
    material_id = fields.Many2one('product.template',string="Material")
    brand = fields.Char(string="Brand")
    size_id = fields.Many2one('lerm.size.line',string="Size")
    grade_id = fields.Many2one('lerm.qty.line',string="Grade")
    sample_qty_id = fields.Many2one('lerm.qty.line',string="Sample Quantity")
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



