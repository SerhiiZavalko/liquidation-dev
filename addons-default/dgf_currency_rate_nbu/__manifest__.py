# Copyright 2008-2016 Camptocamp
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Currency Rate Update (NBU)",
    "version": "14.0.1.1.1",
    "author": "Camptocamp, Brainbean Apps, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/currency",
    "license": "AGPL-3",
    "category": "Financial Management/Configuration",
    "summary": "Update exchange rates using OCA modules",
    "depends": ["base", "mail"],
    "data": [
        "data/cron.xml",
        "security/ir.model.access.csv",
        "security/res_currency_rate_provider.xml",
        "views/res_currency_rate.xml",
        "views/res_currency_views.xml",
        "views/res_currency_rate_provider.xml",
        "views/res_config_settings.xml",
        "wizards/res_currency_rate_update_wizard.xml",
        "views/res_currency_menu.xml",
    ],
    "installable": True,
}
