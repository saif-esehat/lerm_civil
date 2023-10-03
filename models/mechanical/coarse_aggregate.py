from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math


class CoarseAggregateMechanical(models.Model):
    _name = "mechanical.coarse.aggregate"
    _inherit = "lerm.eln"
    _rec_name = "name"

    name = fields.Char("Name",default="Coarse Aggregate")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")


    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

        
    def get_all_fields(self):
        record = self.env['mechanical.coarse.aggregate'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values



    # Crushing Value
    crushing_value_name = fields.Char("Name",default="Crushing Value")
    crushing_visible = fields.Boolean("Crushing Visible",compute="_compute_visible")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    crushing_value_child_lines = fields.One2many('mechanical.crushing.value.coarse.aggregate.line','parent_id',string="Parameter")

    average_crushing_value = fields.Float(string="Average Aggregate Crushing Value", compute="_compute_average_crushing_value")


    @api.depends('crushing_value_child_lines.crushing_value')
    def _compute_average_crushing_value(self):
        for record in self:
            if record.crushing_value_child_lines:
                sum_crushing_values = sum(record.crushing_value_child_lines.mapped('crushing_value'))
                record.average_crushing_value = sum_crushing_values / len(record.crushing_value_child_lines)
            else:
                record.average_crushing_value = 0.0
   

    

    # Abrasion Value
    abrasion_value_name = fields.Char("Name",default="Los Angeles Abrasion Value")
    abrasion_visible = fields.Boolean("Abrasion Visible",compute="_compute_visible")

    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    abrasion_value_child_lines = fields.One2many('mechanical.abrasion.value.coarse.aggregate.line','parent_id',string="Parameter")
   


    # Specific Gravety 
    specific_gravity_name = fields.Char("Name",default="Specific Gravity & Water Absorption")
    specific_gravity_visible = fields.Boolean("Specific Gravity Visible",compute="_compute_visible")

    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    specific_gravity_child_lines = fields.One2many('mechanical.specific.gravity.and.water.absorption.line','parent_id',string="Parameter")
   

    # Impact Value 
    impact_value_name = fields.Char("Name",default="Aggregate Impact Value")
    impact_visible = fields.Boolean("Impact Visible",compute="_compute_visible")

    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    impact_value_child_lines = fields.One2many('mechanical.impact.value.coarse.aggregate.line','parent_id',string="Parameter")

    average_impact_value = fields.Float(string="Average Aggregate Crushing Value", compute="_compute_average_impact_value")


    @api.depends('impact_value_child_lines.impact_value')
    def _compute_average_impact_value(self):
        for record in self:
            if record.impact_value_child_lines:
                sum_impact_value = sum(record.impact_value_child_lines.mapped('impact_value'))
                record.average_impact_value = sum_impact_value / len(record.impact_value_child_lines)
            else:
                record.average_impact_value = 0.0

    # @api.model
    # def create(self, vals):
    #     # import wdb;wdb.set_trace()
    #     record = super(coarseAggregateMechanical, self).create(vals)
    #     record.parameter_id.write({'model_id':record.id})
    #     return record
   
    # !0% Fine Value
    name_10fine = fields.Char(default="10% Fine Value")
    fine10_visible = fields.Boolean("10% Fine Visible",compute="_compute_visible")

    wt_sample_10fine = fields.Float("Weight of Sample taken in gms, A")
    wt_sample_passing_10fine = fields.Float("Weight of sample passing 2.36 mm IS sieve after applying load in 10 min, B")
    percent_of_fines = fields.Float("Percentage of Fines",compute="_compute_percent_fines")
    load_applied_10fine = fields.Float("Load applied in 10 min, X kN")
    load_10percent_fine_values = fields.Float("Load for 10 percent fines value",compute="_compute_load_10percent_fine_values")

    @api.depends('wt_sample_10fine','wt_sample_passing_10fine')
    def _compute_percent_fines(self):
        for record in self:
            if record.wt_sample_10fine != 0:
                record.percent_of_fines = (record.wt_sample_passing_10fine / record.wt_sample_10fine )*100
            else:
                record.percent_of_fines = 0

    @api.depends('percent_of_fines','load_applied_10fine')
    def _compute_load_10percent_fine_values(self):
        for record in self:
            if record.percent_of_fines != 0:
                record.load_10percent_fine_values = 14 * record.load_applied_10fine/record.percent_of_fines + 4
            else:
                record.load_10percent_fine_values = 0

    
    

    # Soundness Na2SO4
    soundness_na2so4_name = fields.Char("Name",default="Soundness Na2SO4")
    soundness_na2so4_visible = fields.Boolean("Soundness Na2SO4 Visible",compute="_compute_visible")

    soundness_na2so4_child_lines = fields.One2many('mechanical.soundness.na2so4.line','parent_id',string="Parameter")
    total_na2so4 = fields.Integer(string="Total",compute="_compute_total_na2so4")
    soundness_na2so4 = fields.Float(string="Soundness",compute="_compute_soundness_na2so4")
    

    @api.depends('soundness_na2so4_child_lines.weight_before_test')
    def _compute_total_na2so4(self):
        for record in self:
            record.total_na2so4 = sum(record.soundness_na2so4_child_lines.mapped('weight_before_test'))
    

    @api.depends('soundness_na2so4_child_lines.cumulative_loss_percent')
    def _compute_soundness_na2so4(self):
        for record in self:
            record.soundness_na2so4 = sum(record.soundness_na2so4_child_lines.mapped('cumulative_loss_percent'))


    # Soundness MgSO4
    soundness_mgso4_name = fields.Char("Name",default="Soundness MgSO4")
    soundness_mgso4_visible = fields.Boolean("Soundness MgSO4 Visible",compute="_compute_visible")

    soundness_mgso4_child_lines = fields.One2many('mechanical.soundness.mgso4.line','parent_id',string="Parameter")
    total_mgso4 = fields.Integer(string="Total",compute="_compute_total_mgso4")
    soundness_mgso4 = fields.Float(string="Soundness",compute="_compute_soundness_mgso4")
    
    

    @api.depends('soundness_mgso4_child_lines.weight_before_test')
    def _compute_total_mgso4(self):
        for record in self:
            record.total_mgso4 = sum(record.soundness_mgso4_child_lines.mapped('weight_before_test'))
    

    @api.depends('soundness_mgso4_child_lines.cumulative_loss_percent')
    def _compute_soundness_mgso4(self):
        for record in self:
            record.soundness_mgso4 = sum(record.soundness_mgso4_child_lines.mapped('cumulative_loss_percent'))


    #Elongation Index
    elongation_name = fields.Char("Name",default="Elongation Index")
    elongation_visible = fields.Boolean("Elongation Visible",compute="_compute_visible")

    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    elongation_child_lines = fields.One2many('mechanical.elongation.index.line','parent_id',string="Parameter")
    wt_retained_total_elongation = fields.Float(string="Wt Retained Total",compute="_compute_wt_retained_total_elongation")
    elongated_retain_total = fields.Float(string="Elongated Retained Total",compute="_compute_elongated_retain")
    flaky_passing_total = fields.Float(string="Flaky Passing Total",compute="_compute_flaky_passing")
    aggregate_elongation = fields.Float(string="Aggregate Elongation Value in %",compute="_compute_aggregate_elongation")
    aggregate_flakiness = fields.Float(string="Aggregate Flakiness Value in %",compute="_compute_aggregate_flakiness")
    # combine_elongation_flakiness = fields.Float(string="Combine Elongation & Flakiness Value in %",compute="_compute_combine_elongation_flakiness")


    @api.depends('elongation_child_lines.wt_retained')
    def _compute_wt_retained_total_elongation(self):
        for record in self:
            record.wt_retained_total_elongation = sum(record.elongation_child_lines.mapped('wt_retained'))

    @api.depends('elongation_child_lines.elongated_retain')
    def _compute_elongated_retain(self):
        for record in self:
            record.elongated_retain_total = sum(record.elongation_child_lines.mapped('elongated_retain'))

    # @api.depends('elongation_child_lines.flaky_passing')
    # def _compute_flaky_passing(self):
    #     for record in self:
    #         record.flaky_passing_total = sum(record.elongation_child_lines.mapped('flaky_passing'))

    @api.depends('wt_retained_total_elongation','elongated_retain_total')
    def _compute_aggregate_elongation(self):
        for record in self:
            if record.elongated_retain_total != 0:
                record.aggregate_elongation = record.elongated_retain_total / record.wt_retained_total_elongation * 100
            else:
                record.aggregate_elongation = 0.0


    # @api.depends('wt_retained_total','flaky_passing_total')
    # def _compute_aggregate_flakiness(self):
    #     for record in self:
    #         if record.flaky_passing_total != 0:
    #             record.aggregate_flakiness = record.flaky_passing_total / record.wt_retained_total * 100
    #         else:
    #             record.aggregate_flakiness = 0.0

    # @api.depends('aggregate_elongation','aggregate_flakiness')
    # def _compute_combine_elongation_flakiness(self):
    #     for record in self:
    #         if record.aggregate_flakiness != 0:
    #             record.combine_elongation_flakiness = record.aggregate_elongation + record.aggregate_flakiness
    #         else:
    #             record.combine_elongation_flakiness = 0.0


    # Flakiness Index 
    flakiness_name = fields.Char("Name",default="Flakiness Index")
    flakiness_visible = fields.Boolean("Flakiness Visible",compute="_compute_visible")

    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    flakiness_child_lines = fields.One2many('mechanical.flakiness.index.line','parent_id',string="Parameter")
    wt_retained_total_flakiness = fields.Float(string="Wt Retained Total",compute="_compute_wt_retained_total_flakiness")
    flaky_passing_total = fields.Float(string="Flaky Passing Total",compute="_compute_flaky_passing")
    aggregate_flakiness = fields.Float(string="aggregate Flakiness Value in %",compute="_compute_aggregate_flakiness")
    combine_elongation_flakiness = fields.Float(string="Combine Elongation & Flakiness Value in %",compute="_compute_combine_elongation_flakiness")
    # elongated_retain_total = fields.Float(string="Elongated Retained Total",compute="_compute_elongated_retain")
    # aggregate_elongation = fields.Float(string="aggregate Elongation Value in %",compute="_compute_aggregate_elongation")

    @api.depends('flakiness_child_lines.wt_retained')
    def _compute_wt_retained_total_flakiness(self):
        for record in self:
            record.wt_retained_total_flakiness = sum(record.flakiness_child_lines.mapped('wt_retained'))

    @api.depends('flakiness_child_lines.flaky_passing')
    def _compute_flaky_passing(self):
        for record in self:
            record.flaky_passing_total = sum(record.flakiness_child_lines.mapped('flaky_passing'))


    @api.depends('wt_retained_total_flakiness','flaky_passing_total')
    def _compute_aggregate_flakiness(self):
        for record in self:
            if record.flaky_passing_total != 0:
                record.aggregate_flakiness = record.flaky_passing_total / record.wt_retained_total_flakiness * 100
            else:
                record.aggregate_flakiness = 0.0

    @api.depends('aggregate_elongation','aggregate_flakiness')
    def _compute_combine_elongation_flakiness(self):
        for record in self:
            if record.aggregate_flakiness != 0:
                record.combine_elongation_flakiness = record.aggregate_elongation + record.aggregate_flakiness
            else:
                record.combine_elongation_flakiness = 0.0

    # Deleterious Content

    name_finer75 = fields.Char("Name",default="Material Finer than 75 Micron")
    finer75_visible = fields.Boolean("Finer 75 Visible",compute="_compute_visible")

    wt_sample_finer75 = fields.Float("Weight of Sample in gms")
    wt_dry_sample_finer75 = fields.Float("Weight of dry sample after retained in 75 microns")
    material_finer75 = fields.Float("Material finer than 75 micron in %",compute="_compute_finer75")

    @api.depends('wt_sample_finer75','wt_dry_sample_finer75')
    def _compute_finer75(self):
        for record in self:
            if record.wt_sample_finer75 != 0:
                record.material_finer75 = (record.wt_sample_finer75 - record.wt_dry_sample_finer75)/record.wt_sample_finer75 * 100
            else:
                record.material_finer75 = 0

    
    name_clay_lumps = fields.Char("Name",default="Determination of Clay Lumps")
    clay_lump_visible = fields.Boolean("Clay Lump Visible",compute="_compute_visible")

    wt_sample_clay_lumps = fields.Float("Weight of Sample in gms")
    wt_dry_sample_clay_lumps = fields.Float("Weight of dry sample after retained in 75 microns")
    clay_lumps_percent = fields.Float("Clay Lumps in %",compute="_compute_clay_lumps")

    @api.depends('wt_sample_clay_lumps','wt_dry_sample_clay_lumps')
    def _compute_clay_lumps(self):
        for record in self:
            if record.wt_sample_clay_lumps != 0:
                record.clay_lumps_percent = (record.wt_sample_clay_lumps - record.wt_dry_sample_clay_lumps)/record.wt_sample_clay_lumps * 100
            else:
                record.clay_lumps_percent = 0


    name_light_weight = fields.Char("Name",default="Determination of Light Weight Particles")
    light_weight_visible = fields.Boolean("Light Weight Visible",compute="_compute_visible")

    wt_sample_light_weight = fields.Float("Weight of Sample in gms")
    wt_dry_sample_light_weight = fields.Float("Weight of dry sample after retained in 75 microns")
    light_weight_percent = fields.Float("Light Weight Particle in %",compute="_compute_light_weight")

    @api.depends('wt_sample_light_weight','wt_dry_sample_light_weight')
    def _compute_light_weight(self):
        for record in self:
            if record.wt_sample_light_weight != 0:
                record.light_weight_percent = (record.wt_sample_light_weight - record.wt_dry_sample_light_weight)/record.wt_sample_light_weight * 100
            else:
                record.light_weight_percent = 0




    # Bulk Density
    loose_bulk_density_name = fields.Char("Name",default="Loose Bulk Density (LBD)")
    loose_bulk_visible = fields.Boolean("Loose Bulk Density Visible",compute="_compute_visible")

    loose_bulk_density_child_lines = fields.One2many('coarse.aggregate.loose.bulk.density.line','parent_id',string="Parameter")


    rodded_bulk_density_name = fields.Char("Name",default="Rodded Bulk Density (RBD)")
    rodded_bulk_visible = fields.Boolean("Rodded Bulk Density Visible",compute="_compute_visible")

    rodded_bulk_density_child_lines = fields.One2many('coarse.aggregate.rodded.bulk.density.line','parent_id',string="Parameter")


    # Sieve Analysis 
    sieve_analysis_name = fields.Char("Name",default="Sieve Analysis")
    sieve_visible = fields.Boolean("Sieve Analysis Visible",compute="_compute_visible")

    sieve_analysis_child_lines = fields.One2many('mechanical.coarse.aggregate.sieve.analysis.line','parent_id',string="Parameter")
    total_sieve_analysis = fields.Integer(string="Total",compute="_compute_total_sieve")
    # cumulative = fields.Float(string="Cumulative",compute="_compute_cumulative_sieve")


    def calculate_sieve(self): 
        for record in self:
            for line in record.sieve_analysis_child_lines:
                print("Rows",str(line.percent_retained))
                previous_line = line.serial_no - 1
                if previous_line == 0:
                    if line.percent_retained == 0:
                        # print("Percent retained 0",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 })
                    else:
                        # print("Percent retained else",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 -line.percent_retained})
                else:
                    previous_line_record = self.env['mechanical.coarse.aggregate.sieve.analysis.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': previous_line_record + line.percent_retained})
                    line.write({'passing_percent': 100-(previous_line_record + line.percent_retained)})
                    print("Previous Cumulative",previous_line_record)
                    

 

    @api.depends('sieve_analysis_child_lines.wt_retained')
    def _compute_total_sieve(self):
        for record in self:
            print("recordd",record)
            record.total_sieve_analysis = sum(record.sieve_analysis_child_lines.mapped('wt_retained'))


    # @api.depends('sieve_analysis_child_lines.wt_retained')
    # def _compute_cumulative_sieve(self):
    #     for record in self:
    #         print("recordd",record)
    #         record.cumulative = sum(record.sieve_analysis_child_lines.mapped('wt_retained'))


    # Aggregate grading  

    aggregate_grading_name = fields.Char("Name",default="All in Aggregate Grading")
    aggregate_grading_visible = fields.Boolean("Sieve Analysis Visible",compute="_compute_visible")

    aggregate_grading_child_lines = fields.One2many('mechanical.aggregate.grading.line','parent_id',string="Parameter")
    total_aggregate_grading = fields.Integer(string="Total",compute="_compute_total_aggregate_grading")
    # cumulative_aggregate_grading = fields.Float(string="Cumulative",compute="_compute_cumulative_aggregate_grading")


    def calculate_aggregate(self): 
        for record in self:
            for line in record.aggregate_grading_child_lines:
                print("Rows",str(line.percent_retained))
                previous_line = line.serial_no - 1
                if previous_line == 0:
                    if line.percent_retained == 0:
                        # print("Percent retained 0",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 })
                    else:
                        # print("Percent retained else",line.percent_retained)
                        line.write({'cumulative_retained': line.percent_retained})
                        line.write({'passing_percent': 100 -line.percent_retained})
                else:
                    previous_line_record = self.env['mechanical.aggregate.grading.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': previous_line_record + line.percent_retained})
                    line.write({'passing_percent': 100-(previous_line_record + line.percent_retained)})
                    print("Previous Cumulative",previous_line_record)
                    

 

    # @api.depends('aggregate_grading_child_lines.wt_retained')
    # def _compute_cumulative_aggregate_grading(self):
    #     for record in self:
    #         print("recordd",record)
    #         record.cumulative_aggregate_grading = sum(record.aggregate_grading_child_lines.mapped('wt_retained'))


    @api.depends('aggregate_grading_child_lines.wt_retained')
    def _compute_total_aggregate_grading(self):
        for record in self:
            print("recordd",record)
            record.total_aggregate_grading = sum(record.aggregate_grading_child_lines.mapped('wt_retained'))



    # Angularity 
    angularity_name = fields.Char("Name",default="Angularity Number")
    angularity_visible = fields.Boolean("Angularity",compute="_compute_visible")
    mean_wt_aggregate = fields.Float("Mean weight of the aggregate in the cylinder in gm , W")
    wt_water_required_angularity = fields.Float("Weight of water required to fill the cylinder in gm, C")
    specific_gravity_aggregate_angularity = fields.Float("Specific gravity of aggregate, GA")
    angularity_number = fields.Float("Angularity number",compute="_compute_angularity_number")

    @api.depends('mean_wt_aggregate','wt_water_required_angularity','specific_gravity_aggregate_angularity')
    def _compute_angularity_number(self):
        for record in self:
            if (record.wt_water_required_angularity * record.specific_gravity_aggregate_angularity) != 0:
                record.angularity_number = 67 - (100 * record.mean_wt_aggregate)/(record.wt_water_required_angularity * record.specific_gravity_aggregate_angularity)
            else:
                record.angularity_number = 0

    @api.depends('eln_ref')
    def _compute_visible(self):
        for record in self:
            record.crushing_visible = False
            record.abrasion_visible = False
            record.specific_gravity_visible = False
            record.impact_visible = False
            record.fine10_visible = False
            record.soundness_na2so4_visible = False
            record.soundness_mgso4_visible = False
            record.elongation_visible = False
            record.flakiness_visible = False
            record.finer75_visible = False
            record.clay_lump_visible = False
            record.light_weight_visible = False
            record.loose_bulk_visible = False
            record.rodded_bulk_visible = False
            record.sieve_visible = False
            record.aggregate_grading_visible = False
            record.angularity_visible = False




            for sample in record.sample_parameters:
                if sample.internal_id == 'ee2d3ead-3bf8-4ae5-8e5d-dfe983111f71':
                    record.crushing_visible = True
                if sample.internal_id == '37f2161e-5cc0-413f-b76c-10478c65baf9':
                    record.abrasion_visible = True
                if sample.internal_id == '3114db41-cfa7-49ad-9324-fcdbc9661038':
                    record.specific_gravity_visible = True
                if sample.internal_id == '2bd241bd-4bc3-4fe0-bea2-c1c15ff867a2':
                    record.impact_visible = True
                if sample.internal_id == '5f506c08-4369-491d-93a6-030514c29661':
                    record.fine10_visible = True
                if sample.internal_id == '153f3c8b-6ccb-4db0-b89d-02db61f61e81':
                    record.soundness_na2so4_visible = True
                if sample.internal_id == '89650e58-11a6-42af-8eb7-187467443a79':
                    record.soundness_mgso4_visible = True
                if sample.internal_id == '9effe915-e5a3-45a7-aaeb-10caababd667':
                    record.elongation_visible = True
                if sample.internal_id == 'be7a60bc-bb2c-410d-b91a-4f8730a4ac6f':
                    record.flakiness_visible = True
                if sample.internal_id == '988f5bf6-c865-453c-9cd6-993a5a59ad95':
                    record.finer75_visible = True
                if sample.internal_id == 'd7e389bc-21ad-41eb-a602-f448f996eb2f':
                    record.clay_lump_visible = True
                if sample.internal_id == 'e7cc6b68-2550-4e1e-a28e-8526295e733f':
                    record.light_weight_visible = True
                if sample.internal_id == '65a41d1f-d557-438e-8fd1-2c619a334d02':
                    record.loose_bulk_visible = True
                if sample.internal_id == '357f579d-a310-4015-bc11-28a85c53ac83':
                    record.rodded_bulk_visible = True
                if sample.internal_id == 'c2168fff-e47c-4155-99ff-9d7dc223e768':
                    record.sieve_visible = True
                if sample.internal_id == '6976f6b5-5756-4ef7-a680-50b0c0dbccc8':
                    record.aggregate_grading_visible = True
                if sample.internal_id == '5c163fc2-c88c-4233-921e-1eae56c3ba23':
                    record.angularity_visible = True
                

    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(CoarseAggregateMechanical, self).create(vals)
        record.get_all_fields()
        record.eln_ref.write({'model_id':record.id})
        return record

   
    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

    def get_all_fields(self):
        record = self.env['mechanical.coarse.aggregate'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values

class AggregateGradingLine(models.Model):
    _name = "mechanical.aggregate.grading.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %")



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('serial_no'))
                vals['serial_no'] = max_serial_no + 1

        return super(AggregateGradingLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.serial_no = index + 1

    def write(self, vals):
        # Handle row deletions and adjust serial numbers
        if 'parent_id' in vals or 'wt_retained' in vals:
            for record in self:
                if record.parent_id and record.parent_id == vals.get('parent_id') and 'wt_retained' in vals:
                    record.percent_retained = vals['wt_retained'] / record.parent_id.total_aggregate_grading * 100 if record.parent_id.total_aggregate_grading else 0

            new_self = super(AggregateGradingLine, self).write(vals)

            if 'wt_retained' in vals:
                for record in self:
                    record.parent_id._compute_total_aggregate_grading()

            return new_self

        return super(AggregateGradingLine, self).write(vals)

    def unlink(self):
        # Get the parent_id before the deletion
        parent_id = self[0].parent_id

        res = super(AggregateGradingLine, self).unlink()

        if parent_id:
            parent_id.aggregate_grading_child_lines._reorder_serial_numbers()

        return res


    @api.depends('wt_retained', 'parent_id.total_aggregate_grading')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / self.parent_id.total_sieve_analysis * 100
            except ZeroDivisionError:
                record.percent_retained = 0


    @api.depends('cumulative_retained')
    def _compute_cum_retained(self):
        self.cumulative_retained=0
        


    def get_previous_record(self):
        for record in self:
            # import wdb; wdb.set_trace()
            sorted_lines = sorted(record.parent_id.aggregate_grading_child_lines, key=lambda r: r.id)
            # index = sorted_lines.index(record)
            # print("Working")

    




class SieveAnalysisLine(models.Model):
    _name = "mechanical.coarse.aggregate.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %")



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('serial_no'))
                vals['serial_no'] = max_serial_no + 1

        return super(SieveAnalysisLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.serial_no = index + 1

    def write(self, vals):
        # Handle row deletions and adjust serial numbers
        if 'parent_id' in vals or 'wt_retained' in vals:
            for record in self:
                if record.parent_id and record.parent_id == vals.get('parent_id') and 'wt_retained' in vals:
                    record.percent_retained = vals['wt_retained'] / record.parent_id.total * 100 if record.parent_id.total else 0

            new_self = super(SieveAnalysisLine, self).write(vals)

            if 'wt_retained' in vals:
                for record in self:
                    record.parent_id._compute_total()

            return new_self

        return super(SieveAnalysisLine, self).write(vals)

    def unlink(self):
        # Get the parent_id before the deletion
        parent_id = self[0].parent_id

        res = super(SieveAnalysisLine, self).unlink()

        if parent_id:
            parent_id.sieve_analysis_child_lines._reorder_serial_numbers()

        return res


    @api.depends('wt_retained', 'parent_id.total_sieve_analysis')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / self.parent_id.total_sieve_analysis * 100
            except ZeroDivisionError:
                record.percent_retained = 0


    @api.depends('cumulative_retained')
    def _compute_cum_retained(self):
        self.cumulative_retained=0
        


    def get_previous_record(self):
        for record in self:
            # import wdb; wdb.set_trace()
            sorted_lines = sorted(record.parent_id.sieve_analysis_child_lines, key=lambda r: r.id)
            # index = sorted_lines.index(record)
            # print("Working")



       


class LooseBulkDensityLine(models.Model):
    _name = "coarse.aggregate.loose.bulk.density.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    weight_empty_bucket = fields.Float(string="Weight of Empty Bucket in kg")
    volume_of_bucket = fields.Float(string="Volume of Bucket in cubic meter")
    sample_plus_bucket = fields.Float(string="[Sample Weight + Bucket  Weight] in kg")
    sample_weight = fields.Float(string="Sample Weight in kg",compute="_compute_sample_weight")
    loose_bulk_density = fields.Float(string="Loose Bulk Density in kg per cubic meter",compute="_compute_loose_bulk_density")


    @api.depends('sample_plus_bucket', 'weight_empty_bucket')
    def _compute_sample_weight(self):
        for record in self:
            record.sample_weight = record.sample_plus_bucket - record.weight_empty_bucket

    

    @api.depends('sample_weight', 'volume_of_bucket')
    def _compute_loose_bulk_density(self):
        for record in self:
            if record.volume_of_bucket:
                record.loose_bulk_density = record.sample_weight / record.volume_of_bucket
            else:
                record.loose_bulk_density = 0.0


    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(LooseBulkDensityLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

class RoddedBulkDensityLine(models.Model):
    _name = "coarse.aggregate.rodded.bulk.density.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    weight_empty_bucket = fields.Float(string="Weight of Empty Bucket in kg")
    volume_of_bucket = fields.Float(string="Volume of Bucket in cubic meter")
    sample_plus_bucket = fields.Float(string="[Sample Weight + Bucket  Weight] in kg")
    sample_weight = fields.Float(string="Sample Weight in kg",compute="_compute_sample_weight")
    rodded_bulk_density = fields.Float(string="Rodded Bulk Density in kg per cubic meter",compute="_compute_roddede_bulk_density")


    @api.depends('sample_plus_bucket', 'weight_empty_bucket')
    def _compute_sample_weight(self):
        for record in self:
            record.sample_weight = record.sample_plus_bucket - record.weight_empty_bucket

    

    @api.depends('sample_weight', 'volume_of_bucket')
    def _compute_roddede_bulk_density(self):
        for record in self:
            if record.volume_of_bucket:
                record.rodded_bulk_density = record.sample_weight / record.volume_of_bucket
            else:
                record.rodded_bulk_density = 0.0



    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(RoddedBulkDensityLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

class ElongationIndexLine(models.Model):
    _name = "mechanical.elongation.index.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="I.S Sieve Size")
    wt_retained = fields.Integer(string="Wt Retained (in gms)")
    elongated_retain = fields.Float(string="Elongated Retained (in gms)")
    # flaky_passing = fields.Float(string="Flaky Passing (in gms)")
    

    

    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(FlakinessElongationIndexLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

class FlakinessIndexLine(models.Model):
    _name = "mechanical.flakiness.index.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="I.S Sieve Size")
    wt_retained = fields.Integer(string="Wt Retained (in gms)")
    # elongated_retain = fields.Float(string="Elongated Retained (in gms)")
    flaky_passing = fields.Float(string="Flaky Passing (in gms)")
    

    

    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(FlakinessElongationIndexLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1

class SoundnessNa2Line(models.Model):
    _name = "mechanical.soundness.na2so4.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate', string="Parent Id")
    
    sieve_size_passing = fields.Char(string="Sieve Size Passing")
    sieve_size_retained = fields.Char(string="Sieve Size Retained")
    weight_before_test = fields.Float(string="Weight of test fraction before test in gm.")
    weight_after_test = fields.Float(string="Weight of test feaction Passing Finer Sieve After test")
    grading_original_sample = fields.Float(string="Grading of Original sample in %", compute="_compute_grading")
    passing_percent = fields.Float(string="Percentage Passing Finer Sieve After test (Percentage Loss)",compute="_compute_passing_percent")
    cumulative_loss_percent = fields.Float(string="Commulative percentage Loss",compute="_compute_cumulative_na2so4")
    
    @api.depends('parent_id.total_na2so4','weight_before_test')
    def _compute_grading(self):
        for record in self:
            try:
                record.grading_original_sample = (record.weight_before_test/record.parent_id.total_na2so4)*100
            except ZeroDivisionError:
                record.grading_original_sample = 0

    @api.depends('weight_before_test','weight_after_test')
    def _compute_passing_percent(self):
        for record in self:
            try:
                record.passing_percent = (record.weight_after_test / record.weight_before_test)*100
            except:
                record.passing_percent = 0

    @api.depends('weight_after_test', 'parent_id.total_na2so4')
    def _compute_cumulative_na2so4(self):
        for record in self:
            try:
                record.cumulative_loss_percent = (record.weight_after_test / record.parent_id.total_na2so4) * 100
            except:
                record.cumulative_loss_percent = 0



    

class SoundnessMgLine(models.Model):
    _name = "mechanical.soundness.mgso4.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate', string="Parent Id")
    
    sieve_size_passing = fields.Char(string="Sieve Size Passing")
    sieve_size_retained = fields.Char(string="Sieve Size Retained")
    weight_before_test = fields.Float(string="Weight of test fraction before test in gm.")
    weight_after_test = fields.Float(string="Weight of test feaction Passing Finer Sieve After test")
    grading_original_sample = fields.Float(string="Grading of Original sample in %", compute="_compute_grading")
    passing_percent = fields.Float(string="Percentage Passing Finer Sieve After test (Percentage Loss)",compute="_compute_passing_percent")
    cumulative_loss_percent = fields.Float(string="Commulative percentage Loss",compute="_compute_cumulative_mgso4")
    
    @api.depends('parent_id.total_mgso4','weight_before_test')
    def _compute_grading(self):
        for record in self:
            try:
                record.grading_original_sample = (record.weight_before_test/record.parent_id.total_mgso4)*100
            except ZeroDivisionError:
                record.grading_original_sample = 0

    @api.depends('weight_before_test','weight_after_test')
    def _compute_passing_percent(self):
        for record in self:
            try:
                record.passing_percent = (record.weight_after_test / record.weight_before_test)*100
            except:
                record.passing_percent = 0

    @api.depends('weight_after_test', 'parent_id.total_mgso4')
    def _compute_cumulative_mgso4(self):
        for record in self:
            try:
                record.cumulative_loss_percent = (record.weight_after_test / record.parent_id.total_mgso4) * 100
            except:
                record.cumulative_loss_percent = 0



    
class ImpactValueLine(models.Model):
    _name = "mechanical.impact.value.coarse.aggregate.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")

    sample_no = fields.Integer(string="Sample", readonly=True, copy=False, default=1)
    wt_of_cylinder = fields.Integer(string="Weight of cylindrical measure in gms")
    total_wt_of_dried = fields.Integer(string="Total Wt. of Oven dried (4 hrs) aggregate sample + cylindrical measure in gms")
    total_wt_aggregate = fields.Float(string="Total Wt. of Oven dried (4 hrs) aggregate sample filling the cylindrical measure in gms", compute="_compute_total_wt_aggregate")
    wt_of_aggregate_passing = fields.Float(string="Wt. of aggregate passing 2.36 mm sieve after the test in gms")
    wt_of_aggregate_retained = fields.Float(string="Wt. of aggregate retained on 2.36 mm sieve after the test in gms", compute="_compute_wt_of_aggregate_retained")
    impact_value = fields.Float(string="Aggregate Impact value", compute="_compute_impact_value")


    @api.depends('total_wt_of_dried', 'wt_of_cylinder')
    def _compute_total_wt_aggregate(self):
        for rec in self:
            rec.total_wt_aggregate = rec.total_wt_of_dried - rec.wt_of_cylinder


    @api.depends('total_wt_aggregate', 'wt_of_aggregate_passing')
    def _compute_wt_of_aggregate_retained(self):
        for rec in self:
            rec.wt_of_aggregate_retained = rec.total_wt_aggregate - rec.wt_of_aggregate_passing


    @api.depends('wt_of_aggregate_passing', 'total_wt_aggregate')
    def _compute_impact_value(self):
        for rec in self:
            if rec.total_wt_aggregate != 0:
                rec.impact_value = (rec.wt_of_aggregate_passing / rec.total_wt_aggregate) * 100
            else:
                rec.impact_value = 0.0


    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sample_no'))
    #             vals['sample_no'] = max_serial_no + 1

    #     return super(CrushingValueLine, self).create(vals)

    # def _reorder_serial_numbers(self):
    #     # Reorder the serial numbers based on the positions of the records in child_lines
    #     records = self.sorted('id')
    #     for index, record in enumerate(records):
    #         record.sample_no = index + 1

    


class CrushingValueLine(models.Model):
    _name = "mechanical.crushing.value.coarse.aggregate.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")

    sample_no = fields.Integer(string="Sample", readonly=True, copy=False, default=1)
    wt_of_cylinder = fields.Integer(string="Weight of the empty cylinder in gms")
    total_wt_of_dried = fields.Integer(string="Total weight of oven dried ( 4.0 hrs ) aggregate sample filling the cylindrical measure in gms")
    total_wt_aggregate = fields.Float(string="Total weight of aggeregate in the cylinder in gms", compute="_compute_total_wt_aggregate")
    wt_of_aggregate_passing = fields.Float(string="Weight of aggregate fines passing 2.36 mm sieve after  the application of Load gms")
    wt_of_aggregate_retained = fields.Float(string="Weight of aggregate retained on 2.36 mm sieve after the test in gms", compute="_compute_wt_of_aggregate_retained")
    crushing_value = fields.Float(string="Aggregate Crushing value", compute="_compute_crushing_value")


    @api.depends('total_wt_of_dried', 'wt_of_cylinder')
    def _compute_total_wt_aggregate(self):
        for rec in self:
            rec.total_wt_aggregate = rec.total_wt_of_dried - rec.wt_of_cylinder


    @api.depends('total_wt_aggregate', 'wt_of_aggregate_passing')
    def _compute_wt_of_aggregate_retained(self):
        for rec in self:
            rec.wt_of_aggregate_retained = rec.total_wt_aggregate - rec.wt_of_aggregate_passing


    @api.depends('wt_of_aggregate_passing', 'total_wt_aggregate')
    def _compute_crushing_value(self):
        for rec in self:
            if rec.total_wt_aggregate != 0:
                rec.crushing_value = (rec.wt_of_aggregate_passing / rec.total_wt_aggregate) * 100
            else:
                rec.crushing_value = 0.0


    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sample_no'))
    #             vals['sample_no'] = max_serial_no + 1

    #     return super(CrushingValueLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sample_no = index + 1



class SpecificGravityAndWaterAbsorptionLine(models.Model):
    _name = "mechanical.specific.gravity.and.water.absorption.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Test", readonly=True, copy=False, default=1)
    wt_surface_dry = fields.Integer(string="Weight of saturated surface dry (SSD) sample in air in gms")
    wt_sample_inwater = fields.Integer(string="Weight of saturated sample in water in gms")
    oven_dried_wt = fields.Integer(string="Oven dried weight of sample in gms")
    specific_gravity = fields.Float(string="Specific Gravity",compute="_compute_specific_gravity")
    water_absorption = fields.Float(string="Water absorption  %",compute="_compute_water_absorption")


    @api.depends('wt_surface_dry', 'wt_sample_inwater', 'oven_dried_wt')
    def _compute_specific_gravity(self):
        for line in self:
            if line.wt_surface_dry - line.wt_sample_inwater != 0:
                line.specific_gravity = line.oven_dried_wt / (line.wt_surface_dry - line.wt_sample_inwater)
            else:
                line.specific_gravity = 0.0



    @api.depends('wt_surface_dry', 'oven_dried_wt')
    def _compute_water_absorption(self):
        for line in self:
            if line.oven_dried_wt != 0:
                line.water_absorption = ((line.wt_surface_dry - line.oven_dried_wt) / line.oven_dried_wt) * 100
            else:
                line.water_absorption = 0.0


    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(SpecificGravityAndWaterAbsorptionLine, self).create(vals)

    # def _reorder_serial_numbers(self):
    #     # Reorder the serial numbers based on the positions of the records in child_lines
    #     records = self.sorted('id')
    #     for index, record in enumerate(records):
    #         record.sr_no = index + 1





class AbrasionValueCoarseAggregateLine(models.Model):
    _name = "mechanical.abrasion.value.coarse.aggregate.line"
    parent_id = fields.Many2one('mechanical.coarse.aggregate',string="Parent Id")
   
    sr_no = fields.Integer(string="Test", readonly=True, copy=False, default=1)
    total_weight_sample = fields.Integer(string="Total weight of Sample in gms")
    weight_passing_sample = fields.Integer(string="Weight of Passing sample in 1.70 mm IS sieve in gms")
    weight_retain_sample = fields.Integer(string="Weight of Retain sample in 1.70 mm IS sieve in gms",compute="_compute_weight_retain_sample")
    abrasion_value_percentage = fields.Float(string="Abrasion Value (in %)",compute="_compute_sample_weight")


    @api.depends('total_weight_sample', 'weight_passing_sample')
    def _compute_weight_retain_sample(self):
        for line in self:
            line.weight_retain_sample = line.total_weight_sample - line.weight_passing_sample

    # @api.depends('total_weight_sample')
    # def _compute_sample_weight(self):
    #     for line in self:
    #         # Your computation logic for abrasion_value_percentage here
    #         pass


    @api.depends('total_weight_sample', 'weight_passing_sample')
    def _compute_sample_weight(self):
        for line in self:
            if line.total_weight_sample != 0:
                line.abrasion_value_percentage = (line.weight_passing_sample / line.total_weight_sample) * 100
            else:
                line.abrasion_value_percentage = 0.0


    # @api.model
    # def create(self, vals):
    #     # Set the serial_no based on the existing records for the same parent
    #     if vals.get('parent_id'):
    #         existing_records = self.search([('parent_id', '=', vals['parent_id'])])
    #         if existing_records:
    #             max_serial_no = max(existing_records.mapped('sr_no'))
    #             vals['sr_no'] = max_serial_no + 1

    #     return super(AbrasionValueCoarseAggregateLine, self).create(vals)

    # def _reorder_serial_numbers(self):
    #     # Reorder the serial numbers based on the positions of the records in child_lines
    #     records = self.sorted('id')
    #     for index, record in enumerate(records):
    #         record.sr_no = index + 1

