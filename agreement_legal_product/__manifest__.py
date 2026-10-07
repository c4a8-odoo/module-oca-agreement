# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreements Legal - Products/Services",
    "summary": "Add products and services to legal agreements",
    "author": "Pavlov Media, Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement_legal", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/agreement.xml",
        "views/menu.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
