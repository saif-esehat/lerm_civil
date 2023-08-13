from odoo import models , fields,api
import json
import base64
import qrcode
from io import BytesIO
from lxml import etree




class CementReport(models.AbstractModel):
    _name = 'report.lerm_civil.lerm_cement_report'
    _description = 'Cement Report'
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids)
            
        data = {
            "material_id":eln.material.id,
            "grade_id":eln.grade_id.id
        }
        model = eln.get_product_base_calc_line(data).ir_model.model
        cement_data = self.env[model].search([("id","=",eln.model_id)])
        print(cement_data.normal_consistency_trial1)
        return {
            'eln': eln,
            'cement': cement_data
        }
