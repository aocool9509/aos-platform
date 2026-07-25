import unicodedata

from odoo import api, fields, models


class AosVehicle(models.Model):
    _name = "aos.vehicle"
    _description = "AOS Vehicle"
    _order = "name, registration_number, id"

    name = fields.Char(string="Vehicle Name", required=True, index=True)
    registration_number = fields.Char(
        string="Registration Number",
        required=True,
        index=True,
        copy=False,
    )
    active = fields.Boolean(default=True, index=True)
    image_1920 = fields.Image(
        string="Vehicle Image",
        max_width=1920,
        max_height=1920,
        copy=False,
    )

    _sql_constraints = [
        (
            "registration_number_uniq",
            "unique(registration_number)",
            "Registration number must be unique.",
        ),
    ]

    @staticmethod
    def _normalize_registration_number(registration_number):
        if not isinstance(registration_number, str):
            return registration_number
        return "".join(
            character.upper()
            if "LATIN" in unicodedata.name(character, "")
            else character
            for character in registration_number.strip()
        )

    @api.model_create_multi
    def create(self, vals_list):
        normalized_vals_list = []
        for vals in vals_list:
            normalized_vals = dict(vals)
            if "registration_number" in normalized_vals:
                normalized_vals["registration_number"] = (
                    self._normalize_registration_number(
                        normalized_vals["registration_number"]
                    )
                )
            normalized_vals_list.append(normalized_vals)
        return super().create(normalized_vals_list)

    def write(self, vals):
        normalized_vals = dict(vals)
        if "registration_number" in normalized_vals:
            normalized_vals["registration_number"] = (
                self._normalize_registration_number(
                    normalized_vals["registration_number"]
                )
            )
        return super().write(normalized_vals)
