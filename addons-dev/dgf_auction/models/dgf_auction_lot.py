# -*- coding: utf-8 -*-
from datetime import datetime
# from datetime import timezone
import time
# import json

from odoo import models, fields, api

BASE_ENDPOINT = 'https://prozorro.sale/auction/'


class DgfAuctionLot(models.Model):
    _name = 'dgf.auction.lot'
    _description = 'Лот аукціону'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # domain = [('type_id', 'in', (101, 102))]

    name = fields.Char(index=True, compute='_compute_name',
                       store=True, readonly=False)
    _id = fields.Char(string='Ідентифікатор технічний', index=True)

    classification = fields.Char(string='CAV', help="CAV")
    additionalClassifications = fields.Char(
        string='CPVS', help="CPVS", index=True)
    lotId = fields.Char(string='Номер лоту', index=True)
    code = fields.Char(string='Лот №', readonly=True, copy=False, store=True)

    description = fields.Text(string='Опис', index=True)
    start_value_amount = fields.Float(digits=(15, 2))
    location_latitude = fields.Float(digits=(2, 6))
    location_longitude = fields.Float(digits=(2, 6))
    quantity = fields.Float(digits=(5, 2))

    registrationDate = dateModified = fields.Date(help="Дата реєстрації")
    registrationID = fields.Char(
        string='registrationID', help="registrationID")
    registrationStatus = fields.Char(
        string='registrationStatus', help="registrationStatus")
    regulationsPropertyLeaseItemType = fields.Char(
        string='regulationsPropertyLeaseItemType', help="regulationsPropertyLeaseItemType")

    auction_count = fields.Integer(
        string="Кількість аукціонів", compute='_compute_auction_count', store=False)
    company_id = fields.Many2one(
        'res.company', string='Банк', required=True)  # , default=lambda self: self.env.company
    # href = fields.Char(string="Гіперпосилання", compute='_compute_href', store=True, readonly=True)
    active = fields.Boolean(default=True, string='Активно',
                            help="Чи є запис активним чи архівованим.")
    notes = fields.Text('Примітки')

    # asset_id = fields.Many2one('dgf.asset', required=True, ondelete='cascade', delegate=True, string="Картка активу")  # alternative to _inherits class attribute
    # reg_num = fields.Char(string="Реєстраційний номер")
    # living_area = fields.Float('Житлова площа', digits=(10, 4))
    # total_area = fields.Float('Загальна площа', digits=(10, 4))
    # register_type_id = fields.Many2one(
    #     comodel_name='stat.classifier.item', string='Тип реєстру',
    #     ondelete='restrict',
    #     context={},
    #     domain=[('classifier_code', '=', 'register_type')],)
    # cad_num = fields.Char(string="Кадастровий номер", index=True, help="Кадастровий номер земельної ділянки")

    # @api.depends('auctionId')
    # def _compute_href(self):
    #     for item in self:
    #         item.href = BASE_ENDPOINT + item.auctionId

    @api.depends('lotId')
    def _compute_name(self):
        pass
        # for item in self:
        #     a_id = item.auctionId if item.auctionId is not False else ''
        #     item.name = 'Аукціон №{}'.format(a_id)

    @api.model
    def create(self, vals):
        # if vals.get("code", "/") == "/":
        #     team_id = vals.get("maintenance_team_id")
        #     sequence = self.env["maintenance.team"].browse(
        #         team_id
        #     ).sequence_id or self.env.ref(
        #         "maintenance_request_sequence.seq_maintenance_request_auto"
        #     )
        #     vals["code"] = sequence.next_by_id()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        use_rent_lot_sequense = bool(IrConfigParameter.get_param("dgf_auction.use_rent_lot_sequense"))
        if use_rent_lot_sequense:
            rent_lot_sequence_id = int(IrConfigParameter.get_param("dgf_auction.rent_lot_sequence_id"))
            sequence = self.env["ir.sequence"].browse(rent_lot_sequence_id)
            if rent_lot_sequence_id:
                vals["code"] = sequence.next_by_id()
        return super().create(vals)

    def _compute_lot_number(self):
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        use_rent_lot_sequense = bool(IrConfigParameter.get_param("dgf_auction.use_rent_lot_sequense"))
        if use_rent_lot_sequense:
            rent_lot_sequence_id = IrConfigParameter.get_param("dgf_auction.rent_lot_sequence_id")
            if rent_lot_sequence_id:
                self.code = rent_lot_sequence_id.next_by_id()
        else:
            pass

    def _compute_auction_count(self):
        if self.ids:
            domain = [('auction_lot_id', 'in', self.ids)]
            auction = self.env['dgf.auction']
            counts_data = auction.read_group(
                domain, ['auction_lot_id'], ['auction_lot_id'])
            mapped_data = {
                count['auction_lot_id'][0]: count['auction_lot_id_count'] for count in counts_data
            }
        else:
            mapped_data = {}
        for record in self:
            record.auction_count = mapped_data.get(record.id, 0)

        # for record in self:
        #     record.auction_count = auction.search_count(
        #         [('auction_lot_id', '=', self.id)])
