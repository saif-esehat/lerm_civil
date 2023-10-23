from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class MechanicalAdmixture(models.Model):
    _name = 'mechanical.admixture'
    _inherit = "lerm.eln"
    _rec_name = "name"


    name_admixture = fields.Char("Name",default="Admixture")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")
    
