# -*- coding: utf-8 -*-
from flectra import http

# class SiswaCommerce(http.Controller):
#     @http.route('/siswa_commerce/siswa_commerce/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/siswa_commerce/siswa_commerce/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('siswa_commerce.listing', {
#             'root': '/siswa_commerce/siswa_commerce',
#             'objects': http.request.env['siswa_commerce.siswa_commerce'].search([]),
#         })

#     @http.route('/siswa_commerce/siswa_commerce/objects/<model("siswa_commerce.siswa_commerce"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('siswa_commerce.object', {
#             'object': obj
#         }) 