/** @odoo-module **/
const spreadsheet = require("@documents_spreadsheet/js/o_spreadsheet/o_spreadsheet_loader")[Symbol.for("default")];
const { createEmptyWorkbookData } = spreadsheet.helpers;
import field_registry from 'web.field_registry_owl';
import AbstractFieldOwl from 'web.AbstractFieldOwl';
const { getDataFromTemplate, base64ToJson } = require("documents_spreadsheet.pivot_utils");
var rpc = require('web.rpc');
const { Component, useState } = owl;
const { Model } = spreadsheet;



class Spreadsheet extends AbstractFieldOwl {


    setup() {
        super.setup(...arguments);
        // this.action = useService("action");
        this.state = useState({ name: "Test" });
        // createEmptyWorkbookData

    }

    async insertInDatasheet() {




        if (!this.props.record.data.datasheet) {
            var datasheet = await this.getDatasheetData()
            var templateId = datasheet[0].spreadsheet_template[0]
            const data = await getDataFromTemplate(this.env.services.rpc, templateId)
            // console.log(data)
            const name = this.props.record.data.eln_id.data.display_name + "-" + this.record.data.parameter.parameter_name

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
                args: [[eln_parameters_id], { "datasheet": spreadsheetId }]
            });

            this.__owl__.parent.parentWidget.do_action({ type: "ir.actions.client", tag: "action_open_spreadsheet", params: { spreadsheet_id: spreadsheetId } })



        } else {
            // console.log(this.props.record.data.datasheet.data.id)
            // var datasheet = await this.getDatasheetData()
            // var templateId = datasheet[0].spreadsheet_template[0]
            // const data = await getDataFromTemplate(this.env.services.rpc, templateId)

            this.__owl__.parent.parentWidget.do_action({ type: "ir.actions.client", tag: "action_open_spreadsheet", params: { spreadsheet_id: this.props.record.data.datasheet.data.id } })
            // var rpc = this.env.services.rpc
            // debugger

            // const model = await new Model(data, {
            //     mode: "normal",
            //     evalContext: {
            //         env: {
            //             delayedRPC: rpc,
            //             services: { rpc },
            //         },
            //     },
            // });

            // // await model.waitForIdle();
            // // await model.dispatch("EVALUATE_CELLS", { sheetId: "Sheet1" })
            // await model.waitForIdle();

            // var xlsx =  await model.exportXLSX();

            // // await waitForEvaluation(model);
            // debugger
            // // rpc.query({
            // //     model: "ir.attachment",
            // //     method: "create",
            // //     args: [posted],
            // // })
            // // debugger
            // console.log(xlsx)

        }


    }


    async getDatasheetData() {
        // console.log(this.record.data)

        var datasheet_id = this.record.data.parameter.data.id
        var datasheet_data = await rpc.query({
            model: 'lerm.parameter.master',
            method: 'read',
            args: [[datasheet_id], []]
        })

        // console.log(datasheet_data)

        return datasheet_data
    }



}


class SetResult extends AbstractFieldOwl {

    async getDataSheetFromParameter() {
        var datasheet_id = this.props.record.data.datasheet.data.id
        var datasheet_data = await rpc.query({
            model: 'documents.document',
            method: 'read',
            args: [[datasheet_id], ["datas"]]
        })
        var data = base64ToJson(datasheet_data[0].datas)
        const model = await new Model(data, {
            mode: "normal",
            evalContext: {
                env: {
                    delayedRPC: rpc,
                    services: { rpc },
                },
            },
        });

        await model.waitForIdle();
        await model.dispatch("EVALUATE_CELLS", { sheetId: "Sheet1" })
        await model.waitForIdle();
        const sheet = model.getters.getSheets();
        const filteredSheet = sheet.filter((result) => {
            return result.name == 'Sheet1';
        });
        console.log(filteredSheet , 'sheet')
        const id = filteredSheet[0].rows[12].cells[1].evaluated.value;
        console.log(id , 'evalutaed value')


        const filteredDataFromSheet = filteredSheet[0].rows.filter((result) => {
            return Object.keys(result.cells).length !== 0
        });
        const columnsHeading = Object.values(filteredDataFromSheet[0].cells).map(entry => entry.evaluated.value);


        var rows = [];
        // Iterate over each object in the array
        for (var i = 1; i < filteredDataFromSheet.length; i++) {
            var obj = filteredDataFromSheet[i];

            // Create an empty array to store the evaluated values for the current row
            var rowValues = [];

            // Iterate over each cell in the current object
            // for (var cellKey in obj.cells) {
            for (let i = 0; i <= columnsHeading.length - 1 ; i ++) {
                if (obj.cells[i]) {
                    var cellValue = obj.cells[i];

                    // Check if the 'evaluated' key exists in the cell
                    if (cellValue.evaluated && cellValue.evaluated.value) {
                            // Append the 'value' from 'evaluated' to the row values
                            rowValues.push(cellValue.evaluated.value);
                    }
                }
                else{
                    rowValues.push("-");
                }
            }
            // Append the row values to the rows array
            rows.push(rowValues);
        }
        var formatedFinalData = [
            {'columns' : columnsHeading},
            {'rows' : rows}
        ]
        console.log(formatedFinalData)
        formatedFinalData = JSON.stringify(formatedFinalData);
        console.log(formatedFinalData)

    
        var eln_parameters_id = this.record.data.id
        await this.env.services.rpc({
            model: "eln.parameters",
            method: "write",
            args: [[eln_parameters_id], { "result_json": formatedFinalData }]
        });

        $( ".set_result_class" ).val(String(id))
        $( ".set_result_class" ).trigger("change")



    }




}

SetResult.template = "lerm_civil.set_result"


Spreadsheet.template = 'lerm_civil.fill_datasheet';


field_registry.add('set_result', SetResult);

field_registry.add('datasheet', Spreadsheet);

export default Spreadsheet

