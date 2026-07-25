# Contributing to AOS Platform

This guide defines the contribution and coding standards for the AOS Platform on Odoo 18 Community.

## Development Workflow

1. Inspect the relevant existing files and confirmed project context.
2. Explain the proposed change and list affected files.
3. Implement only the reviewed scope.
4. Validate applicable Python, XML, security, and manifest changes.
5. Run relevant tests.
6. Update project documentation when behavior, setup, status, or scope changes.
7. Summarize completed work and remaining risks.

## Branch Strategy

- Keep the default branch stable and releasable.
- Create a short-lived branch for each focused change.
- Use descriptive branch names with one of these prefixes:
  - `feature/` for new capabilities
  - `fix/` for defect corrections
  - `docs/` for documentation
  - `refactor/` for behavior-preserving improvements
  - `chore/` for maintenance
- Rebase or update the branch before review when necessary.
- Do not combine unrelated work in one branch.
- Delete merged branches after confirming the merge.

Examples:

```text
feature/vehicle-booking-foundation
fix/booking-access-rule
docs/development-setup
```

## Commit Messages

Write commit messages in English using a concise, imperative description. Follow this structure:

```text
type(scope): summary
```

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `build`.

Examples:

```text
feat(aos_base): add shared configuration model
fix(vehicle_booking): correct booking access rule
docs: document local development setup
```

- Keep the first line focused on one logical change.
- Explain motivation and relevant consequences in the body when needed.
- Reference related work items where applicable.
- Do not commit generated caches, logs, credentials, or local runtime data.

## Pull Requests

- Open one pull request for one focused outcome.
- Provide a clear title and summary of the change.
- Explain why the change is needed and identify affected modules.
- List created and modified files.
- Describe validation performed and any remaining risks.
- Include screenshots for meaningful user-interface changes.
- Document configuration, migration, security, or compatibility effects.
- Keep the pull request small enough for effective review.
- Resolve review feedback before requesting final approval.

## Coding Style

- Use English for source code, technical names, comments, and documentation.
- Prefer clear, maintainable code over clever abstractions.
- Keep functions, classes, records, and modules focused.
- Avoid duplication without introducing speculative frameworks.
- Add comments only when they explain intent or a non-obvious constraint.
- Keep changes consistent with surrounding project conventions.
- Do not add external dependencies without explicit approval.

## Python Standards

- Target Python 3.12.
- Follow PEP 8 and Odoo Python conventions.
- Use four spaces for indentation.
- Use descriptive `snake_case` names for variables, functions, methods, and modules.
- Use `PascalCase` for Python classes.
- Keep imports grouped and remove unused imports.
- Use the Odoo ORM instead of direct SQL unless direct SQL is justified and reviewed.
- Use recordsets correctly and avoid unnecessary queries inside loops.
- Make overridden methods cooperative by calling `super()` where required.
- Use Odoo logging instead of `print`.
- Validate Python syntax and add tests for meaningful behavior.

## XML Standards

- Use UTF-8 XML with consistent four-space indentation.
- Give records stable, descriptive external identifiers.
- Use lowercase `snake_case` identifiers prefixed by the relevant module or feature context.
- Keep XML files focused by concern, such as views, menus, security, or data.
- Order records so referenced records are loaded first.
- Use explicit `ref` values and avoid fragile database identifiers.
- Add access groups to restricted menus, views, actions, and records as appropriate.
- Keep user-facing strings clear and translatable.
- Validate XML syntax before review.

## Odoo Standards

- Target Odoo 18 Community only.
- Never modify files under `D:\Odoo\odoo`.
- Place every custom module under `D:\Odoo\AOS\addons`.
- Use an `18.0.x.y.z` module version and declare `LGPL-3` unless another approved license applies.
- Declare only necessary module dependencies.
- Keep reusable core modules independent of business and customer-specific modules.
- Isolate customer-specific behavior in dedicated modules.
- Prefer supported inheritance and extension mechanisms over copying Odoo code.
- Define model access rights and record rules explicitly when models are introduced.
- Load security definitions before dependent views or data.
- Avoid hard-coded customer behavior when configuration can express the requirement.
- Include module-level tests in the module and project-level tests under `AOS/tests` when appropriate.

## Review Process

1. The author reviews the complete diff and removes unrelated or generated changes.
2. Python, XML, manifests, security definitions, and applicable tests are validated.
3. A reviewer checks scope, correctness, maintainability, security, and architectural classification.
4. Dependency changes and customer-specific behavior receive explicit scrutiny.
5. The author addresses feedback and records any accepted limitations or risks.
6. The pull request receives approval before merge.
7. The merged result is verified against the intended Odoo 18 Community environment.

Review approval confirms that the change follows current requirements and project standards; it does not authorize speculative expansion beyond the reviewed scope.

## Review Checklist

- [ ] The change is limited to an approved requirement.
- [ ] No file under `D:\Odoo\odoo` was modified.
- [ ] Custom module changes are under `D:\Odoo\AOS\addons`.
- [ ] Dependencies are necessary and respect architecture boundaries.
- [ ] Python, XML, manifests, and security files were validated as applicable.
- [ ] Tests cover meaningful behavior and risk.
- [ ] Credentials, logs, backups, caches, and generated files are excluded.
- [ ] Documentation and status records are current.

## Documentation Updates

- Update `README.md` when entry-point setup or project orientation changes.
- Update `CHANGELOG.md` for user-visible changes.
- Update `docs\PROJECT_STATUS.md` after meaningful completed work.
- Update `AI_CONTEXT.md` when confirmed operating context or scope changes.
- Update architecture, setup, and roadmap documents when their governing facts change.
- Never document planned modules or features as completed.
