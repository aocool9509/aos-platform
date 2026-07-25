from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AosVehicleBooking(models.Model):
    _name = "aos.vehicle.booking"
    _description = "AOS Vehicle Booking"
    _order = "start_datetime desc, id desc"
    _rec_name = "name"

    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False,
        index=True,
    )
    requester_id = fields.Many2one(
        comodel_name="res.users",
        string="Requester",
        required=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
    )
    vehicle_id = fields.Many2one(
        comodel_name="aos.vehicle",
        string="Vehicle",
        ondelete="restrict",
    )
    start_datetime = fields.Datetime(
        string="Start Date and Time",
        index=True,
    )
    end_datetime = fields.Datetime(
        string="End Date and Time",
        index=True,
    )
    destination = fields.Char(string="Destination")
    purpose = fields.Text(string="Purpose")
    decision_note = fields.Text(
        string="Decision Note",
        copy=False,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        readonly=True,
        copy=False,
    )

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "Booking reference must be unique.",
        ),
    ]

    @api.constrains("start_datetime", "end_datetime")
    def _check_datetime_order(self):
        for booking in self:
            if (
                booking.start_datetime
                and booking.end_datetime
                and booking.start_datetime >= booking.end_datetime
            ):
                raise ValidationError(
                    "End date and time must be later than start date and time."
                )
