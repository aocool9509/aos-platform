# AOS AI Context

## Project Overview

AOS Platform is a modular, reusable business platform built on Odoo 18 Community. Vehicle Booking is the first planned business application.

Confirmed project facts must not be replaced by assumptions. Inspect relevant files before changing code or documentation.

## Confirmed Environment

- Windows development workstation
- Odoo 18 Community at `D:\Odoo\odoo`
- Python 3.12 virtual environment at `D:\Odoo\venv`
- PostgreSQL with the `aos` development database
- Visual Studio Code configuration at `D:\Odoo\.vscode`
- AOS project at `D:\Odoo\AOS`
- Custom addons at `D:\Odoo\AOS\addons`

Odoo runs successfully, PostgreSQL connectivity works, and `aos_base` is installed.

## Architecture Rules

- Never modify the Odoo source directory.
- Keep all custom modules under `D:\Odoo\AOS\addons`.
- Classify work as Core, Business, Customer-specific, Add-on, or Configuration.
- Keep reusable platform capabilities independent of Vehicle Booking.
- Keep customer-specific behavior outside reusable core modules.
- Prefer configuration over hard-coded customization.
- Avoid speculative features and unnecessary dependencies.

## Naming Rules

- Use English for code, technical names, comments, documentation, and commits.
- Use the `aos_` prefix for AOS modules.
- Core direction: `aos_base`, `aos_booking`, `aos_dms`, `aos_helpdesk`, `aos_approval`.
- Business direction: `aos_vehicle_booking`.
- Customer modules: `aos_customer_xxx`.
- Planned names do not mean that modules or features are implemented.

## Current Status

- Current phase: Platform Foundation
- Development environment: complete and operational
- `aos_base`: created and installed
- Vehicle Booking business logic: not implemented
- PDF reporting: unavailable because wkhtmltopdf is not installed

## Current Scope

Maintain the platform foundation and define the minimum Vehicle Booking demo only after its models and scope are reviewed.

## Next Tasks

1. Validate repository files.
2. Initialize the AOS Git repository if needed.
3. Commit the platform foundation.
4. Design the minimum Vehicle Booking demo scope.
5. Create the next module only after model and scope review.

## Prohibited Actions

- Do not modify `D:\Odoo\odoo`.
- Do not expose credentials or master passwords.
- Do not add business logic without reviewed requirements.
- Do not create speculative modules or external dependencies.
- Do not place customer-specific logic in reusable modules.

## Update Instructions

- Update `docs\PROJECT_STATUS.md` when meaningful work is completed.
- Update `CHANGELOG.md` for user-visible changes.
- Keep this file concise and update it when confirmed operating context changes.
