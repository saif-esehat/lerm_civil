from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , timedelta
import math
from decimal import Decimal
import matplotlib.pyplot as plt
import io
import base64

class WbmMechanical(models.Model):
    _name = "mechanical.wbm"
    _inherit = "lerm.eln"
    _rec_name = "name"


    name = fields.Char("Name",default="WBM")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(WbmMechanical, self).create(vals)
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
        record = self.env['mechanical.wbm'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values

    @api.depends('eln_ref')
    def _compute_sample_parameters(self):
        
        for record in self:
            records = record.eln_ref.parameters_result.parameter.ids
            record.sample_parameters = records
            print("Records",records)

    @api.depends('eln_ref','sample_parameters')
    def _compute_visible(self):
        for record in self:
            record.dry_gradation_visible = False
            record.water_absorbtion_visible  = False  
            record.elongation_visible = False
            record.flakiness_visible = False
            record.abrasion_visible = False
            record.impact_visible = False
            record.plastic_visible = False
            record.liquid_limit_visible = False
            record.plasticity_index_visible = False
            record.density_relation_visible = False
            record.cbr_visible = False


            for sample in record.sample_parameters:
                print("Samples internal id",sample.internal_id)
                if sample.internal_id == '48b74892-3497-4b7f-819a-a26f25c9848':
                    record.dry_gradation_visible = True
                if sample.internal_id == '247b2e3e-6974-4a89-9a32-2375ca190815':
                    record.water_absorbtion_visible  = True  
                if sample.internal_id == '5429fe61-638d-4e6f-b258-df8a2fc0ea5c':
                    record.elongation_visible = True
                    record.flakiness_visible = True
                if sample.internal_id == '8d2a4700-8125-4f5f-aa7c-f82d1416d5eb':
                    record.flakiness_visible = True
                    record.elongation_visible = True
                if sample.internal_id == 'ded398c1-9ee6-4115-a8db-015d7cb6d5c7':
                    record.abrasion_visible = True
                if sample.internal_id == 'e9e985d1-e282-488c-9dbb-16e9f14b065b':
                    record.impact_visible = True
                if sample.internal_id == '0eff3fc4-d228-42f5-9927-69ca7dadbcee':
                    record.plastic_visible  = True  
                if sample.internal_id == '07bc2253-d02d-43fd-b4a7-dd5a6c6cd36e':
                    record.liquid_limit_visible = True
                if sample.internal_id == '3a650086-0d26-4a6c-8bff-0269dde01d2a':
                    record.liquid_limit_visible = True
                    record.plasticity_index_visible = True
                if sample.internal_id == '9b21943c-b50a-42ec-8489-75e615e51466':
                    record.density_relation_visible = True
                if sample.internal_id == 'e042cfd0-6461-4137-ba6a-381d0229b973':
                    record.cbr_visible = True
                

    # Dry Gradation
    dry_gradation_name = fields.Char(default="Dry Gradation")
    dry_gradation_visible = fields.Boolean(compute="_compute_visible")

    dry_gradation_table = fields.One2many('mech.wbm.dry.gradation.line','parent_id',string="Dry Gradation")
    total_sieve_analysis = fields.Integer(string="Total",compute="_compute_total_sieve")
    


    def calculate_sieve(self): 
        for record in self:
            for line in record.dry_gradation_table:
                print("Rows",str(line.percent_retained))
                previous_line = line.serial_no - 1
                if previous_line == 0:
                    if line.percent_retained == 0:
                        # print("Percent retained 0",line.percent_retained)
                        line.write({'cumulative_retained': round(line.percent_retained + line.percent_retained,2)})
                        line.write({'passing_percent': 100 })
                    else:
                        # print("Percent retained else",line.percent_retained)
                        line.write({'cumulative_retained': round(line.percent_retained + line.percent_retained,2)})
                        line.write({'passing_percent': round(100 -line.percent_retained - line.percent_retained,2)})
                else:
                    previous_line_record = self.env['mech.dry.gradation.line'].search([("serial_no", "=", previous_line),("parent_id","=",self.id)]).cumulative_retained
                    line.write({'cumulative_retained': round(previous_line_record + line.percent_retained,2)})
                    line.write({'passing_percent': round(100-(previous_line_record + line.percent_retained),2)})
                    print("Previous Cumulative",previous_line_record)
                    

    


    @api.depends('dry_gradation_table.wt_retained')
    def _compute_total_sieve(self):
        for record in self:
            print("recordd",record)
            record.total_sieve_analysis = sum(record.dry_gradation_table.mapped('wt_retained'))

    def default_get(self, fields):
        print("From Default Value")
        res = super(WbmMechanical, self).default_get(fields)

        default_dry_sieve_sizes = []
        default_elongated_sieve_sizes = []
        dry_sieve_sizes = ['53 mm','45 mm','22.4 mm', '11.2 mm', '4.75 mm','2.36 mm','600 micron','75 micron','pan']
        elongation_sieve_sizes = ['63 mm', '50 mm', '40 mm', '31.5 mm', '25 mm','20 mm','16 mm','12.5 mm','10 mm','6.3 mm']


        for i in range(9):  # You can change the number of default lines as needed
            size = {
                'sieve_size': dry_sieve_sizes[i] # Set the default product
                # Set the default quantity
            }
            default_dry_sieve_sizes.append((0, 0, size))
        res['dry_gradation_table'] = default_dry_sieve_sizes
        for i in range(10):  # You can change the number of default lines as needed
            size = {
                'sieve_size': elongation_sieve_sizes[i] # Set the default product
                # Set the default quantity
            }
            default_elongated_sieve_sizes.append((0, 0, size))
        res['dry_gradation_table'] = default_dry_sieve_sizes
        res['elongation_table'] = default_elongated_sieve_sizes

        return res

    # Water Absorbtion 
    water_absorbtion_name = fields.Char(default="Water Absorbtion")
    water_absorbtion_visible = fields.Boolean(compute="_compute_visible")

    wt_ssd_sample = fields.Integer('Weight of saturated surface dry (SSD) sample in air in gms, A')
    oven_dried_wt = fields.Float('Oven dried weight of sample in gms, C')
    water_absorbtion = fields.Float('Water absorption  %',compute="_compute_water_absorbtion")

    @api.depends('wt_ssd_sample','oven_dried_wt')
    def _compute_water_absorbtion(self):
        for record in self:
            if record.oven_dried_wt != 0:
                record.water_absorbtion = round((record.wt_ssd_sample - record.oven_dried_wt)/record.oven_dried_wt * 100,2)
            else:
                record.water_absorbtion = 0

    # Flakiness and Elongation 
    elongation_name = fields.Char(default="Elongation and Flakiness Index")
    elongation_visible = fields.Boolean(compute="_compute_visible")

    flakiness_name = fields.Char(default=" Flakiness Index")
    flakiness_visible = fields.Boolean(compute="_compute_visible")

    elongation_table = fields.One2many('mech.wbm.elongation.flakiness.line','parent_id',string="Elongation Flakiness Index")

    total_wt_retained_fl_el = fields.Float('Total',compute="_compute_total_el_fl")
    total_elongated_retained = fields.Float('Total Elongation',compute="_compute_total_elongation")
    total_flakiness_retained = fields.Float('Total Flakiness',compute="_compute_total_flakiness")

    aggregate_elongation = fields.Float('Aggregate Elongation Value in %',compute="_compute_aggregate_elongation")
    aggregate_flakiness = fields.Float('Aggregate Flakiness Value in %' ,compute="_compute_aggregate_flakiness")
    aggregate_combine = fields.Float('Aggregate Elongation & Flakiness Value in %',compute="_compute_aggregate_combine")


    @api.depends('elongation_table.wt_retained')
    def _compute_total_el_fl(self):
        for record in self:
            record.total_wt_retained_fl_el = sum(record.elongation_table.mapped('wt_retained'))

    @api.depends('elongation_table.elongated_retained')
    def _compute_total_elongation(self):
        for record in self:
            record.total_elongated_retained = sum(record.elongation_table.mapped('elongated_retained'))

    @api.depends('elongation_table.flakiness_retained')
    def _compute_total_flakiness(self):
        for record in self:
            record.total_flakiness_retained = sum(record.elongation_table.mapped('flakiness_retained'))

    @api.depends('total_wt_retained_fl_el','total_elongated_retained')
    def _compute_aggregate_elongation(self):
        for record in self:
            if record.total_elongated_retained != 0:
                record.aggregate_elongation = round(record.total_elongated_retained/record.total_wt_retained_fl_el,2)
            else:
                record.aggregate_elongation = 0

    @api.depends('total_wt_retained_fl_el','total_flakiness_retained')
    def _compute_aggregate_flakiness(self):
        for record in self:
            if record.total_flakiness_retained != 0:
                record.aggregate_flakiness = round(record.total_flakiness_retained/record.total_wt_retained_fl_el,2)
            else:
                record.aggregate_flakiness = 0

    @api.depends('total_wt_retained_fl_el','total_flakiness_retained')
    def _compute_aggregate_combine(self):
        for record in self:
            record.aggregate_combine = round(record.aggregate_elongation+record.aggregate_flakiness,2)
            



    # Abrasion Value
    abrasion_value_name = fields.Char("Name",default="Abrasion Value")
    abrasion_visible = fields.Boolean("Abrasion Visible",compute="_compute_visible")

    total_weight_sample_abrasion = fields.Integer(string="Total weight of Sample in gms")
    weight_passing_sample_abrasion = fields.Integer(string="Weight of Passing sample in 1.70 mm IS sieve in gms")
    weight_retain_sample_abrasion = fields.Integer(string="Weight of Retain sample in 1.70 mm IS sieve in gms",compute="_compute_weight_retain_sample_abrasion")
    abrasion_value_percentage = fields.Float(string="Abrasion Value (%)",compute="_compute_sample_weight")


    @api.depends('total_weight_sample_abrasion', 'weight_passing_sample_abrasion')
    def _compute_weight_retain_sample_abrasion(self):
        for line in self:
            line.weight_retain_sample_abrasion = line.total_weight_sample_abrasion - line.weight_passing_sample_abrasion


    @api.depends('total_weight_sample_abrasion', 'weight_passing_sample_abrasion')
    def _compute_sample_weight(self):
        for line in self:
            if line.total_weight_sample_abrasion != 0:
                line.abrasion_value_percentage = round((line.weight_passing_sample_abrasion / line.total_weight_sample_abrasion) * 100,2)
            else:
                line.abrasion_value_percentage = 0.0

    # Impact Value 
    impact_value_name = fields.Char("Name",default="Impact Value")
    impact_visible = fields.Boolean("Impact Visible",compute="_compute_visible")

    impact_value_child_lines = fields.One2many('mech.wbm.impact.line','parent_id',string="Parameter")

    average_impact_value = fields.Float(string="Average Impact Value", compute="_compute_average_impact_value")

    

    @api.depends('impact_value_child_lines.impact_value')
    def _compute_average_impact_value(self):
        for record in self:
            if record.impact_value_child_lines:
                sum_impact_value = sum(record.impact_value_child_lines.mapped('impact_value'))
                record.average_impact_value = round((sum_impact_value / len(record.impact_value_child_lines)),1)
            else:
                record.average_impact_value = 0.0

    # Liquid Limit
    liquid_limit_name = fields.Char("Name",default="Liquid Limit")
    liquid_limit_visible = fields.Boolean("Liquid Limit Visible",compute="_compute_visible")

    liquid_limit_table = fields.One2many('mech.wbm.liquid.limit.line','parent_id',string="Liquid Limit")
    liquid_limit = fields.Float("Liquid Limit")
    remarks_liquid_limit = fields.Selection([
        ('plastic', 'Plastic'),
        ('non-plastic', 'Non-Plastic')],"Remarks",store=True)


    # Plastic Limit
    plastic_name = fields.Char("Name",default="Plastic Limit")
    plastic_visible = fields.Boolean("Plastic Limit Visible",compute="_compute_visible")

    plastic_table = fields.One2many('mech.wbm.plastic.limit.line','parent_id',string="Plastic Limit")
    average_plastic_moisture = fields.Float("Average",compute="_compute_plastic_average")
    remarks_plastic = fields.Selection([
        ('plastic', 'Plastic'),
        ('non-plastic', 'Non-Plastic')],"Remarks",store=True)

   

    
    @api.depends('plastic_table.moisture_percent')
    def _compute_plastic_average(self):
        for record in self:
            if record.plastic_table:
                sum_moisture_percent = sum(record.plastic_table.mapped('moisture_percent'))
                record.average_plastic_moisture = round((sum_moisture_percent / len(record.plastic_table)),2)
            else:
                record.average_plastic_moisture = 0.0

    # Plasticity Index
    plasticity_index_visible = fields.Boolean("Plasticity Index Visible",compute="_compute_visible")
    plasticity_index = fields.Float("Plasticity Index",compute="_compute_plasticity_limit")

    @api.depends('average_plastic_moisture','liquid_limit')
    def _compute_plasticity_limit(self):
        for record in self:
            record.plasticity_index = record.liquid_limit - record.average_plastic_moisture

    # Density Relation Heavy Compaction
    density_relation_name = fields.Char("Name",default="Density Relation Using Heavy Compaction")
    density_relation_visible = fields.Boolean("Density Relation Visible",compute="_compute_visible")

    density_relation_table = fields.One2many('mech.wbm.density.relation.line','parent_id',string="Density Relation")
    wt_of_modul = fields.Float('Weight of Mould in gm')
    vl_of_modul = fields.Float('Volume of Mould in cc')
    chart_image_density = fields.Binary("Line Chart", compute="_compute_chart_image_density", store=True)



    def generate_line_chart_density(self):
        # Prepare data for the chart
        x_values = []
        y_values = []
        for line in self.density_relation_table:
            x_values.append(line.moisture)
            y_values.append(line.dry_density)
        
        # Create the line chart
        plt.plot(x_values, y_values, marker='o')
        plt.xlabel('% Moisture')
        plt.ylabel('Dry Density')
        plt.title('Density Relation Using Heavy Compaction')


        plt.ylim(bottom=0, top=max(y_values) + 10)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()  # Close the figure to free up resources
        buffer.seek(0)
    
        # Convert the chart image to base64
        chart_image = base64.b64encode(buffer.read()).decode('utf-8')  
        return chart_image
    
    @api.depends('density_relation_table')
    def _compute_chart_image_density(self):
        try:
            for record in self:
                chart_image = record.generate_line_chart_density()
                record.chart_image_density = chart_image
        except:
            pass 



    # CBR
    cbr_name = fields.Char("Name",default="CBR")
    cbr_visible = fields.Boolean("CBR Visible",compute="_compute_visible")

    cbr_table = fields.One2many('mechanical.wbm.cbr.line','parent_id',string="CBR")
    chart_image_cbr = fields.Binary("Line Chart", compute="_compute_chart_image_cbr", store=True)


    def generate_line_chart_cbr(self):
        # Prepare data for the chart
        x_values = []
        y_values = []
        for line in self.cbr_table:
            x_values.append(line.penetration)
            y_values.append(line.load)
        
        # Create the line chart
        plt.plot(x_values, y_values, marker='o')
        plt.xlabel('Penetration')
        plt.ylabel('Load')
        plt.title('CBR')


        plt.ylim(bottom=0, top=max(y_values) + 10)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()  # Close the figure to free up resources
        buffer.seek(0)
    
        # Convert the chart image to base64
        chart_image = base64.b64encode(buffer.read()).decode('utf-8')  
        return chart_image
    
    @api.depends('cbr_table')
    def _compute_chart_image_cbr(self):
        try:
            for record in self:
                chart_image = record.generate_line_chart_cbr()
                record.chart_image_cbr = chart_image
        except:
            pass 



class WbmDensityRelationLine(models.Model):
    _name = "mech.wbm.density.relation.line"
    parent_id = fields.Many2one('mechanical.wbm',string="Parent Id")

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
            line.wt_of_compact = round(line.wt_of_modul_compact - line.parent_id.wt_of_modul,2)



    @api.depends('wt_of_compact', 'parent_id.vl_of_modul')
    def _compute_bulk_density(self):
        for line in self:
            if line.parent_id.vl_of_modul != 0:
                line.bulk_density = round(line.wt_of_compact / line.parent_id.vl_of_modul,2)
            else:
                line.bulk_density = 0.0



    @api.depends('wt_of_container_dry', 'wt_of_container')
    def _compute_wt_of_dry_sample(self):
        for line in self:
            line.wt_of_dry_sample = round(line.wt_of_container_dry - line.wt_of_container,2)


    @api.depends('wt_of_container_wet','wt_of_container_dry')
    def _compute_wt_of_moisture(self):
        for record in self:
            record.wt_of_moisture = round((record.wt_of_container_wet - record.wt_of_container_dry),2)


    @api.depends('wt_of_moisture', 'wt_of_dry_sample')
    def _compute_moisture(self):
        for line in self:
            if line.wt_of_dry_sample != 0:
                line.moisture = round(line.wt_of_moisture / line.wt_of_dry_sample * 100,2)
            else:
                line.moisture = 0.0


    @api.depends('bulk_density', 'moisture')
    def _compute_dry_density(self):
        for line in self:
            line.dry_density = round((100 * line.bulk_density) / (100 + line.moisture),2)


 



class WbmCBRLine(models.Model):
    _name = "mechanical.wbm.cbr.line"
    parent_id = fields.Many2one('mechanical.wbm',string="Parent Id")

    penetration = fields.Float(string="Penetration in mm")
    proving_reading = fields.Float(string="Proving Ring Reading")
    load = fields.Float(string="Load in Kg", compute="_compute_load")


    @api.depends('proving_reading')
    def _compute_load(self):
        for record in self:
            record.load = record.proving_reading * 6.96



class WbmLiquidLimitLine(models.Model):
    _name = "mech.wbm.liquid.limit.line"
    parent_id = fields.Many2one('mechanical.wbm', string="Parent Id")
    
    container_no = fields.Char("Container No.")
    blows = fields.Integer(string="No of Blows")
    mass_wet_sample_container = fields.Float(string="Mass of wet sample+container, (M1) in gms")
    mass_dry_sample_container = fields.Float(string="Mass of dry sample+container, (M2) in gms")
    mass_container = fields.Float(string="Mass of container, (M3) in gms")
    mass_moisture = fields.Float(string="Mass of Moisture, (M1-M2) in gms",compute="_compute_mass_moisture")
    mass_dry_sample = fields.Float(string="Mass of dry sample, (M2-M3) in gms",compute="_compute_mass_dry_sample")
    moisture_percent = fields.Float(string="% Moisture",compute="_compute_moisture_percent")


    @api.depends('mass_dry_sample_container','mass_wet_sample_container')
    def _compute_mass_moisture(self):
        for record in self:
            record.mass_moisture = record.mass_wet_sample_container - record.mass_dry_sample_container


    @api.depends('mass_dry_sample_container','mass_container')
    def _compute_mass_dry_sample(self):
        for record in self:
            record.mass_dry_sample = record.mass_dry_sample_container - record.mass_container

    @api.depends('mass_moisture','mass_dry_sample')
    def _compute_moisture_percent(self):
        for record in self:
            if record.mass_dry_sample != 0:
                record.moisture_percent = round((record.mass_moisture /record.mass_dry_sample) *100,2)
            else:
                record.moisture_percent = 0



class WbmPlasticLimitLine(models.Model):
    _name = "mech.wbm.plastic.limit.line"
    parent_id = fields.Many2one('mechanical.wbm', string="Parent Id")
    
    container_no = fields.Char("Container No.")
    mass_wet_sample_container = fields.Float(string="Mass of wet sample+container, (M1) in gms")
    mass_dry_sample_container = fields.Float(string="Mass of dry sample+container, (M2) in gms")
    mass_container = fields.Float(string="Mass of container, (M3) in gms")
    mass_moisture = fields.Float(string="Mass of Moisture, (M1-M2) in gms",compute="_compute_mass_moisture")
    mass_dry_sample = fields.Float(string="Mass of dry sample, (M2-M3) in gms",compute="_compute_mass_dry_sample")
    moisture_percent = fields.Float(string="% Moisture",compute="_compute_moisture_percent")


    @api.depends('mass_dry_sample_container','mass_wet_sample_container')
    def _compute_mass_moisture(self):
        for record in self:
            record.mass_moisture = record.mass_wet_sample_container - record.mass_dry_sample_container


    @api.depends('mass_dry_sample_container','mass_container')
    def _compute_mass_dry_sample(self):
        for record in self:
            record.mass_dry_sample = record.mass_dry_sample_container - record.mass_container

    @api.depends('mass_moisture','mass_dry_sample')
    def _compute_moisture_percent(self):
        for record in self:
            if record.mass_dry_sample != 0:
                record.moisture_percent = round((record.mass_moisture /record.mass_dry_sample) *100,2)
            else:
                record.moisture_percent = 0


class WbmDryGradationLine(models.Model):
    _name = "mech.wbm.dry.gradation.line"
    parent_id = fields.Many2one('mechanical.wbm', string="Parent Id")
    
    serial_no = fields.Integer(string="Sr. No", readonly=True, copy=False, default=1)
    sieve_size = fields.Char(string="IS Sieve Size" )
    wt_retained = fields.Float(string="Wt. Retained in gms")
    percent_retained = fields.Float(string='% Retained', compute="_compute_percent_retained")
    cumulative_retained = fields.Float(string="Cum. Retained %", store=True)
    passing_percent = fields.Float(string="Passing %")



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('serial_no'))
                vals['serial_no'] = max_serial_no + 1

        return super(DryGradationLine, self).create(vals)

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
                    record.percent_retained = round((vals['wt_retained'] / record.parent_id.total * 100),2) if record.parent_id.total else 0

            new_self = super(DryGradationLine, self).write(vals)

            if 'wt_retained' in vals:
                for record in self:
                    record.parent_id._compute_total_sieve()

            return new_self

        return super(DryGradationLine, self).write(vals)

    def unlink(self):
        # Get the parent_id before the deletion
        parent_id = self[0].parent_id

        res = super(DryGradationLine, self).unlink()

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


class WbmElongationLine(models.Model):
    _name = "mech.wbm.elongation.flakiness.line"
    parent_id = fields.Many2one('mechanical.wbm', string="Parent Id")

    sieve_size = fields.Char(string="IS Sieve Size")
    wt_retained = fields.Float(string="Wt. Retained in gms")
    elongated_retained = fields.Float(string="Elongated Retained in gms")
    flakiness_retained = fields.Float(string="Flakiness Retained in gms")



# class FlakinessLine(models.Model):
#     _name = "mech.flakiness.line"
#     parent_id = fields.Many2one('mechanical.wbm', string="Parent Id")

#     sieve_size = fields.Char(string="IS Sieve Size")
#     wt_retained = fields.Float(string="Wt. Retained in gms")
#     flakiness_retained = fields.Float(string="Flakiness Retained in gms")


class WbmImpactValueLine(models.Model):
    _name = "mech.wbm.impact.line"
    parent_id = fields.Many2one('mechanical.wbm',string="Parent Id")

    sample_no = fields.Integer(string="Sample", readonly=True, copy=False, default=1)
    wt_of_cylinder = fields.Integer(string="Weight of cylindrical measure in gms")
    total_wt_of_dried = fields.Integer(string="Total Wt. of Oven dried (4 hrs) aggregate sample + cylindrical measure in gms")
    total_wt_aggregate = fields.Float(string="Total Wt. of Oven dried (4 hrs) aggregate sample filling the cylindrical measure in gms", compute="_compute_total_wt_aggregate")
    wt_of_aggregate_passing = fields.Float(string="Wt. of aggregate passing 2.36 mm sieve after the test in gms")
    wt_of_aggregate_retained = fields.Float(string="Wt. of aggregate retained on 2.36 mm sieve after the test in gms", compute="_compute_wt_of_aggregate_retained")
    impact_value = fields.Float(string="Impact value", compute="_compute_impact_value")


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