# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_invoice = fields.Date(track_visibility='onchange')
    l10n_mx_edi_expense_id = fields.Many2one(
        'hr.expense', 'Expense',
        help='Stores the expense related with this invoice')
    l10n_mx_edi_expense_sheet_id = fields.Many2one(
        'hr.expense.sheet', string='Expense Sheet',
        related='l10n_mx_edi_expense_id.sheet_id', store=True,
        help='Stores the expense sheet related with this invoice')

    @api.multi
    def action_invoice_open(self):
        res = super().action_invoice_open()
        message = _(
            'The amount total in the CFDI is (%s) and that value is different '
            'to the invoice total (%s), that values must be consistent. '
            'Please review the invoice lines and try again. You can contact '
            'your manager to change the minimum allowed for this difference '
            'in the journal.\n\nCFDI with UUID: %s')
        label = self.env.ref(
            'l10n_mx_edi_hr_expense.tag_omit_invoice_amount_check')
        partners = self.mapped('partner_id').filtered(
            lambda par: label not in par.category_id)
        invoices = self.filtered(lambda inv: inv.l10n_mx_edi_cfdi_amount and
                                 inv.partner_id in partners)
        for invoice in invoices.filtered(lambda inv: inv.type in (
                'in_invoice', 'in_refund')):
            diff = invoice.journal_id.l10n_mx_edi_amount_authorized_diff
            if not abs(invoice.amount_total - invoice.l10n_mx_edi_cfdi_amount) > diff:  # noqa
                continue
            currency = invoice.currency_id
            raise UserError(message % (
                formatLang(self.env, invoice.l10n_mx_edi_cfdi_amount, currency_obj=currency),  # noqa
                formatLang(self.env, invoice.amount_total, currency_obj=currency),  # noqa
                invoice.l10n_mx_edi_cfdi_uuid))
        for invoice in invoices.filtered(lambda inv: inv.type in (
                'out_invoice', 'out_refund')):
            diff = invoice.journal_id.l10n_mx_edi_amount_authorized_diff
            if not abs(invoice.amount_total - invoice.l10n_mx_edi_cfdi_amount) > diff:  # noqa
                continue
            currency = invoice.currency_id
            invoice.message_post(body=message % (
                formatLang(self.env, invoice.l10n_mx_edi_cfdi_amount, currency_obj=currency),  # noqa
                formatLang(self.env, invoice.amount_total, currency_obj=currency),  # noqa
                invoice.l10n_mx_edi_cfdi_uuid))
        return res

    @api.multi
    def action_view_expense(self):
        self.ensure_one()
        expense = self.env['hr.expense'].search([
            ('l10n_mx_edi_invoice_id', '=', self.id)], limit=1)
        if not expense:
            raise UserError(_('This invoice was not created from an expense'))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense',
            'target': 'current',
            'res_id': expense.id
        }

    @api.multi
    def _reclassify_journal_entries(
            self, account_id=None, product_id=None, date=None):
        """Reclassify data in the invoice"""
        for inv in self:
            inv.date = date if date else inv.date
            for line in inv.invoice_line_ids:
                line.account_id = account_id if account_id else line.account_id
                line.product_id = product_id if product_id else line.product_id
            if not inv.move_id:
                continue
            state = inv.move_id.state
            if state == 'posted':
                inv.move_id.button_cancel()
            inv.move_id.date = date if date else inv.move_id.date
            tax_accounts = inv.tax_line_ids.mapped('account_id')
            lines = inv.move_id.line_ids.filtered(
                lambda l: l.account_id.user_type_id.type != 'payable' and
                l.account_id not in tax_accounts)
            for line in lines:
                line.account_id = account_id if account_id else line.account_id
                line.date = date if date else line.date
            if state == 'posted':
                inv.move_id.action_post()
