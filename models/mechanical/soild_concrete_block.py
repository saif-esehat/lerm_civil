from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError
import math




class SolidConcreteBlock(models.Model):
    _name = "mechanical.solid.concrete.block"
    _inherit = "lerm.eln"
    _rec_name = "name_solid_bolck"


    name_solid_bolck = fields.Char("Name",default="Solid Concrete Block")
    parameter_id = fields.Many2one('eln.parameters.result', string="Parameter")

    sample_parameters = fields.Many2many('lerm.parameter.master',string="Parameters",compute="_compute_sample_parameters",store=True)
    eln_ref = fields.Many2one('lerm.eln',string="Eln")

    
    # Block Density
    block_density_name = fields.Char("Name",default="Block Density")
    block_density_visible = fields.Boolean("Block Density Visible",compute="_compute_visible")

    child_lines = fields.One2many('mechanical.block.density.line','parent_id',string="Parameter")
    average_block = fields.Float(string="Average Block Density", compute="_compute_average_block",digits=(16,1))

    average_length = fields.Float(string="Average Length", compute="_compute_average_length",digits=(16,1))
    average_hight = fields.Float(string="Average Height",compute="_compute_average_hight", digits=(16, 1))
    average_thickness = fields.Float(string="Average Thickness", compute="_compute_average_width1",digits=(16,1))


    @api.depends('child_lines.block_density')
    def _compute_average_block(self):
        for record in self:
            block_densities = record.child_lines.mapped('block_density')
            if block_densities:
                record.average_block = sum(block_densities) / len(block_densities)
            else:
                record.average_block = 0.0


    @api.depends('child_lines.length')
    def _compute_average_length(self):
        for record in self:
            if record.child_lines:
                lengths = [line.length for line in record.child_lines]
                record.average_length = sum(lengths) / len(lengths)
            else:
                record.average_length = 0.0

                
    @api.depends('child_lines.heigth')
    def _compute_average_hight(self):
        for record in self:
            if record.child_lines:
                heights = [line.heigth for line in record.child_lines]
                record.average_hight = sum(heights) / len(heights)
            else:
                record.average_hight = 0.0

  
   

    @api.depends('child_lines.thickness')
    def _compute_average_width1(self):
        for record in self:
            if record.child_lines:
                thicknesss = [line.thickness for line in record.child_lines]
                record.average_thickness = sum(thicknesss) / len(thicknesss)
            else:
                record.average_thickness = 0.0


    
    # Moisture Movment
    moisture_movment_name = fields.Char("Name",default="Moisture Movement")
    moisture_movment_visible = fields.Boolean("Moisture Movment Visible",compute="_compute_visible")

    child_lines1 = fields.One2many('mechanical.moisture.movement.line','parent_id',string="Parameter")
    average_moisture_movment = fields.Float(string="Average",compute="_compute_average_moisture_movment", digits=(12, 2))


    
    @api.depends('child_lines1.moisture_movment')
    def _compute_average_moisture_movment(self):
        for record in self:
            moisture_movments = record.child_lines1.mapped('moisture_movment')
            record.average_moisture_movment = sum(moisture_movments) / len(moisture_movments) if len(moisture_movments) > 0 else 0.0

     
    # Drying shrinkage
    drying_shrinkage_name = fields.Char("Name",default="Drying Shrinkage")
    drying_shrinkage_visible = fields.Boolean("Drying Shrinkage Visible",compute="_compute_visible")

    child_lines2 = fields.One2many('mechanical.drying.shrinkage.line','parent_id',string="Parameter")
    average_drying_shrinkage = fields.Float(string="Average", compute="_compute_average_drying_shrinkage")

    @api.depends('child_lines2.drying_shrinkage')
    def _compute_average_drying_shrinkage(self):
        for record in self:
            total_drying_shrinkage = sum(record.child_lines2.mapped('drying_shrinkage'))
            count_lines = len(record.child_lines2)
            record.average_drying_shrinkage = total_drying_shrinkage / count_lines if count_lines else 0.0


    

    water_absorption_name = fields.Char("Name",default="Water Absorption")
    water_absorption_visible = fields.Boolean("Water Absorption Visible",compute="_compute_visible")
    child_lines3 = fields.One2many('mechanical.water.absorption.line','parent_id',string="Parameter")
    average_water_absorption = fields.Float(string="Average", compute="_compute_average_water_absorption")


    @api.depends('child_lines3.water_absorption')
    def _compute_average_water_absorption(self):
        for record in self:
            total_water_absorption = 0.0
            count_lines = len(record.child_lines3)
            for line in record.child_lines3:
                total_water_absorption += line.water_absorption
            record.average_water_absorption = total_water_absorption / count_lines if count_lines else 0.0


    # Dimension

    dimension_name1 = fields.Char("Name",default="Dimension")
    dimension_visible = fields.Boolean("Dimension Visible",compute="_compute_visible")   

    # name = fields.Char("Name",default="DIMENSION")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines4 = fields.One2many('mechanical.dimension.line','parent_id',string="Parameter")
    average_length = fields.Float(string="Average Length", compute="_compute_average_length",digits=(16,1))
    average_hight = fields.Float(string="Average Thickness",compute="_compute_average_hight", digits=(16, 1))
    average_width = fields.Float(string="Average Width", compute="_compute_average_width",digits=(16,1))
    

    @api.depends('child_lines4.length')
    def _compute_average_length(self):
        for record in self:
            if record.child_lines4:
                lengths = [line.length for line in record.child_lines4]
                record.average_length = sum(lengths) / len(lengths)
            else:
                record.average_length = 0.0

                
    @api.depends('child_lines4.hight')
    def _compute_average_hight(self):
        for record in self:
            if record.child_lines4:
                heights = [line.hight for line in record.child_lines4]
                record.average_hight = sum(heights) / len(heights)
            else:
                record.average_hight = 0.0

  
   

    @api.depends('child_lines4.width')
    def _compute_average_width(self):
        for record in self:
            if record.child_lines4:
                widths = [line.width for line in record.child_lines4]
                record.average_width = sum(widths) / len(widths)
            else:
                record.average_width = 0.0



     # Compressive Strength

    compressive_name = fields.Char("Name",default="Compressive Strength")
    compressive_visible = fields.Boolean("Compressive Strength Visible",compute="_compute_visible")   

    # name = fields.Char("Name",default="DIMENSION")
    parameter_id = fields.Many2one('eln.parameters.result',string="Parameter")
    child_lines5 = fields.One2many('mechanical.compressive.strength.line','parent_id',string="Parameter")
    avg_compressive_strength = fields.Float(string="Average",compute="compute_avg_compressive_strength",digits=(16,2))


    @api.depends('child_lines5.compressiv_strength')
    def compute_avg_compressive_strength(self):
        for record in self:
            total_strength = sum(line.compressiv_strength for line in record.child_lines5)
            num_lines = len(record.child_lines5)
            record.avg_compressive_strength = total_strength / num_lines if num_lines > 0 else 0.0







    ### Compute Visible
    @api.depends('sample_parameters')
    def _compute_visible(self):
        
        for record in self:
            record.block_density_visible = False
            record.moisture_movment_visible = False
            record.drying_shrinkage_visible = False
            record.water_absorption_visible = False
            record.dimension_visible = False
            record.compressive_visible = False
           
            
            for sample in record.sample_parameters:
                print("Internal Ids",sample.internal_id)

                if sample.internal_id == "e2190504-cc89-4334-a001-4766f9c65e24":
                    record.block_density_visible = True

                if sample.internal_id == "89acdd9a-0b60-4ab4-92fa-3b7756bab153":
                    record.moisture_movment_visible = True

                if sample.internal_id == "32aee782-8018-4833-a365-d72ccb6f47bd":
                    record.drying_shrinkage_visible = True

                if sample.internal_id == "0faf6556-4902-4926-a6bd-ed0024dc5929":
                    record.water_absorption_visible = True

                if sample.internal_id == "68e3da78-7440-44b3-8f19-2f7e3c0de618":
                    record.dimension_visible = True

                if sample.internal_id == "3402d345-b96e-4ed1-a545-dd5b2a6e259a":
                    record.compressive_visible = True





                




               


    @api.model
    def create(self, vals):
        # import wdb;wdb.set_trace()
        record = super(SolidConcreteBlock, self).create(vals)
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
        record = self.env['mechanical.solid.concrete.block'].browse(self.ids[0])
        field_values = {}
        for field_name, field in record._fields.items():
            field_value = record[field_name]
            field_values[field_name] = field_value

        return field_values
    


class BlockDensityLine(models.Model):
    _name = "mechanical.block.density.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    length = fields.Float(string="Length (mm)")
    heigth = fields.Float(string="Height (mm)")
    thickness = fields.Float(string="Thickness (mm)")
    volume = fields.Float(string="Volume (Cm3)", compute="_compute_volume")
    intial_wt = fields.Float(string="Initial Weight of the Specimen (kg)")
    final_wt = fields.Float(string="Final Weight of the Specimen after Oven Dry (kg) (Constant)")
    block_density = fields.Float(string="Block Density (kg/M³)", compute="_compute_block_density")



    @api.depends('length','heigth','thickness')
    def _compute_volume(self):
        for record in self:
            record.volume = record.length * record.heigth * record.thickness


    @api.depends('final_wt','volume')
    def _compute_block_density(self):
        for record in self:
            if record.volume != 0:
                record.block_density = record.final_wt / record.volume * 1000000
            else:
                record.block_density = 0.0

    

    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(BlockDensityLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



class MoistureMovementLine(models.Model):
    _name = "mechanical.moisture.movement.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    dry_length = fields.Float(string="Dry Length of the Block")
    wet_length = fields.Float(string="Wet Length of the Block")
    moisture_movment = fields.Float(string="Moisture Movement %", compute="_compute_moisture_movement", digits=(12, 2))



    @api.depends('dry_length', 'wet_length')
    def _compute_moisture_movement(self):
        for record in self:
            if record.wet_length != 0:
                record.moisture_movment = (record.wet_length - record.dry_length) / record.wet_length * 100
            else:
                record.moisture_movment = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(MoistureMovementLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



class DryingShrinkageLine(models.Model):
    _name = "mechanical.drying.shrinkage.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    wet_measurment = fields.Float(string="Wet measuremet of the Block",digits=(12, 3))
    dry_measurment = fields.Float(string="Dry Measurement of the Block",digits=(12, 3))
    dry_lengths = fields.Float(string="Dry Lenth")
    drying_shrinkage = fields.Float(string="Drying Shrinkage %", compute="_compute_drying_shrinkage",digits=(12, 2))



    @api.depends('wet_measurment', 'dry_measurment', 'dry_lengths')
    def _compute_drying_shrinkage(self):
        for record in self:
            if record.dry_lengths != 0:
                record.drying_shrinkage = record.dry_measurment - (record.wet_measurment / record.dry_lengths * 100)
            else:
                record.drying_shrinkage = 0.0


    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(DryingShrinkageLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1


class WaterAbsorptionLine(models.Model):
    _name = "mechanical.water.absorption.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr.No.", readonly=True, copy=False, default=1)
    wet_mass = fields.Float(string="Wet Mass of the Block (kg)")
    dry_mass = fields.Float(string="Dry Mass of the Block (kg)")
    water_absorption = fields.Float(string="Water Absorption %", compute="_compute_water_absorption")


    @api.depends('wet_mass', 'dry_mass')
    def _compute_water_absorption(self):
        for record in self:
            if record.dry_mass != 0:
                record.water_absorption = (record.wet_mass - record.dry_mass) / record.dry_mass * 100
            else:
                record.water_absorption = 0.0



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(WaterAbsorptionLine, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1




class DimensionSolidBlock(models.Model):
    _name = "mechanical.dimension.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No.",readonly=True, copy=False, default=1)
    length = fields.Float(string="Length in mm")
    hight = fields.Float(string="Thickness in mm")
    width = fields.Float(string="Width in mm")



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(DimensionSolidBlock, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1



class CompressiveStrengthSolidBlock(models.Model):
    _name = "mechanical.compressive.strength.line"
    parent_id = fields.Many2one('mechanical.solid.concrete.block',string="Parent Id")
   
    sr_no = fields.Integer(string="Sr No.",readonly=True, copy=False, default=1)
    length = fields.Float(string="Length in mm")
    width = fields.Float(string="Width in mm")
    hight = fields.Float(string="Thickness in mm")
    area = fields.Float(string="Area (mm²)",compute="compute_area")
    load = fields.Float(string="Load (N)")
    compressiv_strength = fields.Float(string="Compressive Strength N/mm²",compute="compute_compressive_strength")


    @api.depends('width','hight')
    def compute_area(self):
        for record in self:
            record.area = record.width * record.hight
    

    @api.depends('load', 'area')
    def compute_compressive_strength(self):
        for record in self:
            if record.area != 0:
                record.compressiv_strength = (record.load / record.area) * 1000
            else:
                record.compressiv_strength = 0.0



    @api.model
    def create(self, vals):
        # Set the serial_no based on the existing records for the same parent
        if vals.get('parent_id'):
            existing_records = self.search([('parent_id', '=', vals['parent_id'])])
            if existing_records:
                max_serial_no = max(existing_records.mapped('sr_no'))
                vals['sr_no'] = max_serial_no + 1

        return super(CompressiveStrengthSolidBlock, self).create(vals)

    def _reorder_serial_numbers(self):
        # Reorder the serial numbers based on the positions of the records in child_lines
        records = self.sorted('id')
        for index, record in enumerate(records):
            record.sr_no = index + 1






