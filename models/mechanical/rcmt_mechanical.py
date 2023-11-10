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

    # age_of_days = fields.Selection([
    #     ('3', '3'),
    #     ('7', '7'),
    #     ('14', '14'),
    #     ('28', '28'),
    # ], string='Age at Test')
    grade = fields.Many2one('lerm.grade.line',string="Grade",compute="_compute_grade_id",store=True)
   
    age_of_days = fields.Selection([
        ('3days', '3 Days'),
        ('7days', '7 Days'),
        ('14days', '14 Days'),
        ('28days', '28 Days'),
    ], string='Age', default='28days',required=True,compute="_compute_age_of_days")
    date_of_casting = fields.Date(string="Date of Casting",compute="compute_date_of_casting")
    date_of_testing = fields.Date(string="Date of Testing")

    age_of_test = fields.Integer("Age of Test, days",compute="compute_age_of_test")
    difference = fields.Integer("Difference",compute="compute_difference")


    sample_condition = fields.Char(string="Sample Conditioning")

    rcmt_nabl = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail')], string="NABL", compute="_compute_rcmt_nabl", store=True)



    dimension_name = fields.Char("Name",default="Core sample and its dimension")
    child_lines = fields.One2many('mechanical.dimension.rcmt.line','parent_id',string="Parameter")

  

    observed_value_name = fields.Char("Name",default="Observed  Value")
    specimen1_ov1 = fields.Float(string="Average Value of anolye solution °C")
    specimen1_ov2 = fields.Float(string="Absolute Value of applied Voltage V")
    specimen1_ov3 = fields.Float(string="Thickness of specimen mm (L)")

    specimen2_ov1 = fields.Float(string="Average Value of Penetration depth mm (dx)")
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

    @api.onchange('eln_ref')
    def _compute_age_of_days(self):
        for record in self:
            if record.eln_ref.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.eln_ref.sample_id.id)]).days_casting
                if sample_record == '3':
                    record.age_of_days = '3days'
                elif sample_record == '7':
                    record.age_of_days = '7days'
                elif sample_record == '14':
                    record.age_of_days = '14days'
                elif sample_record == '28':
                    record.age_of_days = '28days'
                else:
                    record.age_of_days = None
            else:
                record.age_of_days = None

    @api.depends('date_of_testing','date_of_casting')
    def compute_age_of_test(self):
        for record in self:
            if record.date_of_casting and record.date_of_testing:
                date1 = fields.Date.from_string(record.date_of_casting)
                date2 = fields.Date.from_string(record.date_of_testing)
                date_difference = (date2 - date1).days
                record.age_of_test = date_difference
            else:
                record.age_of_test = 0

    @api.depends('age_of_test','age_of_days')
    def compute_difference(self):
        for record in self:
            age_of_days = 0
            if record.age_of_days == '3days':
                age_of_days = 3
            elif record.age_of_days == '7days':
                age_of_days = 7
            elif record.age_of_days == '14days':
                age_of_days = 14
            elif record.age_of_days == '28days':
                age_of_days = 28
            else:
                age_of_days = 0
            record.difference = record.age_of_test - age_of_days




    @api.onchange('eln_ref')
    def compute_date_of_casting(self):
        for record in self:
            if record.eln_ref.sample_id:
                sample_record = self.env['lerm.srf.sample'].search([('id','=', record.eln_ref.sample_id.id)]).date_casting
                record.date_of_casting = sample_record
            else:
                record.date_of_casting = None


    @api.depends('eln_ref', 'grade')
    def _compute_rcmt_nabl(self):
        for record in self:
            record.rcmt_nabl = 'fail'
            line = self.env['lerm.parameter.master'].search([('internal_id', '=', '36f86e6e-391c-4d7b-818d-28f7b75ea261')])
            materials = self.env['lerm.parameter.master'].search([('internal_id', '=', '36f86e6e-391c-4d7b-818d-28f7b75ea261')]).parameter_table
            for material in materials:
                if material.grade.id == record.grade.id:
                    lab_min = line.lab_min_value
                    lab_max = line.lab_max_value
                    mu_value = line.mu_value

                    # Your logic for rcmt_nabl based on lab_min, lab_max, and mu_value
                    if lab_min >= lab_min and lab_max <= lab_max:
                        record.rcmt_nabl = 'pass'
                        break
                else:
                    record.rcmt_nabl = 'fail'



   

    
    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(RCMT, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record
    


    @api.depends('eln_ref')
    def _compute_grade_id(self):
        if self.eln_ref:
            self.grade = self.eln_ref.grade_id.id







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




   

