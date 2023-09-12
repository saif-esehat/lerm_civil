from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta
import math



class Soil(models.Model):
    _name = "mechanical.soil"
    _inherit = "lerm.eln"
    _rec_name = "name_soil"


    name_soil = fields.Char("Name",default="Soil")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    tests = fields.Many2many("mechanical.soil.test",string="Tests")

    # CBR

    soil_name = fields.Char("Name",default="California Bearing Ratio")
    soil_visible = fields.Boolean("California Bearing Ratio Visible",compute="_compute_visible")
    job_no_soil = fields.Char(string="Job No")
    material_soil = fields.Char(String="Material")
    start_date_soil = fields.Date("Start Date")
    end_date_soil = fields.Date("End Date")
    soil_table = fields.One2many('mechanical.soil.cbr.line','parent_id',string="CBR")

    # FSI

    fsi_name = fields.Char("Name",default="Free Swell Index")
    fsi_visible = fields.Boolean("Free Swell Index Visible",compute="_compute_visible")
    job_no_fsi = fields.Char(string="Job No")
    material_fsi = fields.Char(String="Material")
    start_date_fsi = fields.Date("Start Date")
    end_date_fsi = fields.Date("End Date")
    fsi_table = fields.One2many('mechanical.free.swell.index.line','parent_id',string="FSI")

    # Sieve Analysis
    sieve_name = fields.Char("Name",default="Sieve Analysis")
    sieve_visible = fields.Boolean("Sieve Analysis Visible",compute="_compute_visible")
    job_no_sieve = fields.Char(string="Job No")
    material_sieve = fields.Char(String="Material")
    start_date_sieve = fields.Date("Start Date")
    end_date_sieve = fields.Date("End Date")
    child_lines = fields.One2many('mechanical.soil.sieve.analysis.line','parent_id',string="Sieve Analysis")
    total = fields.Integer(string="Total",compute="_compute_total")
    # cumulative = fields.Float(string="Cumulative",compute="_compute_cumulative")


    def calculate(self): 
        for record in self:
            for line in record.child_lines:
                print("Rows",str(line.percent_retained))
                previous_line = line.serial_no - 1
                if previous_line == 0:
                    line.write({'cumulative_retained': line.percent_retained})
                    line.write({'passing_percent': 100})

                else:
                    previous_line_record = self.env['mechanical.soil.sieve.analysis.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': previous_line_record + line.percent_retained})
                    line.write({'passing_percent': 100-(previous_line_record + line.percent_retained)})
                    print("Previous Cumulative",previous_line_record)
                    

                
    

   
    @api.depends('child_lines.wt_retained')
    def _compute_total(self):
        for record in self:
            print("recordd",record)
            record.total = sum(record.child_lines.mapped('wt_retained'))

    # @api.onchange('child_lines.wt_retained')
    # def _compute_cumulative(self):
    #     for record in self:
    #         record.total = sum(record.child_lines.mapped('wt_retained'))


    @api.onchange('total')
    def _onchange_total(self):
        for line in self.child_lines:
            line._compute_percent_retained()
            # line._compute_cumulative_retained()


    # Havy Compaction-MDD
    heavy_name = fields.Char("Name",default="Heavy Compaction-MDD")
    heavy_visible = fields.Boolean("Heavy Compaction-MDD Visible",compute="_compute_visible")
    job_no_heavy = fields.Char(string="Job No")
    material_heavy = fields.Char(String="Material")
    start_date_heavy = fields.Date("Start Date")
    end_date_heavy = fields.Date("End Date")
    heavy_table = fields.One2many('mechanical.heavy.compaction.line','parent_id',string="Heavy Compaction")
    wt_of_modul = fields.Integer(string="Weight of Mould in gm")
    vl_of_modul = fields.Integer(string="Volume of Mould in cc")

    # Havy Compaction-OMC
    heavy_omc_name = fields.Char("Name",default="Heavy Compaction-OMC")
    heavy_omc_visible = fields.Boolean("Heavy Compaction-OMC Visible",compute="_compute_visible")
    job_no_heavy_omc = fields.Char(string="Job No")
    material_heavy_omc = fields.Char(String="Material")
    start_date_heavy_omc = fields.Date("Start Date")
    end_date_heavy_omc = fields.Date("End Date")
    heavy_omc_table = fields.One2many('mechanical.heavy.omc.compaction.line','parent_id',string="Heavy Compaction")
    wt_of_modul_heavy_omc = fields.Integer(string="Weight of Mould in gm")
    vl_of_modul_heavy_omc = fields.Integer(string="Volume of Mould in cc")

   
     # Light Compaction-OMC
    light_omc_name = fields.Char("Name",default="Light Compaction-OMC")
    light_omc_visible = fields.Boolean("Light Compaction-OMC Visible",compute="_compute_visible")
    job_no_light_omc = fields.Char(string="Job No")
    material_light_omc = fields.Char(String="Material")
    start_date_light_omc = fields.Date("Start Date")
    end_date_light_omc = fields.Date("End Date")
    light_omc_table = fields.One2many('mechanical.light.omc.compaction.line','parent_id',string="Heavy Compaction")
    wt_of_modul_light_omc = fields.Integer(string="Weight of Mould in gm")
    vl_of_modul_light_omc = fields.Integer(string="Volume of Mould in cc")


    # Light Compaction-MDD
    light_mdd_name = fields.Char("Name",default="Light Compaction-MDD")
    light_mdd_visible = fields.Boolean("Light Compaction-MDD Visible",compute="_compute_visible")
    job_no_light_mdd = fields.Char(string="Job No")
    material_light_mdd = fields.Char(String="Material")
    start_date_light_mdd = fields.Date("Start Date")
    end_date_light_mdd = fields.Date("End Date")
    light_mdd_table = fields.One2many('mechanical.light.mdd.compaction.line','parent_id',string="Heavy Compaction")
    wt_of_modul_light_mdd = fields.Integer(string="Weight of Mould in gm")
    vl_of_modul_light_mdd = fields.Integer(string="Volume of Mould in cc")


    # Liquid Limit
    liquid_limit_name = fields.Char("Name",default="Liquid Limit")
    liquid_limit_visible = fields.Boolean("Liquid Limit Visible",compute="_compute_visible")
    job_no_liquid_limit = fields.Char(string="Job No")
    material_liquid_limit = fields.Char(String="Material")
    start_date_liquid_limit = fields.Date("Start Date")
    end_date_liquid_limit = fields.Date("End Date")
    child_liness = fields.One2many('mechanical.liquid.limit.line','parent_id',string="Liquid Limit")

    liquid_limit = fields.Float('Liquid Limit')

    # def calculate_result(self):

    are_child_lines_filled = fields.Boolean(compute='_compute_are_child_lines_filled',string='child lines',store=False)

    @api.depends('child_liness.moisture', 'child_liness.mass_of_dry_sample')  # Replace with actual field names
    def _compute_are_child_lines_filled(self):
        for record in self:
            all_lines_filled = all(line.moisture and line.mass_of_dry_sample for line in record.child_liness)
            record.are_child_lines_filled = all_lines_filled

       

    def liquid_calculation(self):
        print('<<<<<<<<<<<<')
        for record in self:
            data = self.child_liness
           
            result = 0  # Initialize result before the loop
            print(data, 'data')
            container2Moisture = data[1].moisture
            container1Moisture = data[0].moisture
            container3Moisture = data[2].moisture
            cont2blow = data[1].blwo_no
            cont3blow = data[2].blwo_no
            result = (container2Moisture * 100 - ((container2Moisture - container3Moisture) * 100 * (25 - cont2blow)) / (cont3blow - cont2blow)) / 100
            print(result, 'final result')
        self.write({'liquid_limit': result})

    
     # Plastic Limit
    plastic_limit_name = fields.Char("Name",default="Plastic Limit")
    plastic_limit_visible = fields.Boolean("Plastic Limit Visible",compute="_compute_visible")
    job_no_plastic_limit = fields.Char(string="Job No")
    material_plastic_limit = fields.Char(String="Material")
    start_date_plastic_limit = fields.Date("Start Date")
    end_date_plastic_limit = fields.Date("End Date")

    plastic_limit_table = fields.One2many('mechanical.plasticl.limit.line','parent_id',string="Parameter")

    plastic_limit = fields.Float(string="Average of % Moisture", compute="_compute_plastic_limit")
    plasticity_index = fields.Float(string="Plasticity Index", compute="_compute_plasticity_index")


    @api.depends('plastic_limit_table.moisture')
    def _compute_plastic_limit(self):
        for record in self:
            total_moisture = sum(record.plastic_limit_table.mapped('moisture'))
            record.plastic_limit = total_moisture / len(record.plastic_limit_table) if record.plastic_limit_table else 0.0

    @api.depends('plastic_limit')
    def _compute_plasticity_index(self):
        for record in self:
            record.plasticity_index = 46.14 - record.plastic_limit



     # Dry Density by Sand Replacement method
    dry_density_name = fields.Char("Name",default="Dry Density by Sand Replacement method")
    dry_density_visible = fields.Boolean("Dry Density by Sand Replacement method Visible",compute="_compute_visible")
    job_no_dry_density = fields.Char(string="Job No")
    material_dry_density = fields.Char(String="Material")
    start_date_dry_density = fields.Date("Start Date")
    end_date_dry_density = fields.Date("End Date")


    mmd = fields.Float(string="MMD gm/cc", default=1.72)
    omc = fields.Float(string="OMC gm/cc", default=8.32)

    determination_no = fields.Integer(string="Determination No")
    wt_of_sample = fields.Integer(string="Weight of sample gm")
    water_of_sample = fields.Integer(string="Water content of sample RMM")
    wt_of_before_cylinder = fields.Integer(string="Weight of sand + Cylinder before pouring gm")
    wt_of_after_cylinder = fields.Integer(string="Weight of sand + Cylinder after pouring gm")
    wt_of_sand_cone = fields.Integer(string="Weight of sand in cone gm")
    wt_of_sand_hole = fields.Integer(string="Weight of sand in hole gm", compute="_compute_sand_hole")
    density_of_sand = fields.Float(string="Density of sand gm/cc")
    volume_of_hole = fields.Integer(string="Volume of hole cc", compute="_compute_volume_of_hole")
    bulk_density_of_sample = fields.Float(string="Bulk Density of sample gm/cc",compute="_compute_bulk_density")
    dry_density_of_sample = fields.Float(string="Dry Density of sample",compute="_compute_dry_density")
    degree_of_compaction = fields.Float(string="Degree of Compaction %",compute="_compute_degree_of_compaction")



    @api.depends('wt_of_before_cylinder','wt_of_after_cylinder','wt_of_sand_cone')
    def _compute_sand_hole(self):
        for record in self:
            record.wt_of_sand_hole = record.wt_of_before_cylinder - record.wt_of_after_cylinder - record.wt_of_sand_cone

    @api.depends('wt_of_sand_hole', 'density_of_sand')
    def _compute_volume_of_hole(self):
        for record in self:
            if record.density_of_sand != 0:  # Avoid division by zero
                record.volume_of_hole = record.density_of_sand / record.wt_of_sand_hole
            else:
                record.volume_of_hole = 0.0


    @api.depends('wt_of_sample', 'volume_of_hole')
    def _compute_bulk_density(self):
        for record in self:
            if record.volume_of_hole != 0:  # Avoid division by zero
                record.bulk_density_of_sample = record.wt_of_sample / record.volume_of_hole
            else:
                record.bulk_density_of_sample = 0.0

    @api.depends('bulk_density_of_sample', 'water_of_sample')
    def _compute_dry_density(self):
        for record in self:
            if record.water_of_sample + 100 != 0:  # Avoid division by zero
                record.dry_density_of_sample = (100 * record.bulk_density_of_sample) / (record.water_of_sample + 100)
            else:
                record.dry_density_of_sample = 0.0

    @api.depends('dry_density_of_sample', 'mmd')
    def _compute_degree_of_compaction(self):
        for record in self:
            if record.mmd != 0:  # Avoid division by zero
                record.degree_of_compaction = (record.dry_density_of_sample / record.mmd) * 100
            else:
                record.degree_of_compaction = 0.0



    # Moisture Content

    moisture_content_name = fields.Char("Name",default="Moisture Content")
    moisture_content_visible = fields.Boolean("Moisture Content Visible",compute="_compute_visible")
    job_no_moisture_content = fields.Char(string="Job No")
    material_moisture_content = fields.Char(String="Material")
    start_date_moisture_content = fields.Date("Start Date")
    end_date_moisture_content = fields.Date("End Date")

    moisture_content_table = fields.One2many('mechanical.moisture.content.line','parent_id',string="Parameter")
    average_block = fields.Float(string="Average",compute="_compute_average_moisture_content")



    @api.depends('moisture_content_table.moisture_content')
    def _compute_average_moisture_content(self):
        for record in self:
            total_moisture_content = sum(record.moisture_content_table.mapped('moisture_content'))
            num_lines = len(record.moisture_content_table)
            record.average_block = total_moisture_content / num_lines if num_lines else 0.0


																	

    











     ### Compute Visible
    @api.depends('tests')
    def _compute_visible(self):
        cbr_test = self.env['mechanical.soil.test'].search([('name', '=', 'California Bearing Ratio')])
        fsi_test = self.env['mechanical.soil.test'].search([('name', '=', 'Free Swell Index')])
        sieve_test = self.env['mechanical.soil.test'].search([('name', '=', 'Sieve Analysis')])
        heavy_test = self.env['mechanical.soil.test'].search([('name', '=', 'Heavy Compaction-MDD')])
        heavy_omc_test = self.env['mechanical.soil.test'].search([('name', '=', 'Heavy Compaction-OMC')])
        light_omc_test = self.env['mechanical.soil.test'].search([('name', '=', 'Light Compaction-OMC')])
        light_mdd_test = self.env['mechanical.soil.test'].search([('name', '=', 'Light Compaction-MDD')])
        liquid_limit_test = self.env['mechanical.soil.test'].search([('name', '=', 'Liquid Limit')])
        plastic_limit_test = self.env['mechanical.soil.test'].search([('name', '=', 'Plastic Limit')])
        dry_density_test = self.env['mechanical.soil.test'].search([('name', '=', 'Dry Density by Sand Replacement method')])
        moisture_content_test = self.env['mechanical.soil.test'].search([('name', '=', 'Moisture Content')])
 
        for record in self:
            record.soil_visible = False
            record.fsi_visible  = False  
            record.sieve_visible = False
            record.heavy_visible = False
            record.heavy_omc_visible = False
            record.light_omc_visible = False
            record.light_mdd_visible = False
            record.liquid_limit_visible = False
            record.plastic_limit_visible = False
            record.dry_density_visible = False
            record.moisture_content_visible = False

            if cbr_test in record.tests:
                record.soil_visible = True

            if fsi_test in record.tests:
                record.fsi_visible = True
            #     record.setting_time_visible  = True
            if sieve_test in record.tests:
                record.sieve_visible = True
            if heavy_test in record.tests:
                record.heavy_visible = True
            if heavy_omc_test in record.tests:
                 record.heavy_omc_visible = True
            if light_omc_test in record.tests:
                 record.light_omc_visible = True
            if light_mdd_test in record.tests:
                 record.light_mdd_visible = True
            if liquid_limit_test in record.tests:
                record.liquid_limit_visible = True
            if plastic_limit_test in record.tests:
                record.plastic_limit_visible = True
           
            if dry_density_test in record.tests:
                record.dry_density_visible = True
           
            if moisture_content_test in record.tests:
                record.moisture_content_visible = True
            # if fineness_blaine in record.tests:
            #     record.fineness_blaine_visible = True
               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(Soil, self).create(vals)
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
        record = self.env['mechanical.soil'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values




class SoilTest(models.Model):
    _name = "mechanical.soil.test"
    _rec_name = "name"
    name = fields.Char("Name")


class SoilCBRLine(models.Model):
    _name = "mechanical.soil.cbr.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    penetration = fields.Float(string="Penetration in mm")
    proving_reading = fields.Float(string="Proving Ring Reading")
    load = fields.Float(string="Load in Kg", compute="_compute_load")


    @api.depends('proving_reading')
    def _compute_load(self):
        for record in self:
            record.load = record.proving_reading * 6.96


class FreeSwellIndexLine(models.Model):
    _name = "mechanical.free.swell.index.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    wt_sample = fields.Float(string="Mass of wet sample")
    dry_sample = fields.Float(string="Volume of dry sample in cc")
    v_sample_kerosin = fields.Float(string="Volume of sample after immersing in kerosin for 24 Hrs. in cc, V1")
    v_sample_water = fields.Float(string="Volume of sample after immersing in water for 24 Hrs. in cc, V2")
    increase_volume = fields.Float(string="Increase in Volume, (V2-V1) in cc", compute="_compute_volume")
    fsi = fields.Float(string="% FSI = (V2-V1)/V1 x 100", compute="_compute_fsi")


    @api.depends('v_sample_water', 'v_sample_kerosin')
    def _compute_volume(self):
        for record in self:
            record.increase_volume = record.v_sample_water - record.v_sample_kerosin


    @api.depends('v_sample_water', 'v_sample_kerosin')
    def _compute_volume(self):
        for record in self:
            record.increase_volume = record.v_sample_water - record.v_sample_kerosin

    @api.depends('increase_volume', 'v_sample_kerosin')
    def _compute_fsi(self):
        for record in self:
            if record.v_sample_kerosin != 0:
                record.fsi = (record.increase_volume / record.v_sample_kerosin) * 100
            else:
                record.fsi = 0.0

class SoilSieveAnalysisLine(models.Model):
    _name = "mechanical.soil.sieve.analysis.line"
    parent_id = fields.Many2one('mechanical.soil', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", compute="_compute_cumulative_retained", store=True)
    passing_percent = fields.Float(string="Passing %")

    # @api.onchange('cumulative_retained')
    # def _compute_passing_percent(self):
    #     for record in self:
    #         record.passing_percent = 100 - record.cumulative_retained


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
            parent_id.child_lines._reorder_serial_numbers()

        return res

    
   

    @api.depends('wt_retained', 'parent_id.total')
    def _compute_percent_retained(self):
        for record in self:
            try:
                record.percent_retained = record.wt_retained / self.parent_id.total * 100
            except ZeroDivisionError:
                record.percent_retained = 0


    @api.depends('parent_id.child_lines.cumulative_retained')
    def _compute_cum_retained(self):
        # self.get_previous_record()
        self.cumulative_retained=0
        # sorted_lines = self.sorted(lambda r: r.id)
        # cumulative_retained = 0.0
        # for line in sorted_lines:
        #     line.cumulative_retained = cumulative_retained + line.percent_retained
        #     cumulative_retained = line.cumulative_retained


    def get_previous_record(self):
        for record in self:
            # import wdb; wdb.set_trace()
            sorted_lines = sorted(record.parent_id.child_lines, key=lambda r: r.id)
            # index = sorted_lines.index(record)
            # print("Working")


class HEAVYCOMPACTIONLINE(models.Model):
    _name = "mechanical.heavy.compaction.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    determination_no = fields.Float(string="Determination No")
    wt_of_modul_compact = fields.Integer(string="Weight of Mould + Compacted sample in gm")
    wt_of_compact = fields.Integer(string="Weight of compacted sample in gm", compute="_compute_wt_of_compact")
    bulk_density = fields.Float(string="Bulk Density of sample in gm/cc", compute="_compute_bulk_density")
    container_no = fields.Integer(string="Container No")
    wt_of_container = fields.Float(string="Weight of Container in gm")
    wt_of_container_wet = fields.Float(string="Weight of Container + wet sample in gm")
    wt_of_container_dry = fields.Float(string="Weight of Container + dry sample in gm")
    wt_of_dry_sample = fields.Float(string="Weight of dry sample in gm", compute="_compute_wt_of_dry_sample")
    wt_of_moisture = fields.Float(string="Weight of moisture in gm", compute="_compute_wt_of_moisture")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")
    dry_density = fields.Float(string="Dry density in gm/cc", compute="_compute_dry_density")


    @api.depends('wt_of_modul_compact', 'parent_id.wt_of_modul')
    def _compute_wt_of_compact(self):
        for line in self:
            line.wt_of_compact = line.wt_of_modul_compact - line.parent_id.wt_of_modul



    @api.depends('wt_of_compact', 'parent_id.vl_of_modul')
    def _compute_bulk_density(self):
        for line in self:
            if line.parent_id.vl_of_modul != 0:
                line.bulk_density = line.wt_of_compact / line.parent_id.vl_of_modul
            else:
                line.bulk_density = 0.0


    @api.depends('wt_of_container_dry', 'wt_of_container')
    def _compute_wt_of_dry_sample(self):
        for line in self:
            line.wt_of_dry_sample = line.wt_of_container_dry - line.wt_of_container


    @api.depends('wt_of_container_wet', 'wt_of_container_dry')
    def _compute_wt_of_moisture(self):
        for line in self:
            line.wt_of_moisture = line.wt_of_container_wet - line.wt_of_container_dry


    @api.depends('wt_of_moisture', 'wt_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.wt_of_dry_sample != 0:
                line.moisture = line.wt_of_moisture / line.wt_of_dry_sample * 100
            else:
                line.moisture = 0.0


    @api.depends('bulk_density', 'moisture')
    def _compute_dry_density(self):
        for line in self:
            line.dry_density = (100 * line.bulk_density) / (100 + line.moisture)


class HEAVYOMCCOMPACTIONLINE(models.Model):
    _name = "mechanical.heavy.omc.compaction.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    determination_no = fields.Float(string="Determination No")
    wt_of_modul_compact = fields.Integer(string="Weight of Mould + Compacted sample in gm")
    wt_of_compact = fields.Integer(string="Weight of compacted sample in gm", compute="_compute_wt_of_compact")
    bulk_density = fields.Float(string="Bulk Density of sample in gm/cc", compute="_compute_bulk_density")
    container_no = fields.Integer(string="Container No")
    wt_of_container = fields.Float(string="Weight of Container in gm")
    wt_of_container_wet = fields.Float(string="Weight of Container + wet sample in gm")
    wt_of_container_dry = fields.Float(string="Weight of Container + dry sample in gm")
    wt_of_dry_sample = fields.Float(string="Weight of dry sample in gm", compute="_compute_wt_of_dry_sample")
    wt_of_moisture = fields.Float(string="Weight of moisture in gm", compute="_compute_wt_of_moisture")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")
    dry_density = fields.Float(string="Dry density in gm/cc", compute="_compute_dry_density")


    @api.depends('wt_of_modul_compact', 'parent_id.wt_of_modul')
    def _compute_wt_of_compact(self):
        for line in self:
            line.wt_of_compact = line.wt_of_modul_compact - line.parent_id.wt_of_modul



    @api.depends('wt_of_compact', 'parent_id.vl_of_modul')
    def _compute_bulk_density(self):
        for line in self:
            if line.parent_id.vl_of_modul != 0:
                line.bulk_density = line.wt_of_compact / line.parent_id.vl_of_modul
            else:
                line.bulk_density = 0.0


    @api.depends('wt_of_container_dry', 'wt_of_container')
    def _compute_wt_of_dry_sample(self):
        for line in self:
            line.wt_of_dry_sample = line.wt_of_container_dry - line.wt_of_container


    @api.depends('wt_of_container_wet', 'wt_of_container_dry')
    def _compute_wt_of_moisture(self):
        for line in self:
            line.wt_of_moisture = line.wt_of_container_wet - line.wt_of_container_dry


    @api.depends('wt_of_moisture', 'wt_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.wt_of_dry_sample != 0:
                line.moisture = line.wt_of_moisture / line.wt_of_dry_sample * 100
            else:
                line.moisture = 0.0


    @api.depends('bulk_density', 'moisture')
    def _compute_dry_density(self):
        for line in self:
            line.dry_density = (100 * line.bulk_density) / (100 + line.moisture)

class LIGHTOMCCOMPACTIONLINE(models.Model):
    _name = "mechanical.light.omc.compaction.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    determination_no = fields.Float(string="Determination No")
    wt_of_modul_compact = fields.Integer(string="Weight of Mould + Compacted sample in gm")
    wt_of_compact = fields.Integer(string="Weight of compacted sample in gm", compute="_compute_wt_of_compact")
    bulk_density = fields.Float(string="Bulk Density of sample in gm/cc", compute="_compute_bulk_density")
    container_no = fields.Integer(string="Container No")
    wt_of_container = fields.Float(string="Weight of Container in gm")
    wt_of_container_wet = fields.Float(string="Weight of Container + wet sample in gm")
    wt_of_container_dry = fields.Float(string="Weight of Container + dry sample in gm")
    wt_of_dry_sample = fields.Float(string="Weight of dry sample in gm", compute="_compute_wt_of_dry_sample")
    wt_of_moisture = fields.Float(string="Weight of moisture in gm", compute="_compute_wt_of_moisture")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")
    dry_density = fields.Float(string="Dry density in gm/cc", compute="_compute_dry_density")


    @api.depends('wt_of_modul_compact', 'parent_id.wt_of_modul')
    def _compute_wt_of_compact(self):
        for line in self:
            line.wt_of_compact = line.wt_of_modul_compact - line.parent_id.wt_of_modul



    @api.depends('wt_of_compact', 'parent_id.vl_of_modul')
    def _compute_bulk_density(self):
        for line in self:
            if line.parent_id.vl_of_modul != 0:
                line.bulk_density = line.wt_of_compact / line.parent_id.vl_of_modul
            else:
                line.bulk_density = 0.0


    @api.depends('wt_of_container_dry', 'wt_of_container')
    def _compute_wt_of_dry_sample(self):
        for line in self:
            line.wt_of_dry_sample = line.wt_of_container_dry - line.wt_of_container


    @api.depends('wt_of_container_wet', 'wt_of_container_dry')
    def _compute_wt_of_moisture(self):
        for line in self:
            line.wt_of_moisture = line.wt_of_container_wet - line.wt_of_container_dry


    @api.depends('wt_of_moisture', 'wt_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.wt_of_dry_sample != 0:
                line.moisture = line.wt_of_moisture / line.wt_of_dry_sample * 100
            else:
                line.moisture = 0.0


    @api.depends('bulk_density', 'moisture')
    def _compute_dry_density(self):
        for line in self:
            line.dry_density = (100 * line.bulk_density) / (100 + line.moisture)


class LIGHTMDDCOMPACTIONLINE(models.Model):
    _name = "mechanical.light.mdd.compaction.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")

    determination_no = fields.Float(string="Determination No")
    wt_of_modul_compact = fields.Integer(string="Weight of Mould + Compacted sample in gm")
    wt_of_compact = fields.Integer(string="Weight of compacted sample in gm", compute="_compute_wt_of_compact")
    bulk_density = fields.Float(string="Bulk Density of sample in gm/cc", compute="_compute_bulk_density")
    container_no = fields.Integer(string="Container No")
    wt_of_container = fields.Float(string="Weight of Container in gm")
    wt_of_container_wet = fields.Float(string="Weight of Container + wet sample in gm")
    wt_of_container_dry = fields.Float(string="Weight of Container + dry sample in gm")
    wt_of_dry_sample = fields.Float(string="Weight of dry sample in gm", compute="_compute_wt_of_dry_sample")
    wt_of_moisture = fields.Float(string="Weight of moisture in gm", compute="_compute_wt_of_moisture")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")
    dry_density = fields.Float(string="Dry density in gm/cc", compute="_compute_dry_density")


    @api.depends('wt_of_modul_compact', 'parent_id.wt_of_modul')
    def _compute_wt_of_compact(self):
        for line in self:
            line.wt_of_compact = line.wt_of_modul_compact - line.parent_id.wt_of_modul



    @api.depends('wt_of_compact', 'parent_id.vl_of_modul')
    def _compute_bulk_density(self):
        for line in self:
            if line.parent_id.vl_of_modul != 0:
                line.bulk_density = line.wt_of_compact / line.parent_id.vl_of_modul
            else:
                line.bulk_density = 0.0


    @api.depends('wt_of_container_dry', 'wt_of_container')
    def _compute_wt_of_dry_sample(self):
        for line in self:
            line.wt_of_dry_sample = line.wt_of_container_dry - line.wt_of_container


    @api.depends('wt_of_container_wet', 'wt_of_container_dry')
    def _compute_wt_of_moisture(self):
        for line in self:
            line.wt_of_moisture = line.wt_of_container_wet - line.wt_of_container_dry


    @api.depends('wt_of_moisture', 'wt_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.wt_of_dry_sample != 0:
                line.moisture = line.wt_of_moisture / line.wt_of_dry_sample * 100
            else:
                line.moisture = 0.0


    @api.depends('bulk_density', 'moisture')
    def _compute_dry_density(self):
        for line in self:
            line.dry_density = (100 * line.bulk_density) / (100 + line.moisture)



class LIQUIDLIMITLINE(models.Model):
    _name = "mechanical.liquid.limit.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")



    container_no = fields.Integer(string="Container No")   
    blwo_no = fields.Integer(string="No.of Blows")
    mass_of_wet = fields.Float(string="Mass of wet sample+container (M1) in gms")
    mass_of_dry = fields.Float(string="Mass of dry sample+container (M2) in gms")
    mass_of_container = fields.Float(string="Mass of container (M3) in gms")
    mass_of_moisture = fields.Float(string="Mass of Moisture (M1-M2) in gms", compute="_compute_mass_of_moisture")
    mass_of_dry_sample = fields.Float(string="Mass of dry sample (M2-M3) in gms", compute="_compute_mass_of_dry_sample")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")

   


    @api.depends('mass_of_wet', 'mass_of_dry')
    def _compute_mass_of_moisture(self):
        for line in self:
            line.mass_of_moisture = line.mass_of_wet - line.mass_of_dry


    @api.depends('mass_of_dry', 'mass_of_container')
    def _compute_mass_of_dry_sample(self):
        for line in self:
            line.mass_of_dry_sample = line.mass_of_dry - line.mass_of_container


    @api.depends('mass_of_moisture', 'mass_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.mass_of_dry_sample != 0:
                line.moisture = line.mass_of_moisture / line.mass_of_dry_sample * 100
            else:
                line.moisture = 0.0


class PLASTICLIMITLINE(models.Model):
    _name = "mechanical.plasticl.limit.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")



    container_no = fields.Integer(string="Container No")   
    mass_of_wet = fields.Float(string="Mass of wet sample+container (M1) in gms")
    mass_of_dry = fields.Float(string="Mass of dry sample+container (M2) in gms")
    mass_of_container = fields.Float(string="Mass of container (M3) in gms")
    mass_of_moisture = fields.Float(string="Mass of Moisture (M1-M2) in gms", compute="_compute_mass_of_moisture")
    mass_of_dry_sample = fields.Float(string="Mass of dry sample (M2-M3) in gms", compute="_compute_mass_of_dry_sample")
    moisture = fields.Float(string="% Moisture", compute="_compute_moisture")



    @api.depends('mass_of_wet', 'mass_of_dry')
    def _compute_mass_of_moisture(self):
        for line in self:
            line.mass_of_moisture = line.mass_of_wet - line.mass_of_dry


    @api.depends('mass_of_dry', 'mass_of_container')
    def _compute_mass_of_dry_sample(self):
        for line in self:
            line.mass_of_dry_sample = line.mass_of_dry - line.mass_of_container


    @api.depends('mass_of_moisture', 'mass_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.mass_of_dry_sample != 0:
                line.moisture = line.mass_of_moisture / line.mass_of_dry_sample * 100
            else:
                line.moisture = 0.0


class MoistureContentLine(models.Model):
    _name = "mechanical.moisture.content.line"
    parent_id = fields.Many2one('mechanical.soil',string="Parent Id")
   
    sr_no = fields.Integer(string="SR NO.", readonly=True, copy=False, default=1)
    wt_of_sample = fields.Integer(string="Weight of sample W1 in gm")
    oven_dry_wt = fields.Integer(string="Oven dry Weight of sample W in gm")
    moisture_content = fields.Float(string="% Moisture Content",compute="_compute_moisture_content")


    @api.depends('wt_of_sample', 'oven_dry_wt')
    def _compute_moisture_content(self):
        for record in self:
            if record.oven_dry_wt != 0:
                record.moisture_content = ((record.wt_of_sample - record.oven_dry_wt) / record.oven_dry_wt) * 100
            else:
                record.moisture_content = 0.0

    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(MoistureContentLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1









        

