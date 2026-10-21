from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestDemoRoles(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        base_user = cls.env.ref('base.group_user')
        cls.librarian = cls.env['res.users'].create(
            {
                'name': 'Test Librarian',
                'login': 'test_librarian',
                'password': 'test_librarian_password',
                'group_ids': [
                    (6, 0, [
                        base_user.id,
                        cls.env.ref('library.group_library_manager').id,
                    ])
                ],
            }
        )
        cls.reader = cls.env['res.users'].create(
            {
                'name': 'Test Reader',
                'login': 'test_reader',
                'password': 'test_reader_password',
                'group_ids': [
                    (6, 0, [
                        base_user.id,
                        cls.env.ref('library.group_library_user').id,
                    ])
                ],
            }
        )
        cls.book_1 = cls.env['library.book'].create(
            {'name': 'Role Book 1', 'isbn': '4444444441'}
        )
        cls.book_2 = cls.env['library.book'].create(
            {'name': 'Role Book 2', 'isbn': '4444444442'}
        )
        cls.alice = cls.env['library.member'].create(
            {'name': 'Alice Reader', 'user_id': cls.reader.id}
        )
        cls.bob = cls.env['library.member'].create({'name': 'Bob Other'})
        cls.loan_alice = cls.env['library.loan'].create(
            {'book_id': cls.book_1.id, 'member_id': cls.alice.id}
        )
        cls.loan_bob = cls.env['library.loan'].create(
            {'book_id': cls.book_2.id, 'member_id': cls.bob.id}
        )

    def test_librarian_sees_all_loans(self):
        loans = self.env['library.loan'].with_user(self.librarian).search(
            [('id', 'in', (self.loan_alice | self.loan_bob).ids)]
        )
        self.assertEqual(len(loans), 2)

    def test_librarian_manages_books(self):
        books = self.env['library.book'].with_user(self.librarian)
        book = books.create({'name': 'Temporary Book', 'isbn': '4444444443'})
        book.write({'name': 'Renamed Book'})
        self.assertEqual(book.name, 'Renamed Book')
        book.unlink()
        self.assertFalse(book.exists())

    def test_member_sees_only_own_loans(self):
        loans = self.env['library.loan'].with_user(self.reader).search(
            [('id', 'in', (self.loan_alice | self.loan_bob).ids)]
        )
        self.assertEqual(loans, self.loan_alice)

    def test_member_cannot_read_other_loan(self):
        with self.assertRaises(AccessError):
            self.loan_bob.with_user(self.reader).read(['state'])
