{
    'name': 'Portfolio',
    'version': '1.0',
    'summary': 'Public portfolio page built on Odoo technology (Website + QWeb)',
    'description': """
Training module: a portfolio page embedded in Odoo Website.
Showcases the library project (models, repository) + basic info about me.
""",
    'category': 'Website',
    'author': 'Andrew',
    'depends': ['website'],
    'data': [
        'views/portfolio_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'portfolio/static/src/css/portfolio.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
