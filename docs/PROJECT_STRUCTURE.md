# AOS Platform Project Structure

This document describes the directory organization of the AOS Platform development workspace.

## Workspace Overview

```text
D:\Odoo
├── odoo                  # Original Odoo 18 Community source
├── venv                  # Python 3.12 virtual environment
├── .vscode               # Shared editor and debugger configuration
└── AOS                   # AOS Platform project
    ├── addons            # Custom Odoo modules
    ├── backups           # Local database backups
    ├── config            # Odoo runtime configuration
    ├── docs              # Project documentation
    ├── logs              # Odoo runtime logs
    ├── scripts           # Development and maintenance scripts
    └── tests             # Project-level tests
```

## Root Folders

### `D:\Odoo\odoo`

Contains the original Odoo 18 Community source code and standard addons. AOS treats this directory as an external dependency and never modifies it.

### `D:\Odoo\venv`

Contains the Python 3.12 virtual environment used to run and debug Odoo. Installed Python dependencies belong to this environment rather than the system Python installation.

### `D:\Odoo\.vscode`

Contains shared Visual Studio Code settings and debugger configurations for the workspace. Local or user-specific editor state should not be committed.

### `D:\Odoo\AOS`

Contains all source code, configuration, documentation, tests, and supporting resources owned by the AOS Platform.

## `addons`

Path: `D:\Odoo\AOS\addons`

Contains every custom AOS module. Reusable core modules, business modules, optional add-ons, and customer-specific extensions must remain clearly classified and independently maintainable.

A typical module follows this structure:

```text
addons
└── module_name
    ├── __init__.py
    ├── __manifest__.py
    ├── data
    ├── models
    ├── security
    ├── tests
    └── views
```

Only directories required by the module should be added. Generated Python caches must not be committed.

## `config`

Path: `D:\Odoo\AOS\config`

Contains Odoo runtime configuration. Local files may define database connectivity, addon paths, ports, logging, and development options.

Configuration files containing credentials are local and must not be committed. Distributable example configurations should contain safe defaults and no secrets.

## `docs`

Path: `D:\Odoo\AOS\docs`

Contains maintained project documentation, including architecture, development setup, roadmap, project structure, and release guidance. Documentation should describe approved behavior and decisions without duplicating source code.

## `logs`

Path: `D:\Odoo\AOS\logs`

Contains Odoo runtime logs used for local diagnostics and troubleshooting. Log files are generated artifacts and must not be committed.

## `scripts`

Path: `D:\Odoo\AOS\scripts`

Contains repeatable development, testing, maintenance, backup, and operational helper scripts. Scripts should be focused, documented, safe by default, and compatible with the supported Windows development environment.

## `tests`

Path: `D:\Odoo\AOS\tests`

Contains project-level validation and integration tests that span multiple modules or verify the development environment. Tests specific to one Odoo module should normally live inside that module's `tests` directory.

## `backups`

Path: `D:\Odoo\AOS\backups`

Contains local database or development backups. Backups may include sensitive data, are environment-specific, and must not be committed to version control.

## Structure Rules

- Never modify files under `D:\Odoo\odoo`.
- Store all custom modules under `D:\Odoo\AOS\addons`.
- Keep runtime files, logs, backups, caches, and secrets out of version control.
- Place documentation and tests at the narrowest appropriate scope.
- Add new directories only when an approved requirement justifies them.
