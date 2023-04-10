# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_rates_autoupdate = fields.Boolean(
        string="Automatic Currency Rates (OCA)",
        related="company_id.currency_rates_autoupdate",
        readonly=False,
        help="Enable regular automatic currency rates updates",
    )
