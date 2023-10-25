from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta
import math
import cmath



class RCMT(models.Model):
    _name = "mechanical.rcmt"
    _inherit = "lerm.eln"
    _rec_name = "name_rcmt"


    name_rcmt = fields.Char("Name",default="RCMT")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")


    dimension_name = fields.Char("Name",default="Core sample and its dimension")
    child_lines = fields.One2many('mechanical.dimension.rcmt.line','parent_id',string="Parameter")

  

    observed_value_name = fields.Char("Name",default="Observed  Value")
    specimen1_ov1 = fields.Float()
    specimen1_ov2 = fields.Float()
    specimen1_ov3 = fields.Float()

    specimen2_ov1 = fields.Float()
    specimen2_ov2 = fields.Float()
    specimen2_ov3 = fields.Float()

    specimen3_ov1 = fields.Float()
    specimen3_ov2 = fields.Float()
    specimen3_ov3 = fields.Float()

    specimen2 = fields.Float(string="Specimen-1", compute="_compute_specimen1")
    specimen3 = fields.Float(string="Specimen-2", compute="_compute_specimen2")
    specimen4 = fields.Float(string="Specimen-3", compute="_compute_specimen3")

    @api.depends('child_lines.height')
    def _compute_specimen1(self):
        for record in self:
            if record.child_lines:
                if len(record.child_lines) > 0:
                    first_child_line = record.child_lines[0]
                    record.specimen2 = first_child_line.height
                else:
                    record.specimen2 = 0.0
            else:
                record.specimen2 = 0.0

    @api.depends('child_lines.height')
    def _compute_specimen2(self):
        for record in self:
            if record.child_lines:
                if len(record.child_lines) > 1:
                    second_child_line = record.child_lines[1]
                    record.specimen3 = second_child_line.height
                else:
                    record.specimen3 = 0.0
            else:
                record.specimen3 = 0.0

    @api.depends('child_lines.height')
    def _compute_specimen3(self):
        for record in self:
            if record.child_lines:
                if len(record.child_lines) > 2:
                    third_child_line = record.child_lines[2]
                    record.specimen4 = third_child_line.height
                else:
                    record.specimen4 = 0.0
            else:
                record.specimen4 = 0.0

    specimen1_depth1 = fields.Float(compute="_compute_specimen1_depth1")
    specimen2_depth2 = fields.Float(compute="_compute_specimen1_depth2")
    specimen3_depth3 = fields.Float(compute="_compute_specimen1_depth3")

    @api.depends('child_lines1.dx_avg')
    def _compute_specimen1_depth1(self):
        for record in self:
            if record.child_lines1:
                if len(record.child_lines1) > 0:
                    first_depth_child_line = record.child_lines1[0]
                    record.specimen1_depth1 = first_depth_child_line.dx_avg
                else:
                    record.specimen1_depth1 = 0.0
            else:
                record.specimen1_depth1 = 0.0

    @api.depends('child_lines1.dx_avg')
    def _compute_specimen1_depth2(self):
        for record in self:
            if record.child_lines1:
                if len(record.child_lines1) > 1:
                    second_depth_child_line = record.child_lines1[1]
                    record.specimen2_depth2 = second_depth_child_line.dx_avg
                else:
                    record.specimen2_depth2 = 0.0
            else:
                record.specimen2_depth2 = 0.0

    @api.depends('child_lines1.dx_avg')
    def _compute_specimen1_depth3(self):
        for record in self:
            if record.child_lines1:
                if len(record.child_lines1) > 2:
                    third_depth_child_line = record.child_lines1[2]
                    record.specimen3_depth3 = third_depth_child_line.dx_avg
                else:
                    record.specimen3_depth3 = 0.0
            else:
                record.specimen3_depth3 = 0.0


    specimen1_ov_avg1 = fields.Float(string="Specimen-1 OV Avg 1", compute="_compute_specimen1_ov_avg1")
    specimen2_ov_avg2 = fields.Float(string="Specimen-1 OV Avg 2",compute="_compute_specimen2_ov_avg2")
    specimen3_ov_avg3 = fields.Float(string="Specimen-1 OV Avg 3",compute="_compute_specimen3_ov_avg3")

    # @api.depends('specimen1_ov1', 'specimen2_ov1', 'specimen2', 'specimen1_ov2', 'specimen1_depth1')
    # def _compute_specimen1_ov_avg1(self):
    #     for record in self:
    #         if (record.specimen1_ov1  and record.specimen2 and
    #             record.specimen1_ov2 and record.specimen1_depth1):
                
    #             ov1 = record.specimen1_ov1
    #             ov2 = record.specimen1_ov2
    #             specimen2 = record.specimen2
    #             # ov3 = record.specimen2_ov2
    #             depth1 = record.specimen1_depth1
                
    #             if ov2 != 2:
    #                 specimen1_ov_avg1 = ((0.0239 * (273 + ov1) * (specimen2) / ((ov2 - 2) * (ov1)) * (depth1 - (0.0238) * ((273 + ov1) * specimen2 * depth1 / (ov2 - 2)) ** 0.5)))
    #                 record.specimen1_ov_avg1 = specimen1_ov_avg1
    #             else:
    #                 record.specimen1_ov_avg1 = 0.0
    #         else:
    #             record.specimen1_ov_avg1 = 0.0

    # @api.depends('specimen2_ov1', 'specimen3', 'specimen2_ov2', 'specimen2_depth2')
    # def _compute_specimen1_ov_avg2(self):
    #     for record in self:
    #         if (record.specimen2_ov1  and record.specimen2 and
    #             record.specimen1_ov2 and record.specimen1_depth1):
                
    #             ov1_specimen2 = record.specimen2_ov1
    #             ov2_specimen2 = record.specimen2_ov2
    #             specimen3 = record.specimen3
    #             # ov3 = record.specimen2_ov2
    #             depth2 = record.specimen2_depth2
                
    #             if ov2_specimen2 != 2:
    #                 specimen2_ov_avg2 = ((0.0239 * (273 + ov1_specimen2) * (specimen3) / ((ov2_specimen2 - 2) * (ov1_specimen2)) * (depth2 - (0.0238) * ((273 + ov1_specimen2) * specimen3 * depth2 / (ov2_specimen2 - 2)) ** 0.5)))
    #                 record.specimen2_ov_avg2 = specimen2_ov_avg2
    #             else:
    #                 record.specimen2_ov_avg2 = 0.0
    #         else:
    #             record.specimen2_ov_avg2 = 0.0


    # @api.depends('specimen3_ov1', 'specimen4', 'specimen3_ov2', 'specimen3_depth3')
    # def _compute_specimen1_ov_avg3(self):
    #     for record in self:
    #         if (record.specimen2_ov1  and record.specimen2 and
    #             record.specimen1_ov2 and record.specimen1_depth1):
                
    #             ov1_specimen3 = record.specimen3_ov1
    #             ov2_specimen3 = record.specimen3_ov2
    #             specimen4 = record.specimen4
    #             # ov3 = record.specimen2_ov2
    #             depth3 = record.specimen3_depth3
                
    #             if ov2_specimen3 != 2:
    #                 specimen3_ov_avg3 = ((0.0239 * (273 + ov1_specimen3) * (specimen4) / ((ov2_specimen3 - 2) * (ov1_specimen3)) * (depth3 - (0.0238) * ((273 + ov1_specimen3) * specimen4 * depth3 / (ov2_specimen3 - 2)) ** 0.5)))
    #                 record.specimen3_ov_avg3 = specimen3_ov_avg3
    #             else:
    #                 record.specimen3_ov_avg3 = 0.0
    #         else:
    #             record.specimen3_ov_avg3 = 0.0
    @api.depends('specimen1_ov1', 'specimen2_ov1', 'specimen2', 'specimen1_ov2', 'specimen1_depth1')
    def _compute_specimen1_ov_avg1(self):
        for record in self:
            if (record.specimen1_ov1 and record.specimen2 and
                record.specimen1_ov2 and record.specimen1_depth1):

                ov1 = record.specimen1_ov1
                ov2 = record.specimen1_ov2
                specimen2 = record.specimen2
                depth1 = record.specimen1_depth1

                if ov2 != 2:
                    complex_result = ((0.0239 * (273 + ov1) * specimen2) / ((ov2 - 2) * ov1) * (depth1 - (0.0238 * ((273 + ov1) * specimen2 * depth1 / (ov2 - 2)) ** 0.5)))
                    if complex_result.real >= 0:
                        record.specimen1_ov_avg1 = complex_result.real
                    else:
                        record.specimen1_ov_avg1 = 0.0
                else:
                    record.specimen1_ov_avg1 = 0.0
            else:
                record.specimen1_ov_avg1 = 0.0

    @api.depends('specimen2_ov1', 'specimen3', 'specimen2_ov2', 'specimen2_depth2')
    def _compute_specimen2_ov_avg2(self):
        for record in self:
            ov1_specimen2 = record.specimen2_ov1
            ov2_specimen2 = record.specimen2_ov2
            specimen3 = record.specimen3
            depth2 = record.specimen2_depth2

            if ov1_specimen2 and ov2_specimen2 and specimen3 and depth2:
                if ov2_specimen2 != 2:
                    complex_result = (
                        (0.0239 * (273 + ov1_specimen2) * specimen3) /
                        ((ov2_specimen2 - 2) * ov1_specimen2) *
                        (depth2 - (0.0238 * ((273 + ov1_specimen2) * specimen3 * depth2 / (ov2_specimen2 - 2)) ** 0.5))
                    )
                    if complex_result.real >= 0:
                        record.specimen2_ov_avg2 = complex_result.real
                    else:
                        record.specimen2_ov_avg2 = 0.0
                else:
                    record.specimen2_ov_avg2 = 0.0
            else:
                record.specimen2_ov_avg2 = 0.0

    @api.depends('specimen3_ov1', 'specimen4', 'specimen3_ov2', 'specimen3_depth3')
    def _compute_specimen3_ov_avg3(self):
        for record in self:
            ov1_specimen3 = record.specimen3_ov1
            ov2_specimen3 = record.specimen3_ov2
            specimen4 = record.specimen4
            depth3 = record.specimen3_depth3

            if ov1_specimen3 and ov2_specimen3 and specimen4 and depth3:
                if ov2_specimen3 != 2:
                    complex_result = (
                        (0.0239 * (273 + ov1_specimen3) * specimen4) /
                        ((ov2_specimen3 - 2) * ov1_specimen3) *
                        (depth3 - (0.0238 * ((273 + ov1_specimen3) * specimen4 * depth3 / (ov2_specimen3 - 2)) ** 0.5))
                    )
                    if complex_result.real >= 0:
                        record.specimen3_ov_avg3 = complex_result.real
                    else:
                        record.specimen3_ov_avg3 = 0.0
                else:
                    record.specimen3_ov_avg3 = 0.0
            else:
                record.specimen3_ov_avg3 = 0.0
    

    initial_voltage1 = fields.Char("Initial Voltage(V1)",default="Cell-01")
    initial_voltage2 = fields.Float("Initial Voltage(V1)")
    initial_voltage3 = fields.Char("Initial Voltage(V1)",default="Cell-02")
    initial_voltage4 = fields.Float("Initial Voltage(V1)")
    initial_voltage5 = fields.Char("Initial Voltage(V1)",default="Cell-03")
    initial_voltage6 = fields.Float("Initial Voltage(V1)")


   
    initial_current1 = fields.Char("Initial Current mA",default="Cell-01")
    initial_current2 = fields.Float("Initial Current mA")
    initial_current3 = fields.Char("Initial Current mA",default="Cell-02")
    initial_current4 = fields.Float("Initial Current mA")
    initial_current5 = fields.Char("Initial Current mA",default="Cell-03")
    initial_current6 = fields.Float("Initial Current mA")

    initial_temprrature1 = fields.Char("Initial Temperature during test °C (T1)",default="Reservoir-01")
    initial_temprrature2 = fields.Float("Initial Temperature during test °C (T1)")
    initial_temprrature3 = fields.Char("Initial Temperature during test °C (T1)",default="Reservoir-02")
    initial_temprrature4 = fields.Float("Initial Temperature during test °C (T1)")
    initial_temprrature5 = fields.Char("Initial Temperature during test °C (T1)",default="Reservoir-03")
    initial_temprrature6 = fields.Float("Initial Temperature during test °C (T1)")


    final_voltage1 = fields.Char("Final  Voltage (V2)",default="Cell-01")
    final_voltage2 = fields.Float("Final  Voltage (V2)")
    final_voltage3 = fields.Char("Final  Voltage (V2)",default="Cell-02")
    final_voltage4 = fields.Float("Final  Voltage (V2)")
    final_voltage5 = fields.Char("Final  Voltage (V2)",default="Cell-03")
    final_voltage6 = fields.Float("Final  Voltage (V2)")


    final_curent1 = fields.Char("Final Current mA",default="Cell-01")
    final_curent2 = fields.Float("Final Current mA")
    final_curent3 = fields.Char("Final Current mA",default="Cell-02")
    final_curent4 = fields.Float("Final Current mA")
    final_curent5 = fields.Char("Final Current mA",default="Cell-03")
    final_curent6 = fields.Float("Final Current mA",)


    final_tempreture1 = fields.Char("Final Temperature during test °C (T2)",default="Reservoir-01")
    final_tempreture2 = fields.Float("Final Temperature during test °C (T2)")
    final_tempreture3 = fields.Char("Final Temperature during test °C (T2)",default="Reservoir-02")
    final_tempreture4 = fields.Float("Final Temperature during test °C (T2)")
    final_tempreture5 = fields.Char("Final Temperature during test °C (T2)",default="Reservoir-03")
    final_tempreture6 = fields.Float("Final Temperature during test °C (T2)")


     
     #Measurement for Chloride Penetration depth
     
    depth_name = fields.Char("Name",default="Measurement for Chloride Penetration depth")
    child_lines1 = fields.One2many('mechanical.penetration.depth.rcmt.line','parent_id',string="Parameter")

   

    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(RCMT, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record







    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        # records = self.env['lerm.eln'].search([('id','=', record.eln_id.id)]).parameters_result
        # print("records",records)
        # self.sample_parameters = records
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)



    def get_all_fields(self):
        record = self.env['mechanical.rcmt'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values
    


class DimensionRcmt(models.Model):
    _name = "mechanical.dimension.rcmt.line"
    parent_id = fields.Many2one('mechanical.rcmt',string="Parent Id")
   
    sr_no = fields.Integer(string="Specimen No.",readonly=True, copy=False, default=1)
    height = fields.Float(string="Height (L) mm")
    diameter = fields.Float(string="Diameter mm")
    



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(DimensionRcmt, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1


class PenrtrationDepthRcmt(models.Model):
    _name = "mechanical.penetration.depth.rcmt.line"
    parent_id = fields.Many2one('mechanical.rcmt',string="Parent Id")
   
    depth1 = fields.Float(string="Depth-01")
    depth2 = fields.Float(string="Depth-02")
    depth3 = fields.Float(string="Depth-03")
    depth4 = fields.Float(string="Depth-04")
    depth5 = fields.Float(string="Depth-05")
    depth6 = fields.Float(string="Depth-06")
    dx_avg = fields.Float(string="dx Average mm",compute="_compute_dx_avg")


    @api.depends('depth1', 'depth2', 'depth3', 'depth4', 'depth5', 'depth6')
    def _compute_dx_avg(self):
        for record in self:
            depths = [record.depth1, record.depth2, record.depth3, record.depth4, record.depth5, record.depth6]
            non_empty_depths = [depth for depth in depths if depth is not None]
            if non_empty_depths:
                average = sum(non_empty_depths) / len(non_empty_depths)
                record.dx_avg = average
            else:
                record.dx_avg = 0.0




   

