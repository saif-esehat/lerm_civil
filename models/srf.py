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