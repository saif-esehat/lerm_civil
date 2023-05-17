from odoo import api, fields, models

class ELN(models.Model):
    _name = 'lerm.eln'

    srf_id = fields.Many2one('lerm.civil.srf',string="SRF ID")
    sample_id = fields.Many2one('lerm.srf.sample',string='Sample ID')