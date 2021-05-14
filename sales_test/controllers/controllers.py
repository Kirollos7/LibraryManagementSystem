# -*- coding: utf-8 -*-
# from odoo import http


# class SalesTest(http.Controller):
#     @http.route('/sales_test/sales_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_test/sales_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_test.listing', {
#             'root': '/sales_test/sales_test',
#             'objects': http.request.env['sales_test.sales_test'].search([]),
#         })

#     @http.route('/sales_test/sales_test/objects/<model("sales_test.sales_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_test.object', {
#             'object': obj
#         })
