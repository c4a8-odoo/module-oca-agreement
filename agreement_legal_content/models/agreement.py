# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ["agreement", "agreement.dynamic.content.mixin"]

    use_parties_content = fields.Boolean(help="Use custom content for parties")

    def _get_default_parties(self):
        deftext = """
        <h3>Company Information</h3>
        <p>
        {{object.company_id.partner_id.name or ''}}.<br>
        {{object.company_id.partner_id.street or ''}} <br>
        {{object.company_id.partner_id.state_id.code or ''}}
        {{object.company_id.partner_id.zip or ''}}
        {{object.company_id.partner_id.city or ''}}<br>
        {{object.company_id.partner_id.country_id.name or ''}}.<br><br>
        Represented by <b>{{object.company_contact_id.name or ''}}.</b>
        </p>
        <p></p>
        <h3>Partner Information</h3>
        <p>
        {{object.partner_id.name or ''}}.<br>
        {{object.partner_id.street or ''}} <br>
        {{object.partner_id.state_id.code or ''}}
        {{object.partner_id.zip or ''}} {{object.partner_id.city or ''}}<br>
        {{object.partner_id.country_id.name or ''}}.<br><br>
        Represented by <b>{{object.partner_contact_id.name or ''}}.</b>
        </p>
        """
        return deftext

    parties = fields.Html(
        default=lambda self: self._get_default_parties(),
        help="Parties of the agreement",
    )
    recital_ids = fields.One2many(
        "agreement.recital", "agreement_id", string="Recitals", copy=True
    )
    sections_ids = fields.One2many(
        "agreement.section", "agreement_id", string="Sections", copy=True
    )
    clauses_ids = fields.One2many("agreement.clause", "agreement_id", string="Clauses")
    appendix_ids = fields.One2many(
        "agreement.appendix", "agreement_id", string="Appendices", copy=True
    )
    dynamic_description = fields.Text(
        compute="_compute_dynamic_description", help="Compute dynamic description"
    )
    dynamic_parties = fields.Html(
        compute="_compute_dynamic_parties", help="Compute dynamic parties"
    )
    dynamic_special_terms = fields.Text(
        compute="_compute_dynamic_special_terms", help="Compute dynamic special terms"
    )

    def recompute_from_template(self):
        res = super().recompute_from_template()
        if self.template_id:
            template = self.template_id
            self.recital_ids.unlink()
            self.sections_ids.unlink()
            self.clauses_ids.unlink()
            self.appendix_ids.unlink()

            for recital in template.recital_ids:
                recital.copy({"agreement_id": self.id})

            section_map = {}
            for section in template.sections_ids:
                new_section = section.copy(
                    {
                        "agreement_id": self.id,
                        # Copy clauses explicitly below to avoid duplicated clauses.
                        "clauses_ids": False,
                    }
                )
                section_map[section.id] = new_section.id
            for clause in template.clauses_ids:
                values = {"agreement_id": self.id}
                if clause.section_id:
                    values["section_id"] = section_map.get(clause.section_id.id)
                clause.copy(values)
            for appendix in template.appendix_ids:
                appendix.copy({"agreement_id": self.id})
        return res

    def copy(self, default=None):
        res = super().copy(default)
        section_map = {}
        for section in self.sections_ids:
            new_section = section.copy(
                {
                    "agreement_id": res.id,
                    "clauses_ids": False,
                }
            )
            section_map[section.id] = new_section.id
        for clause in self.clauses_ids:
            values = {"agreement_id": res.id}
            if clause.section_id:
                values["section_id"] = section_map.get(clause.section_id.id)
            clause.copy(values)
        return res

    # compute the dynamic content for jinja expression
    def _compute_dynamic_description(self):
        MailTemplates = self.env["mail.template"]
        for agreement in self:
            lang = agreement.partner_id.lang or "en_US"
            description = MailTemplates.with_context(lang=lang)._render_template(
                agreement.description, "agreement", [agreement.id]
            )[agreement.id]
            agreement.dynamic_description = description

    def _compute_dynamic_parties(self):
        MailTemplates = self.env["mail.template"]
        for agreement in self:
            lang = agreement.partner_id.lang or "en_US"
            parties = MailTemplates.with_context(lang=lang)._render_template(
                agreement.parties, "agreement", [agreement.id]
            )[agreement.id]
            agreement.dynamic_parties = parties

    def _compute_dynamic_special_terms(self):
        MailTemplates = self.env["mail.template"]
        for agreement in self:
            lang = agreement.partner_id.lang or "en_US"
            special_terms = MailTemplates.with_context(lang=lang)._render_template(
                agreement.special_terms, "agreement", [agreement.id]
            )[agreement.id]
            agreement.dynamic_special_terms = special_terms
