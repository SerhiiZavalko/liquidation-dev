# -*- coding: utf-8 -*-
{
    'name': 'DGF: Enforcement',
    'summary': '''DGF Enforcement module''',
    'description': '''DGF Enforcement module''',
    'author': 'DGF',
    'website': 'https://fg.gov.ua',
    'license': 'AGPL-3',
    'version': '14.0.0.1',
    'category': 'Liquidation/Enforcement',
    'depends': [
        'base',
        'mail',
        'web',
        'contacts',
        'dgf_insolvent',
        'iap_alternative_provider'],
    'external_dependencies': {'python': [], 'bin': []},
    'data': [
        # 'security/groups.xml',
        # 'security/security_rules.xml',
        # 'views/res_config_settings.xml',
        'data/ir_config_settings_data.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/dgf_enforcement_views.xml',
        'views/dgf_enforcement_menus.xml',
    ],
    # 'demo': [],
    # 'qweb': [],
    # 'post_load': None,
    # 'pre_init_hook': None,
    # 'post_init_hook': None,
    # 'uninstall_hook': None,
    'auto_install': False,
    'application': True,
    'installable': True,
}
