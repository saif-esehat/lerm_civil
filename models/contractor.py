from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError

class LermContractor(models.Model):
    _inherit = "res.partner"

    contractor_table = fields.One2many('lerm.contractor.line','partner_id',string="Contractor")


class ContractorLine(models.Model):
    _name = 'lerm.contractor.line'

    partner_id = fields.Many2one('res.partner')
    name = fields.Char(string='Contractor Name')