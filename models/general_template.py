from odoo import models , fields,api
import json
import base64
import qrcode
from io import BytesIO
from lxml import etree

class DataSheetReport(models.AbstractModel):
    _name = 'report.lerm_civil.datasheet_generaltemplate_report'
    _description = 'DataSheet Report'
    
    
    
    def get_visible_form_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            tree_element = form_view_dom.find(".//field[@name='child_lines']//tree")
            # print(etree.tostring(tree_element, encoding='utf-8').decode())
            if tree_element is not None:
                for field_node in tree_element.findall(".//field"):
                    modifiers = field_node.get('modifiers')
                    if not modifiers or 'invisible' not in modifiers or 'invisible' in modifiers and eval(modifiers)['invisible']:
                        field_name = field_node.get('name')
                        field_label = field_node.get('string')
                        to_show = field_node.get('invisible')
                        if to_show is None:
                            to_show = False
                        else:
                            to_show = True
                        visible_fields.append((field_name, field_label , to_show))
        return visible_fields
    
    @api.model
    def _get_report_values(self, docids, data=None):
        eln = self.env['lerm.eln'].sudo().browse(docids)
        model_id = eln.parameters_result.model_id
        model_name = eln.parameters_result.parameter[0].ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
            columns = self.get_visible_form_fields(model_name)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'tabledata' : columns
        }
    