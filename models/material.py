from odoo import api, fields, models

class Material(models.Model):
    _inherit = "res.partner"
    _description = "Material"

    group = fields.Many2one('lerm_civil.group',string="Group", required=True)
    material = fields.Char(string="Material", required=True)

    def __str__(self):
        return self.material