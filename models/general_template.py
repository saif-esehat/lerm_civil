from odoo import models , fields,api
import json
import base64
import qrcode
from io import BytesIO
from lxml import etree

class DataSheetReport(models.AbstractModel):
    _name = 'report.lerm_civil.datasheet_generaltemplate_report'
    _description = 'DataSheet Report'
    
    
    def get_visible_table_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            tree_element = form_view_dom.find(".//field[@name='child_lines']//tree")
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
                        visible_fields.append((field_name,field_label,to_show))
        return visible_fields
    
    def get_visible_result_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            result_elemnt = form_view_dom.findall(".//field[@identity='result']")
            for field in result_elemnt:
                field_name = field.get('name')
                field_label = field.get('string')
                to_show = field.get('invisible')
                if to_show is None:
                    to_show = False
                else:
                    to_show = True
                visible_fields.append((field_name,field_label,to_show))
                print(visible_fields , 'visv')
        return visible_fields
    
    def get_visible_additonal_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            extra_elemnt = form_view_dom.findall(".//field[@identity='extra']")
            for field in extra_elemnt:
                field_name = field.get('name')
                field_label = field.get('string')
                to_show = field.get('invisible')
                if to_show is None:
                    to_show = False
                else:
                    to_show = True
                visible_fields.append((field_name,field_label,to_show))
        return visible_fields
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.parameters_result.model_id
        model_name = eln.parameters_result.parameter[0].ir_model.name
        print(model_name , 'ajay')
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
            columns = self.get_visible_table_fields(model_name)
            resultfields = self.get_visible_result_fields(model_name)
            extrafields = self.get_visible_additonal_fields(model_name)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        print(columns , 'columns data')
        print(extrafields , 'extrafields')
        print(resultfields , 'result fie;ds')
        return {
            'eln': eln,
            'data' : general_data,
            'tabledata' : columns,
            'resultdata' : resultfields,
            'extradata' : extrafields
        }
    
class GeneralReport(models.AbstractModel):
    _name = 'report.lerm_civil.general_report_template'
    _description = 'General Report'
    
    
    def get_visible_result_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            result_elemnt = form_view_dom.findall(".//field[@identity='result']")
            for field in result_elemnt:
                field_name = field.get('name')
                field_label = field.get('string')
                to_show = field.get('invisible')
                if to_show is None:
                    to_show = False
                else:
                    to_show = True
                visible_fields.append((field_name,field_label,to_show))
                print(visible_fields , 'visv')
        return visible_fields

    def get_visible_table_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            tree_element = form_view_dom.find(".//field[@name='child_lines']//tree")
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
                        visible_fields.append((field_name,field_label,to_show))
        return visible_fields
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        print(data['context'])
        if 'active_id' in data['context']:
            # stamp = data['context']['inreport']
            # print(stamp , 'stamp value')
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.kes_no)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        
        model_id = eln.parameters_result.model_id
        model_name = eln.parameters_result.parameter[0].ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
            columns = self.get_visible_table_fields(model_name)
            resultfields = self.get_visible_result_fields(model_name)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'tabledata' : columns,
            'resultdata' : resultfields,
            'qrcode': qr_code,
            'stamp' : inreport_value,
        }

class SteelTmtBar(models.AbstractModel):
    _name = 'report.lerm_civil.steel_tmt_bar_report1'
    _description = 'Steel TMT Bar'
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        nabl = data.get('nabl')

        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.kes_no)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        model_id = eln.model_id
        # differnt location for product based
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'qrcode': qr_code,
            'stamp' : inreport_value,
            'nabl' : nabl

        }

    

class SteelTmtBarDataSheet(models.AbstractModel):
    _name = 'report.lerm_civil.steel_tmt_bar_datasheet'
    _description = 'Steel TMT Bar DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }

class CementDataSheet(models.AbstractModel):
    _name = 'report.lerm_civil.cement_datasheet'
    _description = 'Cement DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        # model_name = eln.material.product_based_calculation[0].ir_model.name 
        model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }

class GypsumDataSheet(models.AbstractModel):
    _name = 'report.lerm_civil.gypsum_datasheet'
    _description = 'Gypsum DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        # model_name = eln.material.product_based_calculation[0].ir_model.name 
        model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }

class FlyashDatasheet(models.AbstractModel):
    _name = 'report.lerm_civil.flyash_datasheet'
    _description = 'Fly Ash DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        # model_name = eln.material.product_based_calculation[0].ir_model.name 
        model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }

class GgbsDataSheet(models.AbstractModel):
    _name = 'report.lerm_civil.ggbs_datasheet'
    _description = 'GGBS DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        # model_name = eln.material.product_based_calculation[0].ir_model.name 
        model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }
    
class MicrosilicaDatasheet(models.AbstractModel):
        _name = 'report.lerm_civil.microsilica_datasheet'
        _description = 'Microsilica DataSheet'
    
        @api.model
        def _get_report_values(self, docids, data):
            if 'active_id' in data['context']:
                eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
            else:
                eln = self.env['lerm.eln'].sudo().browse(docids) 
            model_id = eln.model_id
            # differnt location for product based
            # model_name = eln.material.product_based_calculation[0].ir_model.name 
            model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
            if model_name:
                general_data = self.env[model_name].sudo().browse(model_id)
            else:
                general_data = self.env['lerm.eln'].sudo().browse(docids)
            return {
                'eln': eln,
                'data' : general_data
            }

class WptDataSheet(models.AbstractModel):
    _name = 'report.lerm_civil.wpt_datasheet'
    _description = 'WPT DataSheet'

    
    def get_visible_table_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            tree_element = form_view_dom.find(".//field[@name='child_lines']//tree")
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
                        visible_fields.append((field_name,field_label,to_show))
        return visible_fields
    
    def get_visible_result_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            result_elemnt = form_view_dom.findall(".//field[@identity='result']")
            for field in result_elemnt:
                field_name = field.get('name')
                field_label = field.get('string')
                to_show = field.get('invisible')
                if to_show is None:
                    to_show = False
                else:
                    to_show = True
                visible_fields.append((field_name,field_label,to_show))
                print(visible_fields , 'visv')
        return visible_fields
    
    def get_visible_additonal_fields(self, model_name):
        form_view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', model_name),
            ('type', '=', 'form')
        ], limit=1)
        visible_fields = []
        if form_view and form_view.arch:
            form_view_dom = etree.fromstring(form_view.arch.encode('utf-8'))
            extra_elemnt = form_view_dom.findall(".//field[@identity='extra']")
            for field in extra_elemnt:
                field_name = field.get('name')
                field_label = field.get('string')
                to_show = field.get('invisible')
                if to_show is None:
                    to_show = False
                else:
                    to_show = True
                visible_fields.append((field_name,field_label,to_show))
        return visible_fields
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.parameters_result.model_id
        model_name = eln.parameters_result.parameter[0].ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
            columns = self.get_visible_table_fields(model_name)
            resultfields = self.get_visible_result_fields(model_name)
            extrafields = self.get_visible_additonal_fields(model_name)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'tabledata' : columns,
            'resultdata' : resultfields,
            'extradata' : extrafields
        }
    
class PTGroutDatasheet(models.AbstractModel):
    _name = 'report.lerm_civil.pt_grout_datasheet'
    _description = 'PT Grout DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        # model_name = eln.material.product_based_calculation[0].ir_model.name 
        model_name = eln.material.product_based_calculation.filtered(lambda record: record.grade.id == eln.grade_id.id).ir_model.name
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data
        }
        
class ConcreteCubeCompresiveReport(models.AbstractModel):
    _name = 'report.lerm_civil.compresive_concrete_cube_report'
    _description = 'Cube Compresive Report'
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        nabl = data.get('nabl')
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.kes_no)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        model_id = eln.model_id
        # differnt location for product based
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'qrcode': qr_code,
            'stamp' : inreport_value,
            'nabl' : nabl
        }
        
class ConcreteCubeCompresiveDatasheet(models.AbstractModel):
    _name = 'report.lerm_civil.compresive_concrete_cube_datasheet'
    _description = 'Compresive strength Cube DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        print(eln.material.parameter_table1[0].parameter_name , 'parameter')
        parameter_data = self.env['lerm.parameter.master'].sudo().search([('internal_id','=',eln.material.parameter_table1[0].internal_id)])
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'parameter' : parameter_data
        }

class SoilReport(models.AbstractModel):
    _name = 'report.lerm_civil.soil_report'
    _description = 'Soil Report'
    
    @api.model
    def _get_report_values(self, docids, data):
        # eln = self.env['lerm.eln'].sudo().browse(docids)
        inreport_value = data.get('inreport', None)
        nabl = data.get('nabl')
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(eln.kes_no)
        qr.make(fit=True)
        qr_image = qr.make_image()

        # Convert the QR code image to base64 string
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Assign the base64 string to a field in the 'srf' object
        qr_code = qr_image_base64
        model_id = eln.model_id
        # differnt location for product based
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'qrcode': qr_code,
            'stamp' : inreport_value,
            'nabl' : nabl
        }
        
class SoilDatasheet(models.AbstractModel):
    _name = 'report.lerm_civil.soil_datasheet'
    _description = 'Soil DataSheet'
    
    @api.model
    def _get_report_values(self, docids, data):
        if 'active_id' in data['context']:
            eln = self.env['lerm.eln'].sudo().search([('sample_id','=',data['context']['active_id'])])
        else:
            eln = self.env['lerm.eln'].sudo().browse(docids) 
        model_id = eln.model_id
        # differnt location for product based
        print(eln.material.parameter_table1[0].parameter_name , 'parameter')
        parameter_data = self.env['lerm.parameter.master'].sudo().search([('internal_id','=',eln.material.parameter_table1[0].internal_id)])
        model_name = eln.material.product_based_calculation[0].ir_model.name 
        if model_name:
            general_data = self.env[model_name].sudo().browse(model_id)
        else:
            general_data = self.env['lerm.eln'].sudo().browse(docids)
        return {
            'eln': eln,
            'data' : general_data,
            'parameter' : parameter_data
        }
        

