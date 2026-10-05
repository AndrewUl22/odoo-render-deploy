# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PortfolioController(http.Controller):

    @http.route('/portfolio', type='http', auth='public', website=True, sitemap=True)
    def portfolio_page(self, **kwargs):
        """Public portfolio page, accessible without login."""
        values = {
            'name': 'Andrii Ulianov',
            'tagline': 'Full-Stack JS Developer (React / Next.js / Node.js) — Aspiring Odoo Developer',
            'github_url': 'https://github.com/AndrewUl22',
            'linkedin_url': 'https://www.linkedin.com/in/andr%C3%A9-ulianov-717933337/',
            'email': 'anulian22@gmail.com',
            'phone': '+32 465 987 301',
            'skills': [
                'Python', 'Odoo ORM', 'PostgreSQL',
                'XML Views', 'JavaScript', 'Owl Framework',
            ],
            'certificate': {
                'title': 'Fullstack Developer Course',
                'issuer': 'GoIT',
                'date': '24/06/2026',
                'hours': 872,
                'unique_id': '46399',
            },
            'other_projects': [
                {
                    'name': 'TravelTrucks RoadNest',
                    'description': 'Camper rental app: filterable catalog, infinite loading, '
                                    'gallery, reviews, and a booking form.',
                    'stack': 'Next.js 16, React 19, TypeScript, TanStack Query, Swiper',
                    'demo_url': 'https://travel-trucks-road-nest.vercel.app/',
                    'github_url': 'https://github.com/AndrewUl22/TravelTrucks-RoadNest',
                },
                {
                    'name': 'LearnLingo',
                    'description': 'Language tutor booking platform with Firebase auth, '
                                    'filterable teacher catalog, and favorites.',
                    'stack': 'React 19, Vite, Firebase, React Hook Form + Yup',
                    'demo_url': 'https://learn-lingo-gamma-ruby.vercel.app/',
                    'github_url': 'https://github.com/AndrewUl22/LearnLingo',
                },
                {
                    'name': 'VocabBuilder',
                    'description': 'Vocabulary trainer: personal dictionary, community word '
                                    'recommendations, and quiz-based training.',
                    'stack': 'React 19, Vite, Redux Toolkit, Axios',
                    'demo_url': 'https://vocab-builder-weld.vercel.app/',
                    'github_url': 'https://github.com/AndrewUl22/Vocab-builder',
                },
            ],
        }
        return request.render('portfolio.portfolio_page_template', values)
