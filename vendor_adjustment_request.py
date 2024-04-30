from odoo import models, fields

class VendorAdjustmentRequest(models.Model):
    _name = 'vendor.adjustment.request'
    _description = 'Vendor Adjustment Request'

    order_id = fields.Many2one('sale.order', string='Order Reference')
    adjustment_detail = fields.Text(string='Requested Adjustment')
    comment = fields.Text(string='Additional Comments')
    date_request = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('done', 'Done')], string='Status', default='draft')
    @api.multi
    def action_send_email(self):
                template = self.env.ref('base.model_vendor_adjustment_request.email_template_vendor_adjustment_request')
                template.send_mail(self.ids, force_send=True)

    def submit_adjustment_request(self):

        adjustment_request = self.env['vendor.adjustment.request'].create({
            'order_id': self.order_id.id,
            'adjustment_detail': self.adjustment_detail,
            'comment': self.comment,
        })


        template = self.env.ref('vendor_adjustment_request.email_template_vendor_adjustment_request')
        template.send_mail(adjustment_request.id)


        adjustment_request.write({'state': 'sent'})


        action = self.env.ref('vendor_adjustment_request.action_vendor_adjustment_request_list')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'vendor.adjustment.request',
            'view_mode': 'tree,form',
            'views': [(False, 'tree'), (False, 'form')],
            'target': 'current',
            'context': {'create': False},
        }