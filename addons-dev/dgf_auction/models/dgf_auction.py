# -*- coding: utf-8 -*-
import logging
from datetime import datetime
# from datetime import timezone
import time
import json

from odoo import api, fields, models, tools, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)
BASE_ENDPOINT = 'https://prozorro.sale/auction/'


class DgfAuction(models.Model):
    _name = 'dgf.auction'
    _description = 'Аукціон'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _inherits = {'dgf.asset': 'asset_id'}
    # _rec_name = 'name'
    _order = 'auctionPeriodStartDate desc'
    _check_company_auto = True
    _sql_constraints = [
        ('unq_aucId', 'unique(auctionId)', 'Дублі аукціонів (auctionId) не допускаються!'),
        ('unq__id', 'unique(_id)', 'Дублі аукціонів (_id) не допускаються!'),
    ]

    # def _get_default_stage_id(self):
    #     """ Gives default stage_id """
    #     project_id = self.env.context.get('default_project_id')
    #     if not project_id:
    #         return False
    #     return self.stage_find(project_id, [('fold', '=', False), ('is_closed', '=', False)])

    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     search_domain = [('id', 'in', stages.ids)]
    #     if 'default_project_id' in self.env.context:
    #         search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain

    #     stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
    #     return stages.browse(stage_ids)

    name = fields.Char(index=True, compute='_compute_name', store=True, readonly=True)
    _cdu = fields.Selection(
        [('1', 'ЦБД-1'), ('2', 'ЦБД-2'), ('3', 'ЦБД-3')],
        string='ЦБД',
        required=True,
        copy=False,
        default='3',
    )
    _id = fields.Char(string='Ідентифікатор технічний', index=True)
    datePublished = fields.Datetime(string='Дата публікації', help='Дата')
    dateModified = fields.Datetime(string='Дата зміни', help='Дата')
    auctionPeriodStartDate = fields.Datetime(
        string='Дата аукціону', help='Дата')
    auctionId = fields.Char(string='ID аукціону')
    previousAuctionId = fields.Char()
    sellingMethod = fields.Char(string='Метод аукціону', index=True)
    lotId = fields.Char(string='№ лоту в ЕТС', index=True)
    auction_lot_id = fields.Many2one('dgf.auction.lot', string='Лот з оренди')
    currency_id = fields.Many2one('res.currency', string='Валюта', default=lambda self: self.env.ref('base.UAH'))
    value_amount = fields.Float('Початкова ціна', digits=(15, 2))
    value_currency = fields.Char(related='currency_id.name', store=True)
    value_valueAddedTaxIncluded = fields.Boolean()
    valuePeriod = fields.Float('valuePeriod', digits=(15, 2))
    leaseDuration = fields.Float('leaseDuration', digits=(15, 2))
    status = fields.Char(string='Статус', index=True)
    stage_id = fields.Many2one('dgf.auction.stage', string='Статус', store=True, readonly=False, ondelete='restrict',
                               tracking=True, index=True,
                               # default=_get_default_stage_id, compute='_compute_stage_id',
                               # group_expand='_read_group_stage_ids',
                               domain="[]", copy=False)

    description = fields.Text('Опис аукціону')
    title = fields.Char('Заголовок')
    auctionUrl = fields.Char(string='Гіперпосилання на аукціон', readonly=True)
    owner = fields.Char('Майданчик')
    accessDetails = fields.Text()

    guarantee_amount = fields.Float(digits=(15, 2))
    guarantee_currency = fields.Char(related='currency_id.name', store=True)
    registrationFee_amount = fields.Float(digits=(15, 2))
    tenderAttempts = fields.Integer()

    partner_id = fields.Many2one('res.partner', string='Організатор', default=lambda self: self.env.company)
    company_id = fields.Many2one('res.company', string='Банк', required=True, default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='Відповідальний', required=False, default=lambda self: self.env.user)
    href = fields.Char(string='Гіперпосилання', compute='_compute_href', store=True, readonly=False)
    active = fields.Boolean(string='Активно', default=True, help='Чи є запис активним чи архівованим.')
    update_date = fields.Datetime(string='Оновлено', help='Дата оновлення через API')
    notes = fields.Text('Примітки')

    @api.depends('auctionId')
    def _compute_href(self):
        for item in self:
            item.href = '{0}{1}'.format(BASE_ENDPOINT, item.auctionId if item.auctionId is not False else '')

    @api.depends('auctionId')
    def _compute_name(self):
        for item in self:
            item.name = 'Аукціон № {}'.format(item.auctionId if item.auctionId is not False else '')

    # # do  not used
    # @api.depends('project_id')
    # def _compute_stage_id(self):
    #     for task in self:
    #         if task.project_id:
    #             if task.project_id not in task.stage_id.project_ids:
    #                 task.stage_id = task.stage_find(task.project_id.id, [
    #                     ('fold', '=', False), ('is_closed', '=', False)])
    #         else:
    #             task.stage_id = False

    # ----------------------------------------
    # Case management
    # ----------------------------------------

    # def stage_find(self, section_id, domain=[], order='sequence'):
    #     """ Override of the base.stage method
    #         Parameter of the stage search taken from the lead:
    #         - section_id: if set, stages must belong to this section or
    #           be a default stage; if not set, stages must be default
    #           stages
    #     """
    #     # collect all section_ids
    #     section_ids = []
    #     if section_id:
    #         section_ids.append(section_id)
    #     section_ids.extend(self.mapped('project_id').ids)
    #     search_domain = []
    #     if section_ids:
    #         search_domain = [('|')] * (len(section_ids) - 1)
    #         for section_id in section_ids:
    #             search_domain.append(('project_ids', '=', section_id))
    #     search_domain += list(domain)
    #     # perform search, return the first found
    #     return self.env['project.task.type'].search(search_domain, order=order, limit=1).id

    def prepare_data(self, responce):
        if responce is not None and responce['_id']:
            # datetime.now().replace(microsecond=0)
            # requestDate = fields.Datetime.now()
            dateModified = datetime.strptime(responce['dateModified'][:-1], '%Y-%m-%dT%H:%M:%S.%f') if responce['dateModified'] is not None else None
            datePublished = datetime.strptime(responce['datePublished'][:-1], '%Y-%m-%dT%H:%M:%S.%f') if responce['datePublished'] is not None else None
            auctionPeriodStartDate = datetime.strptime(responce['auctionPeriod']['startDate'][:-1], '%Y-%m-%dT%H:%M:%S.%f') if responce['auctionPeriod'] is not None else None
            sellingEntityId = responce['sellingEntity']['identifier']['id']
            sellingEntity = self.env['res.partner'].search([('vat', '=', sellingEntityId)])
            stage_id = self.env['dgf.auction.stage'].search([('code', '=', responce['status'])])

            # lot = self.env["dgf.auction.lot"].search([("name", "=", responce['lotId'])])
            # # [["name", "=", "156/23-1"]]
            # if lot.exists():
            #     auction_lot_id = lot.id
            # else:
            #     item = responce['items'][0]
            #     auction_lot = {
            #         'lotId': responce['lotId'],
            #         'name': responce['lotId'],
            #         'description': responce['title']['uk_UA'],
            #         'classification': item['classification']['id'],
            #         'additionalClassifications': item['additionalClassifications'][0]['id'],
            #         'quantity': item['quantity'],
            #     }
            #     auction_lot_id = lot.create(auction_lot).id

            result = {
                'update_date': datetime.utcnow().replace(microsecond=0),
                '_id': responce['_id'],
                'description': responce['description']['uk_UA'],
                'title': responce['title']['uk_UA'],
                'sellingMethod': responce['sellingMethod'],
                'dateModified': dateModified,
                'datePublished': datePublished,
                'auctionPeriodStartDate': auctionPeriodStartDate,
                'lotId': responce['lotId'],
                # 'auction_lot_id': auction_lot_id,
                'auctionId': responce['auctionId'],
                'value_amount': responce['value']['amount'],
                'auctionUrl': responce['auctionUrl'] if 'auctionUrl' in responce else None,
                'owner': responce['owner'],
                'status': responce['status'],
                'stage_id': stage_id.id,
                'partner_id': sellingEntity.id,
                'notes': json.dumps(responce, ensure_ascii=False, indent=4, sort_keys=True).encode('utf8')
            }
            return result

    def prepare_data_collection(self, responce):
        if responce is not None:
            records_inserted = 0
            records_updated = 0
            result = []
            for item in responce:
                value = self.prepare_data(item)
                record = self.search([('_id', '=', value['_id'])])
                if record.exists():
                    if record.status != value['status']:
                        record.write(value)
                        records_updated += 1
                else:
                    result.append(value)
                    records_inserted += 1
            result_data = {
                'records_inserted': records_inserted,
                'records_updated': records_updated,
                'result': result,
            }
            return result_data

    def search_byAuctionId(self):
        # TODO:
        responce = self.env['prozorro.api']._byAuctionId(auction_id=self.auctionId, description='Prozorro API')
        if responce is not None and responce['_id']:
            write_values = self.prepare_data(responce)
        else:
            write_values = {
                'status': responce['message'],
            }
        self.write(write_values)
        self.env.cr.commit()  # commit every record
        time.sleep(1)

    def search_byDateModified(self, date_modified=None):
        # TODO:
        # https://procedure-sandbox.prozorro.sale/api/search/byAuctionOrganizer/41902587?limit=10&date_modified=2023-03-15
        search_date = date_modified or '2021-03-01'
        params = {'limit': 10, 'date_modified': search_date, 'backward': False}
        responce = self.env['prozorro.api']._byDateModified(date_modified=search_date, params=params, description='Prozorro API')
        if responce is not None:
            write_values = self.prepare_data_collection(responce)['result']
        else:
            write_values = list({
                'status': responce['message'],
            })
        print(write_values)
        # self.write(write_values)
        # self.env.cr.commit()  # commit every record
        time.sleep(1)

    def search_byAuctionOrganizer(self, organizer_id=None, date_modified=None):
        limit = 100
        record_count = 100
        date_now = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        search_date = date_modified or date_now
        # https://procedure-sandbox.prozorro.sale/api/search/byAuctionOrganizer/21708016?limit=100&date_modified=2023-03-20
        records_inserted = 0
        records_updated = 0
        while record_count == 100:
            params = {'limit': limit, 'date_modified': search_date, 'backward': False}
            responce = self.env['prozorro.api']._byAuctionOrganizer(organizer_id=organizer_id, params=params, description='Prozorro API')
            if responce is not None:
                # TODO: refactor - join logic with 'search_byDateModified'
                data_collection = self.prepare_data_collection(responce)
                values = data_collection['result']
                records_inserted = records_inserted + int(data_collection['records_inserted'])
                records_updated = records_updated + int(data_collection['records_updated'])
            else:
                values = list({
                    'status': responce['message'],
                })
            if values:
                self.create(values)
            # self.env.cr.commit()  # commit every record

            record_count = len(responce)
            search_date = responce[record_count - 1]['dateModified']
            time.sleep(1)

        msg = _('Аукуціони організатора {0}. Оновлено: {1}; додано: {2}'.format(organizer_id, records_updated, records_inserted))
        _logger.info(msg)
        return msg

    def update_auction(self):
        # TODO:
        responce = self.env['prozorro.api']._update_auction_detail(_id=self._id, description='Prozorro API')
        if responce is not None and responce['_id']:
            write_values = self.prepare_data(responce)
        else:
            write_values = {
                'status': responce['message'],
            }
        self.write(write_values)
        self.env.cr.commit()  # commit every record
        # time.sleep(1)

    @api.model
    def _scheduled_update(self):
        _logger.info("Scheduled auction update...")
        records = self.search([('stage_id.is_closed', '!=', True)])
        for record in records:
            record.with_context({"scheduled": True}).update_auction()
        msg = _('Оновлено аукціонів: {}'.format(len(records)))
        _logger.info(msg)
        return msg

    @api.model
    def _scheduled_update_by_organizer(self):
        _logger.info("Scheduled auction update by organizer ...")
        date_now = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        records = self.env['res.partner'].search([('auction_ids', '!=', False)])
        for record in records:
            self.with_context({"scheduled": True}).search_byAuctionOrganizer(organizer_id=record.vat, date_modified=date_now)
        msg = _('Оновлено аукціони за організаторами: {}'.format(len(records)))
        _logger.info(msg)
        return msg

    @api.model
    def create(self, vals):
        if "auction_lot_id" not in vals:
            lot = self.env["dgf.auction.lot"].search([('lotId', '=', vals['lotId'])])
            # existing_lot = lot.search(['name', '=', vals['lotId']])
            if lot.exists():
                vals["auction_lot_id"] = lot.id
                # vals["company_id"] = lot.company_id.id
            else:
                data = json.loads(vals['notes'])
                item = data['items'][0]
                auction_lot = {
                    'lotId': vals['lotId'],
                    'name': vals['lotId'],  # переробити після зміни алгоритму
                    'description': vals['title'],
                    'classification': item['classification']['id'],
                    'additionalClassifications': item['additionalClassifications'][0]['id'],
                    'quantity': item['quantity'],
                    # 'auction_ids': [(6, 0, vals.ids)]
                }
                vals["auction_lot_id"] = lot.create(auction_lot).id
        return super().create(vals)

    def create_lot(self):
        if self.ids:
            domain = []
            fields = ["lotId"]
            counts_data = self.read_group(domain=domain, fields=fields, groupby='lotId')
            lots = self.env["dgf.auction.lot"].sudo()
            create_values = []
            for count in counts_data:
                # print('lotId={0}, count={1}'.format(count['lotId'], count['__domain']))
                auctions = self.search(count['__domain'])
                lot = auctions[0]
                data = json.loads(lot['notes'])
                item = data['items'][0]
                auction_lot = {
                    'lotId': lot['lotId'],
                    'name': lot['lotId'],
                    'description': lot['title'],
                    'classification': item['classification']['id'],
                    'additionalClassifications': item['additionalClassifications'][0]['id'],
                    'quantity': item['quantity'],
                    'auction_ids': [(6, 0, auctions.ids)]
                }
                print(auction_lot)
                create_values.append(auction_lot)
            lots.create(create_values)


class DgfAuctionStage(models.Model):
    _name = 'dgf.auction.stage'
    _description = 'Статус аукціону'
    _order = 'sequence, id'

    # def _get_default_project_ids(self):
    #     default_project_id = self.env.context.get('default_project_id')
    #     return [default_project_id] if default_project_id else None

    active = fields.Boolean('Active', default=True)
    code = fields.Char(string='Stage Code', required=True)
    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=[('model', '=', 'dgf.auction')],
        help="If set an email will be sent to the customer when the task or issue reaches this step.")
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    is_closed = fields.Boolean(
        'Closing Stage', help="Tasks in this stage are considered as closed.")

    # project_ids = fields.Many2many('project.project', 'project_task_type_rel', 'type_id', 'project_id', string='Projects',
    #     default=_get_default_project_ids)
    # legend_blocked = fields.Char(
    #     'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
    #     help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    # legend_done = fields.Char(
    #     'Green Kanban Label', default=lambda s: _('Ready'), translate=True, required=True,
    #     help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    # legend_normal = fields.Char(
    #     'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
    #     help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    # rating_template_id = fields.Many2one(
    #     'mail.template',
    #     string='Rating Email Template',
    #     domain=[('model', '=', 'project.task')],
    #     help="If set and if the project's rating configuration is 'Rating when changing stage', then an email will be sent to the customer when the task reaches this step.")
    # auto_validation_kanban_state = fields.Boolean('Automatic kanban status', default=False,
    #     help="Automatically modify the kanban state when the customer replies to the feedback for this stage.\n"
    #         " * A good feedback from the customer will update the kanban state to 'ready for the new stage' (green bullet).\n"
    #         " * A medium or a bad feedback will set the kanban state to 'blocked' (red bullet).\n")
    # disabled_rating_warning = fields.Text(compute='_compute_disabled_rating_warning')
    # def unlink_wizard(self, stage_view=False):
    #     self = self.with_context(active_test=False)
    #     # retrieves all the projects with a least 1 task in that stage
    #     # a task can be in a stage even if the project is not assigned to the stage
    #     readgroup = self.with_context(active_test=False).env['project.task'].read_group([('stage_id', 'in', self.ids)], ['project_id'], ['project_id'])
    #     project_ids = list(set([project['project_id'][0] for project in readgroup] + self.project_ids.ids))

    #     wizard = self.with_context(project_ids=project_ids).env['project.task.type.delete.wizard'].create({
    #         'project_ids': project_ids,
    #         'stage_ids': self.ids
    #     })

    #     context = dict(self.env.context)
    #     context['stage_view'] = stage_view
    #     return {
    #         'name': _('Delete Stage'),
    #         'view_mode': 'form',
    #         'res_model': 'project.task.type.delete.wizard',
    #         'views': [(self.env.ref('project.view_project_task_type_delete_wizard').id, 'form')],
    #         'type': 'ir.actions.act_window',
    #         'res_id': wizard.id,
    #         'target': 'new',
    #         'context': context,
    #     }

    # def write(self, vals):
    #     if 'active' in vals and not vals['active']:
    #         self.env['project.task'].search([('stage_id', 'in', self.ids)]).write({'active': False})
    #     return super(ProjectTaskType, self).write(vals)

    # @api.depends('project_ids', 'project_ids.rating_active')
    # def _compute_disabled_rating_warning(self):
    #     for stage in self:
    #         disabled_projects = stage.project_ids.filtered(lambda p: not p.rating_active)
    #         if disabled_projects:
    #             stage.disabled_rating_warning = '\n'.join('- %s' % p.name for p in disabled_projects)
    #         else:
    #             stage.disabled_rating_warning = False
