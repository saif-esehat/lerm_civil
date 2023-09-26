from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta
import math



class FineAggregate(models.Model):
    _name = "mechanical.fine.aggregate"
    _inherit = "lerm.eln"
    _rec_name = "name_aggregate"


    name_aggregate = fields.Char("Name",default="Fine Aggregate")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    tests = fields.Many2many("mechanical.fine.aggregate.test",string="Tests")

    # Loose Bulk Density (LBD)

    loose_bulk_name = fields.Char("Name",default="Loose Bulk Density (LBD)")
    loose_bulk_visible = fields.Boolean("Loose Bulk Density (LBD) Visible",compute="_compute_visible")

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


     # Rodded Bulk Density (RBD)
    rodded_bulk_name = fields.Char("Name",default="Rodded Bulk Density (RBD)")
    rodded_bulk_visible = fields.Boolean("Loose Bulk Density (LBD) Visible",compute="_compute_visible")

    weight_empty_bucket1 = fields.Float(string="Weight of Empty Bucket in kg")
    volume_of_bucket1 = fields.Float(string="Volume of Bucket in cubic meter")
    sample_plus_bucket1 = fields.Float(string="[Sample Weight + Bucket  Weight] in kg")
    sample_weight1 = fields.Float(string="Sample Weight in kg",compute="_compute_sample_weight1")
    rodded_bulk_density1 = fields.Float(string="Rodded Bulk Density in kg per cubic meter",compute="_compute_rodded_bulk_density")


    @api.depends('sample_plus_bucket1', 'weight_empty_bucket1')
    def _compute_sample_weight1(self):
        for record in self:
            record.sample_weight1 = record.sample_plus_bucket1 - record.weight_empty_bucket1


    @api.depends('sample_weight1', 'volume_of_bucket1')
    def _compute_rodded_bulk_density(self):
        for record in self:
            if record.volume_of_bucket1:
                record.rodded_bulk_density1 = record.sample_weight1 / record.volume_of_bucket1
            else:
                record.rodded_bulk_density1 = 0.0


 
    # Specific Gravity

    specific_gravity_name = fields.Char("Name",default="Specific Gravity")
    specific_gravity_visible = fields.Boolean("Specific Gravity Visible",compute="_compute_visible")

    wt_of_empty_pycnometer = fields.Integer(string="Weight of empty Pycnometer in gms")
    wt_of_pycnometer = fields.Integer(string="Weight of Pycnometer with full of water in gms")
    wt_of_pycnometer_surface_dry = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate in gms")
    wt_of_pycnometer_surface_dry_water = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate + Water in gms")
    wt_of_saturated_surface_dry = fields.Integer(string="Weight of Saturated surface dry Aggregate in gms",compute='_compute_wt_of_saturated_surface_dry')
    wt_of_oven_dried = fields.Integer(string="Weight of Oven dried Aggregate in gms")
    volume_of_water = fields.Integer(string="Volume of water displaced by saturated surface dry aggregate",compute="_compute_volume_of_water")
    specific_gravity = fields.Float(string="SPECIFIC GRAVITY", compute="_compute_specific_gravity")
    water_absorption = fields.Float(string="Water Absorption %",compute="_compute_water_absorption")



    @api.depends('wt_of_pycnometer_surface_dry', 'wt_of_empty_pycnometer')
    def _compute_wt_of_saturated_surface_dry(self):
        for line in self:
            line.wt_of_saturated_surface_dry = line.wt_of_pycnometer_surface_dry - line.wt_of_empty_pycnometer


    @api.depends('wt_of_pycnometer', 'wt_of_empty_pycnometer', 'wt_of_pycnometer_surface_dry', 'wt_of_pycnometer_surface_dry_water')
    def _compute_volume_of_water(self):
        for line in self:
            volume_of_water = (line.wt_of_pycnometer - line.wt_of_empty_pycnometer) - (line.wt_of_pycnometer_surface_dry_water - line.wt_of_pycnometer_surface_dry)
            line.volume_of_water = volume_of_water

    @api.depends('wt_of_oven_dried', 'volume_of_water')
    def _compute_specific_gravity(self):
        for line in self:
            if line.volume_of_water:
                line.specific_gravity = line.wt_of_oven_dried / line.volume_of_water
            else:
                line.specific_gravity = 0.0


    @api.depends('wt_of_saturated_surface_dry', 'wt_of_oven_dried')
    def _compute_water_absorption(self):
        for line in self:
            if line.wt_of_oven_dried:
                line.water_absorption = (line.wt_of_saturated_surface_dry - line.wt_of_oven_dried) / line.wt_of_oven_dried * 100
            else:
                line.water_absorption = 0.0



    # Water Absorption

    water_absorption_name = fields.Char("Name",default="Water Absorption")
    water_absorption_visible = fields.Boolean("Water Absorption Visible",compute="_compute_visible")

    wt_of_empty_pycnometer1 = fields.Integer(string="Weight of empty Pycnometer in gms")
    wt_of_pycnometer1 = fields.Integer(string="Weight of Pycnometer with full of water in gms")
    wt_of_pycnometer_surface_dry1 = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate in gms")
    wt_of_pycnometer_surface_dry_water1 = fields.Integer(string="Weight of Pycnometer + Saturated surface dry Aggregate + Water in gms")
    wt_of_saturated_surface_dry1 = fields.Integer(string="Weight of Saturated surface dry Aggregate in gms",compute='_compute_wt_of_saturated_surface_dry1')
    wt_of_oven_dried1 = fields.Integer(string="Weight of Oven dried Aggregate in gms")
    volume_of_water1 = fields.Integer(string="Volume of water displaced by saturated surface dry aggregate",compute="_compute_volume_of_water1")
    specific_gravity1 = fields.Float(string="SPECIFIC GRAVITY", compute="_compute_specific_gravity1")
    water_absorption1 = fields.Float(string="Water Absorption %",compute="_compute_water_absorption1")



    @api.depends('wt_of_pycnometer_surface_dry1', 'wt_of_empty_pycnometer1')
    def _compute_wt_of_saturated_surface_dry1(self):
        for line in self:
            line.wt_of_saturated_surface_dry1 = line.wt_of_pycnometer_surface_dry1 - line.wt_of_empty_pycnometer1


    @api.depends('wt_of_pycnometer1', 'wt_of_empty_pycnometer1', 'wt_of_pycnometer_surface_dry1', 'wt_of_pycnometer_surface_dry_water1')
    def _compute_volume_of_water1(self):
        for line in self:
            volume_of_water1 = (line.wt_of_pycnometer1 - line.wt_of_empty_pycnometer1) - (line.wt_of_pycnometer_surface_dry_water1 - line.wt_of_pycnometer_surface_dry1)
            line.volume_of_water1 = volume_of_water1

    @api.depends('wt_of_oven_dried1', 'volume_of_water1')
    def _compute_specific_gravity1(self):
        for line in self:
            if line.volume_of_water1:
                line.specific_gravity1 = line.wt_of_oven_dried1 / line.volume_of_water1
            else:
                line.specific_gravity1 = 0.0


    @api.depends('wt_of_saturated_surface_dry1', 'wt_of_oven_dried1')
    def _compute_water_absorption1(self):
        for line in self:
            if line.wt_of_oven_dried1:
                line.water_absorption1 = (line.wt_of_saturated_surface_dry1 - line.wt_of_oven_dried1) / line.wt_of_oven_dried1 * 100
            else:
                line.water_absorption1 = 0.0



    # Sieve Analysis 
    sieve_analysis_name = fields.Char("Name",default="Sieve Analysis")
    sieve_visible = fields.Boolean("Sieve Analysis Visible",compute="_compute_visible")

    sieve_analysis_child_lines = fields.One2many('mechanical.sieve.analysis.line','parent_id',string="Parameter")
    total_sieve_analysis = fields.Integer(string="Total",compute="_compute_total_sieve")
    cumulative = fields.Float(string="Cumulative",compute="_compute_cumulative")


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
                    previous_line_record = self.env['mechanical.sieve.analysis.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': previous_line_record + line.percent_retained})
                    line.write({'passing_percent': 100-(previous_line_record + line.percent_retained)})
                    print("Previous Cumulative",previous_line_record)
                    

 

    @api.depends('sieve_analysis_child_lines.wt_retained')
    def _compute_total_sieve(self):
        for record in self:
            print("recordd",record)
            record.total_sieve_analysis = sum(record.sieve_analysis_child_lines.mapped('wt_retained'))






   






    ### Compute Visible
    @api.depends('tests')
    def _compute_visible(self):
        loose_bulk_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Loose Bulk Density (LBD)')])
        rodded_bulk_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Rodded Bulk Density (RBD)')])
        specific_gravity_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Specific Gravity')])
        water_absorption_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Water Absorption')])
        sieve_analysis_test = self.env['mechanical.fine.aggregate.test'].search([('name', '=', 'Sieve Analysis')])
        
        for record in self:
            record.loose_bulk_visible = False
            record.rodded_bulk_visible = False
            record.specific_gravity_visible = False
            record.water_absorption_visible = False
            record.sieve_visible = False
           
            
            if loose_bulk_test in record.tests:
                record.loose_bulk_visible = True

            if rodded_bulk_test in record.tests:
                record.rodded_bulk_visible = True

            if specific_gravity_test in record.tests:
                record.specific_gravity_visible = True

            if water_absorption_test in record.tests:
                record.water_absorption_visible = True

            if sieve_analysis_test in record.tests:
                record.sieve_visible = True

            




               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(FineAggregate, self).create(vals)
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
        record = self.env['mechanical.fine.aggregate'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values




class AggregateFineTest(models.Model):
    _name = "mechanical.fine.aggregate.test"
    _rec_name = "name"
    name = fields.Char("Name")



class SieveAnalysisLine(models.Model):
    _name = "mechanical.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.fine.aggregate', string="Parent Id")
    
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



