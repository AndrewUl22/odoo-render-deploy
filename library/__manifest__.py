{
    'name': 'Library',
    'version': '1.0',
    'summary': 'Training module: library book management',
    'description': """
Training module for practicing the Odoo framework.
Includes:
- library.book (books)
- library.member (members, delegated from res.partner via _inherits)
- library.loan (book loans)
- Two security groups (User / Librarian) with record rules,
  so a regular member only sees their own loans
- A "Lend a Book" wizard for creating loans
- A PDF "Reading Card" report per member
- Demo data (a handful of books, members, and loans)
""",
    'category': 'Tools',
    'author': 'Andrew',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_loan_views.xml',
        'wizards/library_loan_wizard_views.xml',
        'views/library_menus.xml',
        'reports/library_member_reports.xml',
    ],
    'demo': [
        'data/library_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
