# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': "Product Supply",
    'summary': """
    """,
    'description': """
    """,
    'author': "Humanytek",
    'website': "http://www.humanytek.com",
    'category': 'Manufacturing',
    'version': '1.0.0',
    'depends': [
        'mrp',
        'mrp_workorder',
        'sale_order_observation',
        'product_brand',
    ],
    'data': [
        'report/product_supply_report.xml',
        'report/supply_report_templates.xml',
        'view/stock_view.xml',
        'wizard/product_supply_view.xml',
    ],
    'demo': [
    ],
}
