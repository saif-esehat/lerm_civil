from odoo import models , fields,api
import json

class SrfReport(models.AbstractModel):
    _name = 'report.lerm_civil.srf_report_template'
    _description = 'SRF Report'

    @api.model
    def _get_report_values(self, docids, data=None):


        # import wdb; wdb.set_trace()
        srf = self.env['lerm.civil.srf'].sudo().browse(docids)

        print(srf,"srf DATA")

        return {
            'srf': srf
        }
