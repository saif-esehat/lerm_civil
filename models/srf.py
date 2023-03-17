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