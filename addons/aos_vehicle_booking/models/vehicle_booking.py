from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


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

    def action_submit(self):
        if any(booking.state != "draft" for booking in self):
            raise UserError("Only draft bookings can be submitted.")
        for booking in self:
            if not booking.vehicle_id:
                raise UserError("Vehicle is required before submission.")
            if not booking.start_datetime:
                raise UserError(
                    "Start date and time is required before submission."
                )
            if not booking.end_datetime:
                raise UserError(
                    "End date and time is required before submission."
                )
            if not booking.destination or not booking.destination.strip():
                raise UserError("Destination is required before submission.")
            if not booking.purpose or not booking.purpose.strip():
                raise UserError("Purpose is required before submission.")
            if not booking.vehicle_id.active:
                raise UserError("The selected vehicle must be active.")
            if booking.start_datetime >= booking.end_datetime:
                raise UserError(
                    "Start date and time must be earlier than "
                    "end date and time."
                )
        self.write({"state": "submitted"})
        return True

    def action_approve(self):
        if any(booking.state != "submitted" for booking in self):
            raise UserError("Only submitted bookings can be approved.")
        self.write({"state": "approved"})
        return True

    def action_reject(self):
        if any(booking.state != "submitted" for booking in self):
            raise UserError("Only submitted bookings can be rejected.")
        if any(
            not booking.decision_note or not booking.decision_note.strip()
            for booking in self
        ):
            raise UserError("Decision note is required before rejection.")
        self.write({"state": "rejected"})
        return True

    def action_cancel(self):
        allowed_states = {"draft", "submitted", "approved"}
        if any(booking.state not in allowed_states for booking in self):
            raise UserError(
                "Only draft, submitted, or approved bookings can be cancelled."
            )
        self.write({"state": "cancelled"})
        return True
