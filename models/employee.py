from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError


class EmployeeIngerited(models.Model):
    _name = "employee.inherited"
    _inherit = "hr.employee"

    signature = fields.Binary(string="Signature", attachment=True)
    signature_name = fields.Char(string="Signature Name")