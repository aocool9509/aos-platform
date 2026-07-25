# AOS Platform

## Project Overview

AOS Platform is a modular business application platform built on Odoo 18 Community.

The first business module is an internal vehicle booking system.

## Project Structure

- `D:\Odoo\odoo` contains the original Odoo Community source code.
- `D:\Odoo\AOS` contains the AOS project.
- `D:\Odoo\AOS\addons` contains all custom Odoo modules.
- `D:\Odoo\AOS\config` contains runtime configuration.
- `D:\Odoo\AOS\docs` contains architecture and project documentation.
- `D:\Odoo\AOS\tests` contains project-level tests.

## Mandatory Rules

- Never modify files inside `D:\Odoo\odoo`.
- All custom modules must be created inside `D:\Odoo\AOS\addons`.
- Target Odoo 18 Community only.
- Use Python 3.12.
- Follow Odoo coding conventions and PEP 8.
- Use English for source code, technical names, comments, and Git commits.
- Do not add external Python packages unless explicitly approved.
- Do not add unnecessary dependencies between AOS modules.
- Prefer configuration over customer-specific hard-coded logic.
- Do not implement speculative features that are outside the current task.
- Keep changes small, reviewable, and focused.

## Architecture Rules

Classify every feature as one of:

- Core
- Business
- Customer-specific
- Add-on
- Configuration

Reusable platform capabilities must not depend directly on the vehicle booking module.

Customer-specific behavior must not be placed in reusable core modules.

## Development Workflow

Before changing code:

1. Inspect the relevant existing files.
2. Explain the proposed change briefly.
3. List files that will be created or modified.
4. Implement only the requested scope.
5. Validate Python and XML syntax.
6. Summarize the completed changes and remaining risks.

## Current Scope

The immediate goal is to prepare a working Odoo 18 development environment and create a minimal installable module.

Do not implement the complete vehicle booking application until its models and requirements have been reviewed.