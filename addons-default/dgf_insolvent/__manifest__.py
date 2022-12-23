# -*- coding: utf-8 -*-
{
    'name': 'DGF: Insolvents',
    'summary': '''DGF Insolvents module''',
    'description': '''DGF Insolvents module''',
    'author': 'DGF',
    'website': 'https://fg.gov.ua',
    'license': 'AGPL-3',
    'version': '15.0.0.1',
    'category': 'Liquidation/Insolvents',
    'depends': [
        'base',
        'mail',
        'web',
        'contacts'],
    'external_dependencies': {'python': [], 'bin': []},
    'data': [
        'security/groups.xml',
        'security/security_rules.xml',
        # 'views/res_config_settings.xml',
        'security/ir.model.access.csv',
        'data/generic_dictionary.xml',  # 'data/generic.dictionary.csv',
        'data/res_partner_category.xml',  # 'data/res.partner.category.csv',
        'data/res_partner.xml',  # 'data/res.partner.csv',
        'data/res_company.xml',  # 'data/res.company.csv',
        'views/generic_gictionary_views.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/ir_logging_views.xml',
        'views/dgf_insolvents_views.xml',
        'views/dgf_insolvents_menus.xml',
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
