# -*- coding: utf-8 -*-
from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    pages = fields.Integer(string='Pages')
    active = fields.Boolean(default=True)

    loan_ids = fields.One2many(
        'library.loan', 'book_id', string='Loan History'
    )
    is_available = fields.Boolean(
        string='Available', compute='_compute_is_available', store=True
    )

    @api.depends('loan_ids.state')
    def _compute_is_available(self):
        for book in self:
            open_loans = book.loan_ids.filtered(
                lambda l: l.state == 'ongoing'
            )
            book.is_available = not open_loans

    _isbn_unique = models.Constraint(
        'unique(isbn)',
        'A book with this ISBN already exists.',
    )
