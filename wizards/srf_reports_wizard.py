from odoo import api, fields, models,_
from odoo.exceptions import UserError
import logging



class SrfReportsWizard(models.TransientModel):
    _name = "srf.reports.wizard"

    customer = fields.Many2one('res.partner',string="Customer")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def print_srf_reports(self):
        import wdb ; wdb.set_trace()

        srf_ids = self.env['lerm.civil.srf'].sudo().search([('cutomer','=',self.customer)])
        print(srf_ids)

    def discard_print(self):
        return {'type': 'ir.actions.act_window_close'}