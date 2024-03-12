# from odoo import api, fields, models
# from odoo.exceptions import UserError,ValidationError
# import math

# class ChemicalGyspum(models.Model):
#     _name = "chemical.gyspum"
#     _inherit = "lerm.eln"
#     _rec_name = "name"

#     name = fields.Char("Name",default="Gyspum")
#     parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
#     sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
#     eln_ref = fields.Many2one('lerm.eln',string="Eln")
#     grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)


#     # %Sulphur trioxide (SO3)
#     so3_name = fields.Char("Name", default="SO3")
#     so3_visible = fields.Boolean("SO3", compute="_compute_visible")

#     plaster1 = fields.Char(string="Plaster Of Paris",default="35 Min")
#     retarded1 = fields.Char(string="Retarded Hemihydrate Gypsum Plaster",default="35 Min")
#     anhydrous1 = fields.Char(string="Anhydrous Gypsum Plaster",default="40 Min")
#     keenes1 = fields.Char(string="Keene's Plaster",default="47 Min")

#     wt_of_sample_so3 = fields.Float("original length measurment W1",digits=(16, 4))
#     wt_cr_so3 = fields.Float("Dry measurement ,W2",digits=(16, 4))
#     wt_empty_co3 = fields.Float("Dry length , W3",digits=(16, 4))
#     difference_co3 = fields.Float("D)Diff. in weight(gm)=( B - C )",compute="_compute_difference_co3",digits=(12,4))
#     so3 = fields.Float("SO3  % =  D x 34.30  / A",compute="_compute_so3",digits=(12,3))
