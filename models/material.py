from odoo import api, fields, models

class Material(models.Model):
    _name = "lerm.civil.material"
    _description = "Material"
    _rec_name = 'material'

    group = fields.Many2one('lerm_civil.group',string="Group", required=True)
    material = fields.Char(string="Material", required=True)

    def __str__(self):
        return self.material