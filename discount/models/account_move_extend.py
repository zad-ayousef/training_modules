from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    total_discount = fields.Monetary(
        string='Total Discount',
        compute='_compute_total_discount',
        store=True,
        readonly=True,
        currency_field='currency_id'
    )

    @api.depends('invoice_line_ids.discount', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity')
    def _compute_total_discount(self):
        for move in self:
            total_discount = 0.0
            for line in move.invoice_line_ids.filtered(lambda l: l.discount):
                original_subtotal = line.price_unit * line.quantity
                discount_amount = original_subtotal * (line.discount / 100.0)
                total_discount += discount_amount
            move.total_discount = total_discount



    has_purchase_discount_line = fields.Boolean(default=False)
    has_sales_discount_line = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            move._sync_purchase_discounts()
            move._sync_sales_discounts()
        return moves

    def write(self, vals):
        res = super().write(vals)
        if any(f in vals for f in ['invoice_line_ids', 'line_ids']):
            for move in self:
                move._sync_purchase_discounts()
                move._sync_sales_discounts()
        return res

    def _sync_purchase_discounts(self):
        allowed_discount_value = self.env['ir.config_parameter'].sudo().get_param(
            'discount.allowed_discount'
        )
        if allowed_discount_value != "True":
            return

        for move in self:
            if move.move_type != "in_invoice":
                continue

            discount_account_id = self.env['ir.config_parameter'].sudo().get_param(
                'discount.allowed_discount_account_purchase_id'
            )
            if not discount_account_id:
                continue
            discount_account_id = int(discount_account_id)

            total_discount = 0.0

            for invoice_line in move.invoice_line_ids.filtered(lambda l: l.discount):
                original_subtotal = invoice_line.price_unit * invoice_line.quantity
                discount_amount = original_subtotal * (invoice_line.discount / 100.0)
                total_discount += discount_amount

                corresponding_move_lines = move.line_ids.filtered(
                    lambda l: l.product_id == invoice_line.product_id and
                              l.account_id == invoice_line.account_id and
                              not l.is_purchase_discount_line and
                              not l.is_sales_discount_line
                )

                for line in corresponding_move_lines:
                    line.with_context(check_move_validity=False).write({
                        'debit': original_subtotal if line.debit > 0 else 0.0,
                        'credit': original_subtotal if line.credit > 0 else 0.0,
                        'balance': original_subtotal if line.debit > 0 else -original_subtotal,
                    })

            if total_discount > 0:
                discount_line = move.line_ids.filtered(lambda l: l.is_purchase_discount_line)
                if discount_line:
                    discount_line[0].with_context(check_move_validity=False).write({
                        'credit': total_discount,
                        'balance': -total_discount,
                    })
                else:
                    self.env['account.move.line'].with_context(check_move_validity=False).create({
                        'move_id': move.id,
                        'name': "Purchase Discount",
                        'account_id': discount_account_id,
                        'debit': 0.0,
                        'credit': total_discount,
                        'balance': -total_discount,
                        'partner_id': move.partner_id.id,
                        'currency_id': move.currency_id.id,
                        'is_purchase_discount_line': True,
                        'display_type': 'tax',
                    })
                move.has_purchase_discount_line = True

    # --- SALES DISCOUNTS ---
    def _sync_sales_discounts(self):
        allowed_discount_value = self.env['ir.config_parameter'].sudo().get_param(
            'discount.allowed_discount'
        )
        if allowed_discount_value != "True":
            return

        for move in self:
            if move.move_type != "out_invoice":
                continue

            discount_account_id = self.env['ir.config_parameter'].sudo().get_param(
                'discount.allowed_discount_account_sales_id'
            )
            if not discount_account_id:
                continue
            discount_account_id = int(discount_account_id)

            total_discount = 0.0

            for invoice_line in move.invoice_line_ids.filtered(lambda l: l.discount):
                original_subtotal = invoice_line.price_unit * invoice_line.quantity
                discount_amount = original_subtotal * (invoice_line.discount / 100.0)
                total_discount += discount_amount

                corresponding_move_lines = move.line_ids.filtered(
                    lambda l: l.product_id == invoice_line.product_id and
                              l.account_id == invoice_line.account_id and
                              not l.is_purchase_discount_line and
                              not l.is_sales_discount_line
                )

                for line in corresponding_move_lines:
                    line.with_context(check_move_validity=False).write({
                        'debit': original_subtotal if line.debit > 0 else 0.0,
                        'credit': original_subtotal if line.credit > 0 else 0.0,
                        'balance': original_subtotal if line.debit > 0 else -original_subtotal,
                    })

            if total_discount > 0:
                discount_line = move.line_ids.filtered(lambda l: l.is_sales_discount_line)
                if discount_line:
                    discount_line[0].with_context(check_move_validity=False).write({
                        'debit': total_discount,
                        'balance': total_discount,
                    })
                else:
                    self.env['account.move.line'].with_context(check_move_validity=False).create({
                        'move_id': move.id,
                        'name': "Sales Discount",
                        'account_id': discount_account_id,
                        'debit': total_discount,
                        'credit': 0.0,
                        'balance': total_discount,
                        'partner_id': move.partner_id.id,
                        'currency_id': move.currency_id.id,
                        'is_sales_discount_line': True,
                        'display_type': 'tax',
                    })
                move.has_sales_discount_line = True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_purchase_discount_line = fields.Boolean(default=False)
    is_sales_discount_line = fields.Boolean(default=False)
