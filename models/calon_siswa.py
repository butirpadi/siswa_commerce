# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import calendar


class calon_siswa(models.Model):
    _inherit = 'siswa_psb_ocb11.calon_siswa'
    
    def action_confirm(self):
        # check pembayaran is set or not
        if len(self.biaya_lines) > 0:
            # register siswa to res.partner
            if self.is_siswa_lama:
                # update siswa lama
                self.env['res.partner'].search([('id', '=', self.siswa_id.id)]).write({
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa_lama' : True,
                    'calon_siswa_id' : self.id,
                })
            else:
                # insert into res_partner
                new_siswa = self.env['res.partner'].create({
                    'is_customer' : 1,
                    'name' : self.name,
                    'calon_siswa_id' : self.id,
                    'street' : self.street,
                    'street2' : self.street2,
                    'zip' : self.zip,
                    'city' : self.city,
                    'state_id' : self.state_id.id,
                    'country_id' : self.country_id.id,
                    'phone' : self.phone,
                    'mobile' : self.mobile,
                    'tanggal_registrasi' : self.tanggal_registrasi,
                    'tahunajaran_id' : self.tahunajaran_id.id,
                    'nis' : self.nis,
                    'panggilan' : self.panggilan,
                    'jenis_kelamin' : self.jenis_kelamin,
                    'tanggal_lahir' : self.tanggal_lahir,
                    'tempat_lahir' : self.tempat_lahir,
                    'alamat' : self.alamat,
                    'telp' : self.telp,
                    'ayah' : self.ayah,
                    'pekerjaan_ayah_id' : self.pekerjaan_ayah_id.id,
                    'telp_ayah' : self.telp_ayah,
                    'ibu' : self.ibu,
                    'pekerjaan_ibu_id' : self.pekerjaan_ibu_id.id,
                    'telp_ibu' : self.telp_ibu,
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa' : True,
                    'anak_ke' : self.anak_ke,
                    'dari_bersaudara' : self.dari_bersaudara
                })
                # self.siswa_id = new_siswa.id 
                self.registered_siswa_id = new_siswa.id
                # self.siswa_id = new_siswa.id

            # update state
            self.state = 'reg'

            # assign siswa biaya
            # get tahunajaran_jenjang
            ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([('tahunajaran_id', '=', self.tahunajaran_id.id),
            ('jenjang_id', '=', self.jenjang_id.id)
            ])

            # assign biaya to siswa
            total_biaya = 0.0
            if self.is_siswa_lama:
                id_siswa = self.siswa_id.id
            else:
                id_siswa = new_siswa.id

            for by in ta_jenjang.biayas:

#                 # cek biaya apakah is_optional dan apakah di pilih dalam biaya_lines
#                 by_found = False
#                 if by.biaya_id.is_optional:
#                     for by_in_pay in self.biaya_lines:
#                         if by.biaya_id.id == by_in_pay.biaya_id.id:
#                             by_found = True
#                     if not by_found:
#                         continue

                if self.is_siswa_lama and by.biaya_id.is_siswa_baru_only:
                    print('skip')
                    continue
                else:
                    print('JENJANG ID : ' + str(self.jenjang_id.id))
                    if by.biaya_id.is_bulanan:
                        for bulan_index in range(1, 13):
                            harga = by.harga

                            if by.is_different_by_gender:
                                if self.jenis_kelamin == 'perempuan':
                                    harga = by.harga_alt

                            self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                'siswa_id' : id_siswa,
                                'tahunajaran_id' : self.tahunajaran_id.id,
                                'biaya_id' : by.biaya_id.id,
                                'bulan' : bulan_index,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.jenjang_id.id
                            })

                            # create product on sales
                            self.env['product.template'].create({
                                'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                'siswa_id' : id_siswa,
                                'tahunajaran_id' : self.tahunajaran_id.id,
                                'biaya_id' : by.biaya_id.id,
                                'bulan' : bulan_index,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.jenjang_id.id,
                                'type' : 'service',
                                'list_price' : harga
                            })
                            
                            
                            
                            total_biaya += harga
                    else:
                        harga = by.harga

                        if by.is_different_by_gender:
                            if self.jenis_kelamin == 'perempuan':
                                harga = by.harga_alt

                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : by.biaya_id.name,
                            'siswa_id' : id_siswa,
                            'tahunajaran_id' : self.tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.jenjang_id.id
                        })
                        
                        # create product on sales
                        self.env['product.template'].create({
                            'name' : by.biaya_id.name ,
                            'siswa_id' : id_siswa,
                            'tahunajaran_id' : self.tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.jenjang_id.id,
                            'type' : 'service',
                            'list_price' : harga
                        })
                        
                        total_biaya += harga

            # set total_biaya dan amount_due
            # total_biaya = sum(by.harga for by in self.biayas)
            print('ID SISWA : ' + str(id_siswa))
            res_partner_siswa = self.env['res.partner'].search([('id', '=', id_siswa)])
            self.env['res.partner'].search([('id', '=', id_siswa)]).write({
                'total_biaya' : total_biaya,
                'amount_due_biaya' : res_partner_siswa.amount_due_biaya + total_biaya,
            })

#             # add pembayaran
#             pembayaran = self.env['siswa_keu_ocb11.pembayaran'].create({
#                 'tanggal' : self.tanggal_registrasi ,
#                 'tahunajaran_id' : self.tahunajaran_id.id,
#                 'siswa_id' : id_siswa,
#             })
# 
#             # reset pembayaran_lines
#             pembayaran.pembayaran_lines.unlink()
#             pembayaran.total = 0
# 
#             total_bayar = 0.0
#             for pay in self.biaya_lines:
# 
#                 print('Payment Lines : ')
#                 print('harga : ' + str(pay.harga))
#                 print('dibayar : ' + str(pay.dibayar))
#                 print('biaya_id : ' + str(pay.biaya_id.id))
# 
#                 # get siswa_biaya
#                 if pay.dibayar > 0:  # jangan dimasukkan ke pembayaran untuk yang nilai dibayarnya = 0
#                     if pay.biaya_id:
#                         if pay.biaya_id.is_bulanan:
#                             pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
#                                         ('siswa_id', '=', id_siswa),
#                                         ('tahunajaran_id', '=', self.tahunajaran_id.id),
#                                         ('biaya_id', '=', pay.biaya_id.id),
#                                         ('tahunajaran_id', '=', self.tahunajaran_id.id),
#                                         ('bulan', '=', pay.bulan),
#                                         ]).id
#                         else:
#                             pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
#                                         ('siswa_id', '=', id_siswa),
#                                         ('tahunajaran_id', '=', self.tahunajaran_id.id),
#                                         ('biaya_id', '=', pay.biaya_id.id),
#                                         ('tahunajaran_id', '=', self.tahunajaran_id.id),
#                                         ]).id
# 
#                         pembayaran.pembayaran_lines = [(0, 0, {
#                                                 'biaya_id' : pay_biaya_id,
#                                                 'bayar' : pay.dibayar
#                                                 })]
#                         total_bayar += pay.dibayar
# 
#                 print('pay_biaya_id : ' + str(pay_biaya_id))
#                 print('-------------------')
# 
#             # raise exceptions.except_orm(_('Warning'), _('TEST ERROR'))
# 
#             # confirm pembayaran 
#             pembayaran.action_confirm()
# 
#             # set terbilang
#             if total_bayar == 0:
#                 self.terbilang = 'nol'
#             else:
#                 t = self.terbilang_(total_bayar)
#                 while '' in t:
#                     t.remove('')
#                 self.terbilang = ' '.join(t)
# 
#             self.terbilang += ' Rupiah'
#             # set total
#             self.total = total_bayar

            # raise exceptions.except_orm(_('Warning'), _('You can not delete Done state data'))
        else:
            raise exceptions.except_orm(_('Warning'), _('Can not confirm this registration, complete payment first!')) 