# -*- coding: utf-8 -*-

# from lxml import etree  # dynamic field label
import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError


class DgfAsset(models.Model):
    _name = 'dgf.asset'
    _description = 'Актив'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'base.stage.abstract',
        ]
    _order = "sku"
    is_base_stage = True
    # _rec_name = 'name'
    _check_company_auto = True

    name = fields.Char(string="Найменування", index=True, compute='_compute_name', store=False, readonly=False)
    type_id = fields.Many2one(
        comodel_name='dgf.asset.category', string='Тип активу',
        ondelete='restrict',
        context={},
        domain=[('is_group', '=', False)],)
    group_id = fields.Many2one(string='Група активу', related='type_id.parent_id', store=True, readonly=True)
    bal_account = fields.Char(index=True, string="Балансовий рахунок")
    sku = fields.Char(index=True, string="Номер активу",help="Номер активу (інвентарний, номер договору тощо)")
    dateonbalance = fields.Date(index=True, string='Дата набуття', help="Дата активу (дата оприбуткування на баланс, дата договору тощо)")
    currency_id = fields.Many2one('res.currency', required=True, string='Валюта', default=lambda self: self.env.ref('base.UAH'))
    book_value = fields.Float(string='Балансова вартість', digits=(15, 2))
    # book_value = fields.Monetary(string='Балансова вартість', currency_field='currency_id', store=True) # , compute='_compute_book_value'
    apprisal_value = fields.Float(string='Оціночна вартість', digits=(15, 2))
    partner_id = fields.Many2one('res.partner', string='Контрагент')
    partner_vat = fields.Char(string='Код контрагента', related='partner_id.vat', readonly=True)
    company_id = fields.Many2one('res.company', string='Банк', required=True, default=lambda self: self.env.company)
    odb_id = fields.Char(index=True, string="ID активу в ОДБ")
    eois_id = fields.Char(index=True, string="ID активу в ЄОІС")
    is_liquidpool = fields.Boolean(default=True, string='Включено в ЛМ', help="Чи включено актив до ліквідаційної маси.")
    stage_id = fields.Many2one(string='Статус')
    active = fields.Boolean(default=True, string='Активно', help="Чи є запис активним чи архівованим.")
    description = fields.Text('Опис активу')
    notes = fields.Text('Примітки')

    # @api.onchange('company_id')
    # def _onchange_company_id(self):
    #     for record in self:
    #         return {domain:{[('company_id', '=', record.company_id)]}}

    @api.depends('sku', 'group_id')
    def _compute_name(self):
        for item in self:
            item.name = '{0} №{1}'.format(item.group_id.name, item.sku)



    # def action_update_invoice_date(self):
    #     selected_assets = self.ids
    #     print(len(selected_assets))
    #     print(selected_assets)
    #     self.write({'datesale1': fields.Date.today()})

# Перемістити в розширення Активи-Аукціони
    # def action_create_lot(self):
    #     # selected_assets = self.ids
    #     active_ids = self.env.context.get('active_ids', [])
    #     lines = []
    #     for item in active_ids:
    #         line = (0, 0, {'asset_id': item})
    #         lines.append(line)
    #     # print('Records selected: {}'.format(len(active_ids)))
    #     return {
    #         'name': 'Лот',
    #         'view_type': 'form',
    #         'res_model': 'dgf.auction.lot',
    #         'view_id': False,
    #         'view_mode': 'form',
    #         # 'target': 'new',
    #         'context': {
    #             'default_asset_ids': lines
    #         },
    #         'type': 'ir.actions.act_window'
    #     }


    # # dynamic field label
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     result = super(DgfAsset, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     if view_type == 'form':
    #         doc = etree.XML(result['arch'])
    #         field = doc.xpath("//field[@name='sku']")
    #         if field:
    #             print(self.type_id)
    #             field[0].set("string", "Динамічний Номер активу")
    #             # sale_reference[0].addnext(etree.Element('label', {'string': 'Sale Reference Number'}))
    #             result['arch'] = etree.tostring(doc, encoding='unicode')
    #     return result


class DgfAssetCategory(models.Model):
    _description = 'Категорії активів'
    _name = 'dgf.asset.category'
    _order = 'sequence'
    _parent_store = True

    sequence = fields.Integer('Послідовність', default=10)
    name = fields.Char(string='Найменування', required=True)
    complete_name = fields.Char('Повне найменування', compute='_compute_complete_name', store=True)
    code = fields.Char(string='Код', required=False)
    is_group = fields.Boolean(default=False, string='Група', help="Ознака групи активів.")
    active = fields.Boolean(default=True, string='Активно', help="Чи є запис активним чи архівованим.")
    parent_id = fields.Many2one('dgf.asset.category', string='Батьківська категорія', ondelete='cascade')  # index=True,
    parent_path = fields.Char()  # index=True
    child_ids = fields.One2many('dgf.asset.category', 'parent_id', string='Дочірні категорії')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
