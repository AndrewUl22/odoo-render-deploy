# -*- coding: utf-8 -*-
from odoo import api, fields, models


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherits = {'res.partner': 'partner_id'}
    _order = 'name'

    partner_id = fields.Many2one(
        'res.partner',
        string='Related Contact',
        required=True,
        ondelete='restrict',
        auto_join=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Related User',
        help='Restricts this member to seeing only their own loans.',
    )

    loan_ids = fields.One2many(
        'library.loan', 'member_id', string='Loans'
    )
    loan_count = fields.Integer(
        string='Active Loans', compute='_compute_loan_count'
    )

    @api.depends('loan_ids.state')
    def _compute_loan_count(self):
        for member in self:
            member.loan_count = len(
                member.loan_ids.filtered(lambda l: l.state == 'ongoing')
            )
