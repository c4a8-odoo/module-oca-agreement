# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Legal Content",
    "summary": "Dynamic placeholder content and PDF report for legal agreements",
    "author": "Pavlov Media, "
    "Open Source Integrators, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement_legal"],
    "data": [
        "security/ir.model.access.csv",
        "report/agreement.xml",
        "views/agreement_section.xml",
        "views/agreement_clause.xml",
        "views/agreement_recital.xml",
        "views/agreement_appendix.xml",
        "views/agreement.xml",
        "views/menu.xml",
        "wizards/recompute_agreement_from_template_wizard.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
