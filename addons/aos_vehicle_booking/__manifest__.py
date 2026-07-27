{
    "name": "AOS Vehicle Booking",
    "summary": "Manage internal vehicle booking requests",
    "version": "18.0.1.0.0",
    "category": "Operations",
    "license": "LGPL-3",
    "depends": ["base", "aos_base"],
    "data": [
        "security/ir.model.access.csv",
        "data/vehicle_booking_sequence.xml",
        "views/vehicle_views.xml",
        "views/vehicle_booking_views.xml",
        "views/vehicle_booking_menus.xml",
    ],
    "installable": True,
    "application": True,
}
