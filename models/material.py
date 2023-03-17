from odoo import api, fields, models

class Material(models.Model):
    _name = "lerm.civil.material"
    _description = "Material"
    _rec_name = 'material'

    group = fields.Many2one('lerm_civil.group',string="Group")
    material = fields.Char(string="Material")

    def __str__(self):
        return self.material