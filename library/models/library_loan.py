# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'
    _order = 'loan_date desc'

    book_id = fields.Many2one(
        'library.book', string='Book', required=True
    )
    member_id = fields.Many2one(
        'library.member', string='Member', required=True
    )
    loan_date = fields.Date(
        string='Loan Date', default=fields.Date.context_today
    )
    due_date = fields.Date(string='Due Date')
    return_date = fields.Date(string='Return Date')
    state = fields.Selection(
        [
            ('ongoing', 'Ongoing'),
            ('returned', 'Returned'),
        ],
        string='Status',
        default='ongoing',
    )
    is_overdue = fields.Boolean(
        string='Overdue', compute='_compute_is_overdue'
    )

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for loan in self:
            loan.is_overdue = bool(
                loan.due_date
                and loan.state == 'ongoing'
                and loan.due_date < today
            )

    @api.constrains('book_id', 'state')
    def _check_book_available(self):
        for loan in self:
            if loan.state != 'ongoing':
                continue
            other_ongoing = self.search(
                [
                    ('book_id', '=', loan.book_id.id),
                    ('state', '=', 'ongoing'),
                    ('id', '!=', loan.id),
                ]
            )
            if other_ongoing:
                raise ValidationError(
                    'This book is already on loan to another member.'
                )

    def action_mark_returned(self):
        for loan in self:
            loan.write(
                {
                    'state': 'returned',
                    'return_date': fields.Date.context_today(loan),
                }
            )
