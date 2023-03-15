from odoo import api, fields, models

class Discipline(models.Model):
    _name = "lerm_civil.discipline"
    _description = "Lerm Discipline"

    discipline = fields.Char(string="Discipline")

    def __str__(self):
        return self.discipline

class Group(models.Model):
    _name = "lerm_civil.group"
    _description = "Lerm Group"

    discipline = fields.Many2one('lerm_civil.discipline', string="Discipline")
    group_type = fields.Char(string="Group Type")


    def __str__(self):
        return self.group_type