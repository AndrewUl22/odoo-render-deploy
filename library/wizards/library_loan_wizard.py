# -*- coding: utf-8 -*-
from odoo import fields, models


class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'
    _description = 'Lend a Book'

    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        domain=[('is_available', '=', True)],
    )
    member_id = fields.Many2one(
        'library.member', string='Member', required=True
    )
    due_date = fields.Date(string='Due Date')

    def action_confirm(self):
        self.ensure_one()
        self.env['library.loan'].create(
            {
                'book_id': self.book_id.id,
                'member_id': self.member_id.id,
                'due_date': self.due_date,
            }
        )
        return {'type': 'ir.actions.act_window_close'}
