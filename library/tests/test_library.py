# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLibrary(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book = cls.env['library.book'].create(
            {'name': 'Test Book', 'author': 'Some Author', 'isbn': '1111111111'}
        )
        cls.member_alice = cls.env['library.member'].create({'name': 'Alice'})
        cls.member_bob = cls.env['library.member'].create({'name': 'Bob'})

    def test_book_available_by_default(self):
        self.assertTrue(self.book.is_available)

    def test_loan_marks_book_unavailable(self):
        self.env['library.loan'].create(
            {'book_id': self.book.id, 'member_id': self.member_alice.id}
        )
        self.assertFalse(self.book.is_available)

    def test_cannot_lend_book_already_on_loan(self):
        self.env['library.loan'].create(
            {'book_id': self.book.id, 'member_id': self.member_alice.id}
        )
        with self.assertRaises(ValidationError):
            self.env['library.loan'].create(
                {'book_id': self.book.id, 'member_id': self.member_bob.id}
            )

    def test_returning_book_makes_it_available_again(self):
        loan = self.env['library.loan'].create(
            {'book_id': self.book.id, 'member_id': self.member_alice.id}
        )
        loan.action_mark_returned()
        self.assertEqual(loan.state, 'returned')
        self.assertTrue(self.book.is_available)

    def test_is_overdue(self):
        yesterday = fields.Date.context_today(self.env.user) - timedelta(days=1)
        loan = self.env['library.loan'].create(
            {
                'book_id': self.book.id,
                'member_id': self.member_alice.id,
                'due_date': yesterday,
            }
        )
        self.assertTrue(loan.is_overdue)

    def test_returned_loan_is_never_overdue(self):
        yesterday = fields.Date.context_today(self.env.user) - timedelta(days=1)
        loan = self.env['library.loan'].create(
            {
                'book_id': self.book.id,
                'member_id': self.member_alice.id,
                'due_date': yesterday,
            }
        )
        loan.action_mark_returned()
        self.assertFalse(loan.is_overdue)

    def test_wizard_creates_loan(self):
        wizard = self.env['library.loan.wizard'].create(
            {'book_id': self.book.id, 'member_id': self.member_alice.id}
        )
        wizard.action_confirm()
        loans = self.env['library.loan'].search([('book_id', '=', self.book.id)])
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans.member_id, self.member_alice)

    def test_member_sees_only_own_loans(self):
        group_user = self.env.ref('library.group_library_user')
        user_alice = self.env['res.users'].create(
            {
                'name': 'Alice Login',
                'login': 'alice_test_login',
                'groups_id': [(6, 0, [group_user.id])],
            }
        )
        self.member_alice.user_id = user_alice.id

        loan_alice = self.env['library.loan'].create(
            {'book_id': self.book.id, 'member_id': self.member_alice.id}
        )
        other_book = self.env['library.book'].create({'name': 'Other Book'})
        loan_bob = self.env['library.loan'].create(
            {'book_id': other_book.id, 'member_id': self.member_bob.id}
        )

        visible_to_alice = self.env['library.loan'].with_user(user_alice).search([])
        self.assertIn(loan_alice, visible_to_alice)
        self.assertNotIn(loan_bob, visible_to_alice)
