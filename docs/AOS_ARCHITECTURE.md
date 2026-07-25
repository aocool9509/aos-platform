# AOS Platform Architecture

## 1. Architecture Overview

AOS is a modular, reusable business platform built on Odoo 18 Community. It extends Odoo exclusively through custom addons and configuration; the original Odoo source code is never modified.

The platform separates reusable capabilities from business applications and customer-specific extensions. All AOS modules are maintained under `AOS/addons`, allowing the platform to evolve independently from the Odoo distribution.

## 2. Design Principles

- **Modularity:** Each module has a clear, focused responsibility.
- **Reusability:** Shared capabilities are designed for use by multiple business applications.
- **Separation of concerns:** Platform, business, customer, add-on, and configuration concerns remain distinct.
- **Controlled dependencies:** Modules depend only on capabilities they genuinely require.
- **Configuration over customization:** Variable behavior should be configurable where practical.
- **Odoo compatibility:** Extensions follow supported Odoo 18 Community patterns.
- **Incremental delivery:** Changes remain small, reviewable, tested, and aligned with approved requirements.

## 3. Module Classification

Every AOS feature belongs to one of the following classifications:

| Classification | Purpose |
| --- | --- |
| Core | Reusable platform capabilities shared across business applications |
| Business | Complete business capabilities serving a defined operational domain |
| Customer-specific | Isolated behavior required by a particular customer or deployment |
| Add-on | Optional extensions to an existing core or business capability |
| Configuration | Deployment-level setup that does not require hard-coded behavior |

Classification is determined before implementation to preserve clear ownership and dependency boundaries.

## 4. Core Modules

Core modules provide stable capabilities that may be reused by multiple AOS applications. They must remain business-domain neutral and must not depend on Vehicle Booking or any other individual business module.

`aos_base` is the only implemented AOS core module. It is the installed technical foundation for shared platform concerns.

The planned core-module direction includes:

- `aos_booking`
- `aos_dms`
- `aos_helpdesk`
- `aos_approval`

These names express architectural direction only. They are not implemented, and new core modules will be introduced only when reviewed requirements demonstrate genuine reuse. Advanced approvals, DMS, and Helpdesk are outside the immediate scope.

## 5. Business Modules

Business modules implement cohesive capabilities for a defined business domain. They may use Odoo Community features and approved AOS core modules.

Vehicle Booking is the first planned business application, with `aos_vehicle_booking` as the intended module name. Its requirements and domain model must be reviewed before implementation. Logic specific to Vehicle Booking must remain outside reusable core modules.

## 6. Customer Modules

Customer modules isolate deployment-specific requirements from the reusable platform and standard business modules. They may extend approved AOS capabilities but must not introduce customer behavior into core modules.

Customer-specific modules should remain optional, clearly named, documented, and independently maintainable.

The naming pattern is `aos_customer_xxx`. No customer module is currently implemented.

### Add-on Modules

Add-on modules provide optional extensions to an existing core or business capability. They must depend on the capability they extend and must not become mandatory dependencies of lower architectural layers.

### Configuration

Configuration represents deployment-level behavior expressed through Odoo settings, data, or safe runtime configuration. Configuration is preferred when a requirement varies by deployment and does not justify customer-specific code.

## 7. Dependency Rules

- Odoo Community modules form the external foundation.
- Core modules may depend on Odoo Community modules and other lower-level core modules.
- Business modules may depend on Odoo Community and approved core modules.
- Customer-specific modules may depend on the core and business modules they extend.
- Add-on modules may depend on the capability they enhance.
- Core modules must never depend on business, customer-specific, or optional add-on modules.
- Business modules must not depend on customer-specific modules.
- Circular dependencies are prohibited.
- Dependencies must be explicit, minimal, and justified by current requirements.
- External Python packages require explicit approval.

The intended dependency direction is:

```text
Odoo Community
      ↓
AOS Core
      ↓
AOS Business
      ↓
Customer-specific Extensions
```

Optional add-ons extend an approved layer without reversing this dependency direction.

Configuration may influence an approved layer but must not conceal unsupported cross-layer dependencies.

## 8. Project Directory Structure

```text
D:\Odoo
├── odoo                  # Unmodified Odoo Community source
├── venv                  # Python 3.12 virtual environment
├── .vscode               # Development and debugging configuration
└── AOS
    ├── addons            # All AOS custom modules
    ├── backups           # Local backup storage
    ├── config            # Odoo runtime configuration
    ├── docs              # Architecture and project documentation
    ├── logs              # Runtime logs
    ├── scripts           # Development and maintenance scripts
    └── tests             # Project-level tests
```

Module-specific models, security rules, data, views, and tests belong within their respective addon directories.

## 9. Development Standards

- Target Odoo 18 Community and Python 3.12.
- Never modify files under `D:\Odoo\odoo`.
- Create all custom modules under `D:\Odoo\AOS\addons`.
- Follow Odoo coding conventions and PEP 8.
- Use English for source code, technical names, comments, and commits.
- Define access controls explicitly when introducing models.
- Validate Python and XML syntax for every applicable change.
- Add tests in proportion to behavior and risk.
- Avoid speculative features and unnecessary dependencies.
- Keep changes focused, reviewable, and documented.

## 10. Future Expansion Strategy

AOS will expand through reviewed platform and business requirements rather than speculative abstraction. Reusable capabilities will be promoted into core modules only when multiple applications require them.

Vehicle Booking is intended to validate the initial platform foundation. Later business applications may reuse established core capabilities while remaining independently maintainable. Cross-application needs, such as approvals, may become separate platform capabilities after their scope and reuse have been confirmed.

Customer-specific behavior and optional extensions will remain isolated so the main AOS platform can evolve as a reusable product. Production growth will be supported through documented compatibility, controlled versioning, testing, and migration practices.

Planned module names and roadmap phases do not represent completed functionality. Each new module requires scope, model, dependency, and ownership review before creation.
