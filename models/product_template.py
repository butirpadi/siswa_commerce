# -*- coding: utf-8 -*-
# Part of Flectra. See LICENSE file for full copyright and licensing details.

import itertools
import psycopg2

from flectra.addons import decimal_precision as dp

from flectra import api, fields, models, tools, _
from flectra.exceptions import ValidationError, RedirectWarning, except_orm
from flectra.tools import pycompat
from pprint import pprint


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    siswa_id = fields.Many2one('res.partner', string="Siswa")
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran")
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', ondelete='restrict')
    amount_due = fields.Float('Amount Due',  default=0.0)
    dibayar = fields.Float('Dibayar',  default=0)
    state = fields.Selection([('open', 'Open'), ('paid', 'Paid')], string='Paid',  default='open')
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang')
    bulan = fields.Selection([(0, 'Bulan'), 
                            (1, 'Januari'),
                            (2, 'Februari'),
                            (3, 'Maret'),
                            (4, 'April'),
                            (5, 'Mei'),
                            (6, 'Juni'),
                            (7, 'Juli'),
                            (8, 'Agustus'),
                            (9, 'September'),
                            (10, 'Oktober'),
                            (11, 'November'),
                            (12, 'Desember'),
                            ], string='Bulan', default=0)
#     potongan_ids = fields.One2many('siswa_keu_ocb11.siswa.potongan_biaya',inverse_name='siswa_biaya_id')
    potongan_id = fields.Many2one('siswa_keu_ocb11.siswa.potongan_biaya', string="Potongan")
    



     