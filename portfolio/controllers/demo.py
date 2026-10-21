from odoo import http
from odoo.exceptions import AccessDenied
from odoo.http import request

DEMO_ACCOUNTS = {
    'librarian': ('librarian', 'librarian', '/odoo/action-library.action_library_book'),
    'member': ('member', 'member', '/odoo/action-library.action_library_loan'),
}


class LibraryDemoController(http.Controller):

    def _enter(self, role):
        login, password, url = DEMO_ACCOUNTS[role]
        if request.session.uid:
            current = request.env.user.login
            if current == login or current not in DEMO_ACCOUNTS:
                return request.redirect(url)
        credential = {'login': login, 'password': password, 'type': 'password'}
        try:
            request.session.authenticate(request.env, credential)
        except AccessDenied:
            return request.redirect('/web/login')
        return request.redirect(url)

    @http.route('/demo', type='http', auth='public', website=True, sitemap=False)
    def library_demo(self, **kwargs):
        return self._enter('librarian')

    @http.route('/demo/member', type='http', auth='public', website=True, sitemap=False)
    def library_demo_member(self, **kwargs):
        return self._enter('member')
