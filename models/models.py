from datetime import datetime

from odoo import models, fields, api


class purchase_request(models.Model):
    _name = 'purchase.request'
    _description = 'purchase_request'

    Request_name = fields.Char(string='Request name', required=True)
    Requested_by = fields.Many2one(string='Requested by', comodel_name='res.users',
                                   default=lambda self: self.env.user.id)
    start_date = fields.Date(string='start date', default=datetime.today())
    end_date = fields.Date(string='end date')
    Rejection_reason = fields.Text(string="Rejection reason")
    order_lines = fields.One2many(string='order lines', comodel_name='purchase.request.lines', inverse_name='request_id')
    Total_price = fields.Float(string='Total price', compute='_compute_Total_price', store=1)
    Status = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To be approved'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel')
            ], default='draft')

    # user_group_purchase_manager = cls.env.ref('purchase.group_purchase_manager')
    @api.depends('order_lines')
    def _compute_Total_price(self):
        for rec in self:
            rec.Total_price = 0
            for line in rec.order_lines:
                rec.Total_price = rec.Total_price + line.Total

    def action_draft(self):
        for rec in self:
            rec.Status = 'draft'

    def action_tobe(self):
        for rec in self:
            rec.Status = 'to_be_approved'

    def action_approve(self):
        for rec in self:
            rec.Status = 'approve'

    def action_reject(self):
        for rec in self:
            rec.Status = 'reject'

    def action_cancel(self):
        for rec in self:
            rec.Status = 'to_be_approved'


class purchase_request_lines(models.Model):
    _name = 'purchase.request.lines'
    _description = 'purchase_request_lines.purchase_request_lines'

    product_id = fields.Many2one(string='product', comodel_name='product.product', required=True)
    description = fields.Char(string='description')
    quantity = fields.Float(string='quantity', default=1)
    cost_price = fields.Float(string='cost price')
    Total = fields.Float(string='Total')
    request_id = fields.Many2one(string='request id', comodel_name='purchase.request')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.description = self.product_id.name
            rec.cost_price = self.product_id.standard_price
            price = self.product_id.standard_price
            rec.Total = rec.quantity * self.product_id.standard_price

    @api.onchange('quantity')
    def _onchange_quantity(self):
        for rec in self:
            rec.Total = rec.cost_price * self.quantity

    # @api.onchange('order_lines')
    # def _onchange_order_lines(self):
    #     for rec in self:
    #         total = 0
    #         for line in self.order_lines:
    #             total = total + line.Total
