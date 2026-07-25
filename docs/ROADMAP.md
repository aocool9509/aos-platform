# AOS Platform Roadmap

This roadmap defines outcome-focused phases for the AOS Platform. Planned work is not considered implemented until it has been reviewed, delivered, and recorded in the project status.

## Phase 0 - Development Environment

**Status:** Completed

### Objective

Establish a working local environment for Odoo 18 Community development.

### Outcomes

- Windows workspace and Python 3.12 virtual environment
- PostgreSQL connectivity and `aos` development database
- Operational Odoo 18 Community server
- Visual Studio Code run and debug configuration
- Initial AOS directory structure

## Phase 1 - Platform Foundation

**Status:** In Progress

### Objective

Establish the reusable AOS project foundation, boundaries, standards, and repository documentation.

### Outcomes

- Installed minimal `aos_base` module
- Architecture and dependency rules
- Safe configuration example
- Contribution, setup, status, and AI-context documentation
- Repository validation and initial foundation commit

## Phase 2 - Booking Foundation

**Status:** Planned

### Objective

Review and define the minimum reusable booking domain before creating additional modules.

### Outcomes

- Reviewed booking scope
- Approved domain model and module boundaries
- Defined relationship between reusable booking capabilities and Vehicle Booking
- Agreed security and validation expectations

## Phase 3 - Vehicle Booking Demo

**Status:** Planned

### Objective

Deliver a minimum demonstrable Vehicle Booking application using the approved booking foundation.

### Outcomes

- Installable `aos_vehicle_booking` module
- Minimum reviewed demo workflow
- Appropriate access controls and user interface
- Focused tests and documentation

## Phase 4 - Requirement Validation and V1

**Status:** Planned

### Objective

Validate the demo against reviewed business requirements and prepare a defined first application version.

### Outcomes

- Validated requirements and acceptance criteria
- Resolved gaps from demo feedback
- Documented upgrade and release considerations
- Tested Vehicle Booking V1 scope

## Phase 5 - Reusable Platform Expansion

**Status:** Future

### Objective

Expand AOS only where confirmed cross-application requirements justify reusable platform or additional business modules.

### Outcomes

- Prioritized and reviewed expansion opportunities
- Independently maintainable core and business modules
- Controlled customer-specific and optional extensions
- Versioned compatibility and evolution guidance

## Immediate Scope Boundary

Advanced approval workflow diagrams, delegation, escalation, DMS, and Helpdesk are outside the immediate scope. Planned names such as `aos_approval`, `aos_dms`, and `aos_helpdesk` describe possible future direction and do not represent implemented modules.
