from odoo import models, fields, api, _
import io
import xlsxwriter

class VendorForecast(models.Model):
    @api.multi
    def action_vendor_forecast_download_report(self):
        report_data = self.generate_report_data()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({'bold': True})
        worksheet.write(0, 0, _('Product'), header_format)
        worksheet.write(0, 1, _('Expected Quantity'), header_format)
        worksheet.write(0, 2, _('Forecast Date'), header_format)
        row = 1
        for data in report_data:
            worksheet.write(row, 0, data['product_name'])
            worksheet.write(row, 1, data['expected_quantity'])
            worksheet.write(row, 2, data['forecast_date'])
            row += 1
        workbook.close()
        output.seek(0)
        attachment_id = self.env['ir.attachment'].create({
            'name': 'Vendor Forecast Report.xlsx',
            'datas': output.read(),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment_id.id),
            'target': 'self',
        }

    def generate_report_data(self):
        domain = []
        if self.product_id:
            domain.append(('product_id', '=', self.product_id.id))
        if self.date_from:
            domain.append(('forecast_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('forecast_date', '<=', self.date_to))
        forecast_records = self.env['vendor.forecast'].search(domain)
        report_data = []
        for record in forecast_records:
            report_data.append({
                'product_name': record.product_id.name,
                'expected_quantity': record.expected_quantity,
                'forecast_date': record.forecast_date,
            })
        return report_data
class VendorForecastFilter(models.TransientModel):
    _name = 'vendor.forecast.filter'
    _description = 'Vendor Forecast Filter'

    product_id = fields.Many2one('product.product', string='Product')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    @api.multi
    def apply_filter(self):
        domain = []
        if self.product_id:
            domain.append(('product_id', '=', self.product_id.id))
        if self.date_from:
            domain.append(('forecast_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('forecast_date', '<=', self.date_to))
        action = self.env.context.get('active_id', False) and self.env.ref(
            'vendor_forecast.action_vendor_forecast_list') or False
        if action:
            action.domain = domain