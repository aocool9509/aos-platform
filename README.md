# AOS Platform

## Project Overview

AOS Platform is a modular and reusable business application platform built on Odoo 18 Community. It provides a clean foundation for developing shared platform capabilities and focused business applications without modifying the Odoo source code.

The first business application planned for the platform is Vehicle Booking.

## Project Goals

- Build reusable business capabilities on a stable Odoo Community foundation.
- Keep platform, business, and customer-specific concerns clearly separated.
- Deliver maintainable modules that can evolve independently.
- Prefer configuration and extension over hard-coded customization.

## Technology Stack

- Odoo 18 Community
- Python 3.12
- PostgreSQL
- XML, JavaScript, and SCSS for Odoo user interfaces
- Visual Studio Code
- Codex

## Project Structure

```text
D:\Odoo
├── odoo                  # Original Odoo Community source code
├── venv                  # Python virtual environment
├── .vscode               # Shared development and debugging settings
└── AOS
    ├── addons            # All AOS custom modules
    ├── backups           # Local database backups
    ├── config            # Odoo runtime configuration
    ├── docs              # Architecture and project documentation
    ├── logs              # Runtime logs
    ├── scripts           # Development and maintenance scripts
    └── tests             # Project-level tests
```

The Odoo source code under `D:\Odoo\odoo` is never modified. All custom modules are developed under `D:\Odoo\AOS\addons`.

## Development Environment

The local environment uses the Python virtual environment at `D:\Odoo\venv` and the Odoo configuration at `D:\Odoo\AOS\config\odoo.conf`. Visual Studio Code settings and the debugger launch profile are stored in `D:\Odoo\.vscode`.

Before starting Odoo, ensure PostgreSQL is running and the database credentials in the local Odoo configuration are valid.

## How to Run the Project

From PowerShell:

```powershell
cd D:\Odoo
.\venv\Scripts\python.exe .\odoo\odoo-bin -c .\AOS\config\odoo.conf
```

Open `http://localhost:8069` in a browser after the server starts.

## Current Project Status

The Odoo 18 Community development environment is operational, PostgreSQL connectivity is working, and the `aos` database exists. The minimal `aos_base` technical module has been installed successfully and provides the initial foundation for future shared platform capabilities.

Vehicle Booking business logic has not been implemented. Requirements and domain models must be reviewed before the next module is created.

## Architecture Principles

- Target Odoo 18 Community and Python 3.12.
- Never modify the original Odoo source code.
- Keep all custom modules in `AOS/addons`.
- Follow Odoo coding conventions and PEP 8.
- Keep changes small, focused, and reviewable.
- Avoid unnecessary module dependencies and external packages.
- Separate core, business, customer-specific, add-on, and configuration concerns.
- Prefer reusable configuration over customer-specific hard-coded behavior.
- Use English for source code, technical names, comments, and commits.

## Documentation

- [AI operating context](AI_CONTEXT.md)
- [Architecture](docs/AOS_ARCHITECTURE.md)
- [Development setup](docs/DEVELOPMENT_SETUP.md)
- [Project structure](docs/PROJECT_STRUCTURE.md)
- [Project status](docs/PROJECT_STATUS.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

AOS Platform modules are licensed under the GNU Lesser General Public License v3.0 (LGPL-3).
