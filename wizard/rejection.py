from odoo import api, fields, models


class Rejection(models.TransientModel):
    _name = 'purchase.request.rejection'
    _description = 'rejection on purchase request'

    def _get_purchase_request(self):
        return self._context.get('active_id', False)

    reason = fields.Many2one(comodel_name='purchase.request', string='rejection reason', default=_get_purchase_request)
    rejection = fields.Text(string='rejection Reason')

    def saveReason(self):
        for rec in self:
            self.reason.Rejection_reason = rec.rejection
            self.reason.Status = 'reject'

    def sendemail(self, emails=[]):
        self.reason.Status = 'approve'
        # new = self.env['res.groups'].search([])
        users = self.env["res.users"].search([])
        purchase_manager_users = [user for user in users if user.has_group('purchase.group_purchase_manager')]
        emails = [user.login for user in purchase_manager_users if user.login]
        ctx = {}
        if emails:
            ctx['email_to'] = ','.join(emails)
            ctx['email_from'] = self.env.user.company_id.email
            ctx['send_email'] = True
            template = self.env.ref('purchase_request.purchase_confirm_mail')
            template.with_context(ctx).send_mail(self.id, force_send=True, raise_exception=False)
        # new = self.env.ref('purchase.group_purchase_manager')
        # for line in new.users:
        #     emails = line.email
