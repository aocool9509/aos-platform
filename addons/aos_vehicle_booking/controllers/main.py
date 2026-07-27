from odoo import http
from odoo.http import request


class AosVehicleBookingController(http.Controller):

    @http.route(
        "/aos/vehicle-booking",
        type="http",
        auth="public",
        methods=["GET"],
    )
    def vehicle_booking_landing(self):
        return request.render(
            "aos_vehicle_booking.vehicle_booking_landing_page"
        )

    @http.route(
        "/aos/vehicle-booking/app",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def vehicle_booking_app(self):
        return request.redirect(
            "/odoo/action-aos_vehicle_booking."
            "action_aos_vehicle_booking_welcome",
            code=303,
        )
