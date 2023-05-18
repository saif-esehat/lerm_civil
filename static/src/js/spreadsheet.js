/** @odoo-module **/
const spreadsheet = require("@documents_spreadsheet/js/o_spreadsheet/o_spreadsheet_loader")[Symbol.for("default")];
const { createEmptyWorkbookData } = spreadsheet.helpers;
import field_registry from 'web.field_registry_owl';
import AbstractFieldOwl from 'web.AbstractFieldOwl';
const { getDataFromTemplate } = require("documents_spreadsheet.pivot_utils");
var rpc = require('web.rpc');
const { Component, useState } = owl;


class Spreadsheet extends AbstractFieldOwl  {


    setup() {
        super.setup(...arguments);
        // this.action = useService("action");
        this.state = useState({ name:"Test"});
        // console.log("Setup Working")
    }

    async insertInDatasheet(){
        console.log(this.props.record.data.datasheet)

        

        if (!this.props.record.data.datasheet) {
        var datasheet = await this.getDatasheetData()
        var templateId = datasheet[0].spreadsheet_template[0]
        const data = await getDataFromTemplate(this.env.services.rpc, templateId)
        // console.log(data)
        const name = this.props.record.data.eln_id.data.display_name+"-"+this.record.data.parameter.parameter_name

        const spreadsheetId = await this.env.services.rpc({
            model: "documents.document",
            method: "create",
            args: [
                {
                    name,
                    mimetype: "application/o-spreadsheet",
                    folder_id: this.props.folderId,
                    handler: "spreadsheet",
                    raw: JSON.stringify(data),
                },
            ],
            context: this.props.context,
        });

        this.env.services.notification.notify({
            type: "info",
            message: this.env._t("New sheet saved in Documents"),
            sticky: false,
        });

        this.trigger("spreadsheet-created", { spreadsheetId });

        var eln_parameters_id = this.record.data.id
        await this.env.services.rpc({
                model: "eln.parameters",
                method: "write",
                args: [[eln_parameters_id],{"datasheet":spreadsheetId}]
            });
    
        this.__owl__.parent.parentWidget.do_action({ type : "ir.actions.client" , tag : "action_open_spreadsheet" , params : { spreadsheet_id: spreadsheetId}})

            
        }else{
            this.__owl__.parent.parentWidget.do_action({ type : "ir.actions.client" , tag : "action_open_spreadsheet" , params : { spreadsheet_id: this.props.record.data.id}})

        }
    

    }



    async getDatasheetData(){
        // console.log(this.record.data)

        var datasheet_id = this.record.data.parameter.data.id
        var datasheet_data = await rpc.query({
            model: 'lerm.parameter.master',
            method: 'read',
            args: [[datasheet_id],[]]
        })

        // console.log(datasheet_data)

        return datasheet_data
    }



}


Spreadsheet.template = 'lerm_civil.fill_datasheet';

field_registry.add('datasheet', Spreadsheet);

export default Spreadsheet

