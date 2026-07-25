# Vehicle Booking MVP Technical Design

## 1. Technical Overview

### Module Purpose

`aos_vehicle_booking` provides the first customer-demo business application for AOS Platform. It maintains a small vehicle register and supports an internal user request through submission, approval or rejection, and cancellation.

### Classification

- **Classification:** Business
- **Target:** Odoo 18 Community
- **Location:** `D:\Odoo\AOS\addons\aos_vehicle_booking`

Vehicle-specific models and workflow remain in this business module. No customer-specific behavior belongs in the module.

### Dependencies

Required dependencies:

- `base`
- `aos_base`

`aos_base` is an approved AOS core dependency. No mail, fleet, calendar, approval, DMS, Helpdesk, or external Python dependency is required for the MVP.

### Implementation Boundaries

The module includes only:

- Vehicle master records
- Vehicle booking requests
- Five workflow states
- Manager approval and rejection
- Cancellation rules
- Approved-booking conflict prevention
- Minimum menus, actions, views, security, sequence, and tests

The module does not modify Odoo source code. Multi-company behavior, customer-specific policies, notifications, reporting, attachments, drivers, fleet operations, and external integrations are outside the implementation boundary.

### Deferred Reusable Engines

`aos_booking` is deferred because only one booking use case has been approved. Extracting a reusable booking engine before a second confirmed use case would be speculative.

`aos_approval` is deferred because the MVP requires one manager decision, not a configurable approval platform. The workflow remains local to `aos_vehicle_booking` until cross-application approval requirements are reviewed.

## 2. Module Structure

The intended minimum structure is:

```text
D:\Odoo\AOS\addons\aos_vehicle_booking
├── __init__.py
├── __manifest__.py
├── models
│   ├── __init__.py
│   ├── vehicle.py
│   └── vehicle_booking.py
├── security
│   ├── vehicle_booking_security.xml
│   └── ir.model.access.csv
├── data
│   └── vehicle_booking_sequence.xml
└── views
    ├── vehicle_views.xml
    ├── vehicle_booking_views.xml
    └── vehicle_booking_menus.xml
```

Purpose:

| Path | Purpose |
| --- | --- |
| `__init__.py` | Loads the `models` package |
| `__manifest__.py` | Declares Odoo 18 module metadata and ordered data files |
| `models/__init__.py` | Loads both model files |
| `models/vehicle.py` | Defines `aos.vehicle` |
| `models/vehicle_booking.py` | Defines `aos.vehicle.booking`, workflow, and booking validation |
| `security/vehicle_booking_security.xml` | Defines groups and record rules |
| `security/ir.model.access.csv` | Defines model-level permissions |
| `data/vehicle_booking_sequence.xml` | Defines booking reference generation |
| `views/vehicle_views.xml` | Defines vehicle list, form, and search views plus action |
| `views/vehicle_booking_views.xml` | Defines booking list, form, and search views plus actions |
| `views/vehicle_booking_menus.xml` | Defines the menu hierarchy after actions exist |

No `controllers`, `wizard`, `report`, `demo`, or `static/description` directory is required. Odoo's default module icon is sufficient for the first demo.

The initial module skeleton does not include a `tests` directory. Add it during the automated-test implementation step, when it has immediate content:

```text
tests
├── __init__.py
├── test_vehicle_booking.py
└── test_vehicle_booking_security.py
```

| Planned Test Path | Purpose |
| --- | --- |
| `tests/__init__.py` | Loads the module's test cases |
| `tests/test_vehicle_booking.py` | Covers models, sequence, workflow, validation, normalization, and overlap behavior |
| `tests/test_vehicle_booking_security.py` | Covers internal-user ownership boundaries and manager privileges |

## 3. Manifest Design

| Property | Design |
| --- | --- |
| Name | `AOS Vehicle Booking` |
| Summary | `Manage internal vehicle booking requests` |
| Version | `18.0.1.0.0` |
| Category | `Operations` |
| License | `LGPL-3` |
| Dependencies | `base`, `aos_base` |
| Installable | `True` |
| Application | `True` |

Data files must load in this order:

1. `security/vehicle_booking_security.xml`
2. `security/ir.model.access.csv`
3. `data/vehicle_booking_sequence.xml`
4. `views/vehicle_views.xml`
5. `views/vehicle_booking_views.xml`
6. `views/vehicle_booking_menus.xml`

Groups must exist before access rights and record rules are evaluated. The sequence must exist before users create bookings. Actions must exist before menus reference them.

No demo file is loaded automatically in the MVP.

## 4. Data Models

### A. `aos.vehicle`

#### Model Definition

| Property | Design |
| --- | --- |
| Technical name | `aos.vehicle` |
| Description | `AOS Vehicle` |
| Display name | Standard `name` field through `_rec_name` |
| Default ordering | `name, registration_number, id` |
| Archive behavior | Standard `active` field; archive instead of delete after use |
| Chatter | Not included |

#### Fields

| Technical Name | Type | Label | Required | Default | Index | Copy | Tracking | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `name` | `fields.Char` | Vehicle Name | Yes | None | Yes | Yes | No | Concise human-readable name |
| `registration_number` | `fields.Char` | Registration Number | Yes | None | Yes | No | No | Unique registration or plate |
| `active` | `fields.Boolean` | Active | Yes | `True` | Yes | Yes | No | Controls selection for new requests |
| `image_1920` | `fields.Image` | Vehicle Image | No | None | No | No | No | Standard primary image, limited to 1920 × 1920 |

No capacity, driver, make, model, cost, mileage, or maintenance field is included.

#### SQL Constraints

| Constraint | Rule | Error |
| --- | --- | --- |
| `aos_vehicle_registration_number_uniq` | Unique `registration_number` | `Registration number must be unique.` |

Before saving, `registration_number` is trimmed of leading and trailing whitespace and Latin characters are converted to uppercase. The SQL constraint applies to this normalized stored value. No locale-specific parsing, plate formatting, or transliteration is introduced.

#### Display and Archive Strategy

- `name` is the display value.
- Registration Number is shown beside the name in list and form views.
- Active vehicles are shown by default.
- Archived vehicles remain available on historical booking records.
- Vehicle deletion is permitted only to Booking Managers and should fail naturally when bookings reference the vehicle because `vehicle_id` uses restricted deletion.

### B. `aos.vehicle.booking`

#### Model Definition

| Property | Design |
| --- | --- |
| Technical name | `aos.vehicle.booking` |
| Description | `AOS Vehicle Booking` |
| Display name | Sequence-backed `name` through `_rec_name` |
| Default ordering | `start_datetime desc, id desc` |
| Archive behavior | No `active` field; workflow states preserve history |
| Chatter | Not included |

#### Fields

| Technical Name | Type | Label | Required | Default | Index | Copy | Tracking | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `name` | `fields.Char` | Reference | Yes | `New` until creation | Yes | No | No | Read-only, sequence-backed, unique |
| `requester_id` | `fields.Many2one` to `res.users` | Requester | Yes | Current user | Yes | No | No | Restricted deletion; protected from user reassignment |
| `vehicle_id` | `fields.Many2one` to `aos.vehicle` | Vehicle | No at database level | None | Yes | Yes | No | Required before submit; restricted deletion |
| `start_datetime` | `fields.Datetime` | Start Date and Time | No at database level | None | Yes | Yes | No | Required before submit |
| `end_datetime` | `fields.Datetime` | End Date and Time | No at database level | None | Yes | Yes | No | Required before submit |
| `destination` | `fields.Char` | Destination | No at database level | None | No | Yes | No | Free text; required before submit |
| `purpose` | `fields.Text` | Purpose | No at database level | None | No | Yes | No | Required before submit |
| `state` | `fields.Selection` | Status | Yes | `draft` | Yes | No | No | Read-only outside workflow methods |
| `decision_note` | `fields.Text` | Decision Note | No | None | No | No | No | Required for rejection and visible to requester |

Selection values for `state`:

| Value | Label |
| --- | --- |
| `draft` | Draft |
| `submitted` | Submitted |
| `approved` | Approved |
| `rejected` | Rejected |
| `cancelled` | Cancelled |

There is no `completed` state.

#### Relation and Audit Behavior

- `requester_id` and `vehicle_id` use `ondelete="restrict"` to preserve history.
- Standard Odoo audit fields (`create_uid`, `create_date`, `write_uid`, `write_date`) are used.
- No duplicate creator, approver, approval-date, or cancellation audit fields are added to the MVP.
- No chatter or approval-history model is added.
- `write_uid` and `write_date` show only the most recent write; they do not provide a complete workflow or approval history.
- Full approval/action history is a known auditability requirement that must be reviewed before production V1. It is not a blocker for the first demo.
- Copying a booking must produce a Draft with a new reference and no decision note. Workflow state and reference are never copied.

#### SQL Constraints

| Constraint | Rule | Error |
| --- | --- | --- |
| `aos_vehicle_booking_name_uniq` | Unique `name` | `Booking reference must be unique.` |

Date ordering and overlap rules require Python-level validation because SQL check constraints cannot express the full approved-booking rule safely across records.

## 5. Workflow Methods

Workflow state may change only through the four approved action methods. Direct state changes through ordinary `create` or `write` calls must be rejected.

The action methods may call a private internal state-transition helper or use a narrowly scoped controlled context flag when performing their own state update. That internal mechanism must be inaccessible as a public bypass, must validate the requested transition before use, and must not disable unrelated write protections. This allows approved actions to update `state` without allowing external callers to bypass the workflow.

### `action_submit`

| Aspect | Design |
| --- | --- |
| Allowed state | `draft` |
| Allowed role | Request owner or Booking Manager |
| Validations | Ownership or manager role; vehicle, requester, start, end, destination, and purpose present; start before end; vehicle active |
| Result | `submitted` |
| User-facing errors | Not Draft; not owner; missing required information; invalid period; inactive vehicle |

Conflict checking does not occur at submission. Multiple requests may compete for the same period until a manager decides which one to approve.

### `action_approve`

| Aspect | Design |
| --- | --- |
| Allowed state | `submitted` |
| Allowed role | Booking Manager |
| Validations | Manager role; all required information; start before end; active vehicle; no conflicting Approved booking |
| Result | `approved` |
| User-facing errors | Not Submitted; insufficient role; invalid or incomplete booking; inactive vehicle; conflicting approved reference and period |

The method performs the overlap search immediately before changing state.

### `action_reject`

| Aspect | Design |
| --- | --- |
| Allowed state | `submitted` |
| Allowed role | Booking Manager |
| Validations | Manager role; non-empty `decision_note` |
| Result | `rejected` |
| User-facing errors | Not Submitted; insufficient role; missing rejection reason |

The decision note remains visible to the requester after rejection.

### `action_cancel`

| Current State | Allowed Role | Result |
| --- | --- | --- |
| `draft` | Request owner or Booking Manager | `cancelled` |
| `submitted` | Request owner or Booking Manager | `cancelled` |
| `approved` | Booking Manager only | `cancelled` |

Rejected and Cancelled records cannot be cancelled again. Normal internal users cannot cancel Approved records.

### Edit and Delete Matrix

| State | Normal Internal User | Booking Manager |
| --- | --- | --- |
| `draft` | Owner may edit booking content and delete | May edit or delete |
| `submitted` | Owner may read or cancel; content is read-only | May edit `decision_note`; booking content is read-only |
| `approved` | Owner may read only | Read or cancel; content is read-only |
| `rejected` | Owner may read decision; no edit/delete | Read only; no edit/delete |
| `cancelled` | Owner may read; no edit/delete | Read only; no edit/delete |

Server-side `write` and `unlink` protections must enforce this matrix. View readonly expressions are usability controls, not security controls.

## 6. Booking Conflict Logic

Only Approved bookings block another approval.

A conflict exists when all conditions are true:

- The existing record is not the current record.
- The existing record has the same `vehicle_id`.
- The existing record has `state = approved`.
- The periods overlap:

```text
existing.start_datetime < new.end_datetime
AND
existing.end_datetime > new.start_datetime
```

This rule allows adjacent bookings:

```text
existing.end_datetime == new.start_datetime
```

or:

```text
existing.start_datetime == new.end_datetime
```

### Check Timing

- **Submit:** Do not check conflicts. Submitted requests do not reserve a vehicle.
- **Approve:** Check immediately before setting `state` to `approved`.
- **Direct changes:** Approved booking content is immutable, so changing an approved period or vehicle cannot bypass the check.

Approval-time validation reflects the actual business commitment and permits managers to choose between competing requests.

The MVP accepts the normal search-then-approve race risk for a controlled demo. It does not add explicit locking or transaction serialization. Transaction-safe conflict prevention is a production-readiness blocker and is addressed under Risks.

## 7. Security Design

### Security Groups

| XML ID | Name | Design |
| --- | --- | --- |
| `base.group_user` | Internal User | Standard Odoo group used for normal Vehicle Booking access |
| `aos_vehicle_booking.group_vehicle_booking_manager` | Booking Manager | The only custom security group; implies `base.group_user` |

Do not create a custom Booking User group and do not modify `base.group_user` to imply any custom group. Every authenticated internal user receives normal Vehicle Booking access through the existing `base.group_user`. Portal and public users receive no Vehicle Booking access.

### Model Access Rights

| Model | Group | Read | Create | Write | Delete |
| --- | --- | --- | --- | --- | --- |
| `aos.vehicle` | `base.group_user` | Yes | No | No | No |
| `aos.vehicle` | Booking Manager | Yes | Yes | Yes | Yes |
| `aos.vehicle.booking` | `base.group_user` | Yes | Yes | Yes | Yes |
| `aos.vehicle.booking` | Booking Manager | Yes | Yes | Yes | Yes |

Internal-user write and delete permissions are narrowed by record rules and server-side state/ownership checks.

### Record Rules

| XML ID | Applies To | Domain | Permissions |
| --- | --- | --- | --- |
| `aos_vehicle_booking.rule_vehicle_user_active` | `base.group_user` | Active vehicles only | Read |
| `aos_vehicle_booking.rule_vehicle_manager_all` | Booking Manager | All vehicles | Full |
| `aos_vehicle_booking.rule_booking_user_own` | `base.group_user` | `requester_id` equals current user | Read, create, write, delete |
| `aos_vehicle_booking.rule_booking_manager_all` | Booking Manager | All bookings | Full |

Booking Managers imply `base.group_user`, so the manager's all-record group rule must combine correctly with the internal user's own-record rule to provide full access.

### Button and Method Restrictions

- Submit and user cancellation buttons are visible only when the current user owns the booking or is a manager.
- Approve and Reject buttons are restricted to Booking Manager.
- Approved cancellation is restricted to Booking Manager.
- Every method repeats role, ownership, and state checks server-side.
- The `state`, `name`, and `requester_id` fields cannot be manipulated to bypass workflow or ownership.
- Normal internal users are recognized through `base.group_user`; manager-only methods check `aos_vehicle_booking.group_vehicle_booking_manager`.

### Deletion Restrictions

- Normal internal user: own Draft bookings only.
- Booking Manager: Draft bookings only.
- Submitted, Approved, Rejected, and Cancelled bookings cannot be deleted.
- Vehicles referenced by a booking cannot be deleted; managers archive them instead.

## 8. Sequence Design

| Property | Design |
| --- | --- |
| XML ID | `aos_vehicle_booking.seq_vehicle_booking` |
| Technical code | `aos.vehicle.booking` |
| Name | `Vehicle Booking` |
| Prefix | `VB/%(year)s/` |
| Padding | `5` |
| Company scope | Global for the MVP |
| Assignment | During record creation, before the transaction completes |

Example:

```text
VB/2026/00001
```

The temporary value `New` is never stored as a completed reference. If the sequence is missing or returns no value, creation must stop with a clear user-facing configuration error. Silent fallback to `/`, `New`, or a random value is not allowed because references must remain unique and meaningful.

## 9. Views

Odoo 18 list views use the `list` view type. No calendar view is included; it is not required to demonstrate the approved workflow and would expand the first demo.

### Vehicle Views

#### List

Key fields:

- Vehicle Image thumbnail
- Vehicle Name
- Registration Number
- Active

Behavior:

- Default action shows active vehicles.
- Archived records are available through the standard Archived filter.
- Create, edit, archive, and delete are available only to Booking Managers.

#### Form

Key fields:

- Vehicle Image
- Vehicle Name
- Registration Number
- Active

The form contains no notebook or unrelated fleet fields.

#### Search

A small search view is justified for manager maintenance:

- Search Vehicle Name
- Search Registration Number
- Filters: Active, Archived

### Vehicle Booking Views

#### My Bookings List

Action domain:

```text
requester_id = current user
```

Key fields:

- Reference
- Vehicle
- Start Date and Time
- End Date and Time
- Destination
- Status

Default ordering follows the model. Users can open their own records only.

#### All Bookings List

Visible to Booking Managers only. It uses the same list view and has no ownership domain.

Additional manager field:

- Requester

#### Form

Header:

- Status bar: Draft, Submitted, Approved, Rejected, Cancelled
- Submit button in Draft
- Approve and Reject buttons in Submitted for Booking Managers
- Cancel button in Draft and Submitted for the owner or manager
- Cancel button in Approved for Booking Managers only

Body:

- Reference
- Requester
- Vehicle
- Start Date and Time
- End Date and Time
- Destination
- Purpose
- Decision Note

Readonly behavior:

- Booking content is editable only in Draft.
- `name`, `state`, and `requester_id` are protected.
- Decision Note is editable by Booking Managers in Submitted.
- Rejection reason remains visible to the requester.
- Terminal records are fully read-only.

#### Search

Search fields:

- Reference
- Requester
- Vehicle
- Destination

Filters:

- My Bookings
- Draft
- Submitted
- Approved
- Rejected
- Cancelled

Group-by options:

- Status
- Vehicle
- Requester

No default group-by is required.

### Status Decorations

Colors use view decorations only; there is no database color field.

| State | Decoration |
| --- | --- |
| Draft | `decoration-muted` |
| Submitted | `decoration-warning` |
| Approved | `decoration-success` |
| Rejected | `decoration-danger` |
| Cancelled | `decoration-muted` |

## 10. Menus and Actions

### Menu Hierarchy and Sequence

| Sequence | Menu | XML ID | Visibility |
| --- | --- | --- | --- |
| 10 | Vehicle Booking | `aos_vehicle_booking.menu_vehicle_booking_root` | `base.group_user` |
| 10 | My Bookings | `aos_vehicle_booking.menu_vehicle_booking_my` | `base.group_user` |
| 20 | All Bookings | `aos_vehicle_booking.menu_vehicle_booking_all` | Booking Manager |
| 90 | Configuration | `aos_vehicle_booking.menu_vehicle_booking_configuration` | Booking Manager |
| 10 | Vehicles | `aos_vehicle_booking.menu_vehicle_booking_vehicles` | Booking Manager |

The Configuration label is retained because it follows the approved specification and clearly separates manager-maintained master data.

### Actions

| Action | XML ID | Domain | Context |
| --- | --- | --- | --- |
| My Bookings | `aos_vehicle_booking.action_vehicle_booking_my` | Current user's bookings | Default requester to current user; default state Draft |
| All Bookings | `aos_vehicle_booking.action_vehicle_booking_all` | No additional domain | No forced requester |
| Vehicles | `aos_vehicle_booking.action_vehicle` | Active by default through standard active behavior | No special defaults |

Both booking actions use the same booking list, form, and search views. Role visibility is enforced on menus and reinforced by access rights and record rules.

## 11. Validation and Constraints

### SQL Constraints

- `aos.vehicle.registration_number` is unique.
- `aos.vehicle.booking.name` is unique.

SQL constraints handle stable, single-table uniqueness only.

### Python Constraints

- When both dates are present, `start_datetime` must be earlier than `end_datetime`.
- Vehicle registration numbers are trimmed and Latin characters are converted to uppercase before the normalized value is saved.

The date-order constraint applies as soon as both values exist, including Draft edits. Past and same-day start times are allowed for the demo. No comparison with the current time is implemented.

### Action-Method Validations

- Submit requires requester, active vehicle, dates, destination, and purpose.
- Approve repeats completeness, date-order, and active-vehicle checks.
- Approve prevents overlap with an existing Approved booking.
- Reject requires Decision Note.
- Each action validates its allowed current state and role.
- Cancel validates ownership and applies the Approved-manager rule.

### Write and Delete Enforcement

- Workflow state changes are accepted only through approved action methods.
- Approved action methods use a private helper or narrowly controlled context to perform validated state transitions.
- Ordinary create/write calls and external callers cannot use that internal mechanism to set arbitrary states.
- Normal internal users cannot change `requester_id`.
- Booking content is immutable after submission.
- Only Booking Managers can edit Decision Note while Submitted.
- Delete is limited to Draft according to the role matrix.
- Archived vehicles cannot be selected for submission or approval.

### Security-Rule Enforcement

- Normal internal users (`base.group_user`) see and operate only on their own bookings.
- Booking Managers see all bookings.
- Normal internal users read active vehicles only.
- Booking Managers maintain all vehicles, including archived records.
- Portal and public users have no access.

View expressions must mirror these rules but never replace server-side enforcement.

## 12. Demo Data

### Minimum Dataset

Vehicles:

1. Three active vehicles with distinct names, registration numbers, and images.

Users:

1. Two normal internal users.
2. One internal user assigned Booking Manager.

Bookings:

1. One Draft request.
2. One Submitted request.
3. One Approved request.
4. One Rejected request with a visible Decision Note.
5. One Submitted request that overlaps the Approved request for the same vehicle, used to demonstrate approval conflict.

The conflict scenario must not contain two Approved overlapping records because that would violate the design.

### Loading Decision

Prepare the dataset manually for the first demo. Do not load it automatically from the module.

Reasons:

- The existing `aos` database and real internal users are environment-specific.
- Automatic user creation introduces login, password, and role-management concerns.
- Odoo demo data loads only under specific database installation conditions.
- Manual setup keeps the module smaller and avoids shipping presentation data as product data.

Trade-off: manual preparation is less repeatable. Record the final demo setup as a checklist before the customer session. If repeatable automated demos become necessary, a separate reviewed demo-data file may be added later.

## 13. Acceptance Criteria

- [ ] `aos_vehicle_booking` installs on Odoo 18 Community without errors.
- [ ] The module depends only on `base` and `aos_base`.
- [ ] Vehicle Booking appears for every authenticated internal user.
- [ ] Portal and public users cannot access Vehicle Booking.
- [ ] No custom Booking User group exists and `base.group_user` is not modified to imply a custom group.
- [ ] `aos_vehicle_booking.group_vehicle_booking_manager` is the only custom group and implies `base.group_user`.
- [ ] Booking Managers can create, edit, archive, and view vehicles.
- [ ] Normal internal users can read active vehicles but cannot maintain them.
- [ ] A normal internal user can create a Draft booking for themselves.
- [ ] A normal internal user can submit a complete Draft booking.
- [ ] Submission fails clearly when required information is missing, dates are invalid, or the vehicle is inactive.
- [ ] Past and same-day start times are accepted; no current-time validation is applied.
- [ ] Registration numbers are trimmed and Latin characters are uppercased before uniqueness is checked.
- [ ] Only a Booking Manager can approve a Submitted booking.
- [ ] Only a Booking Manager can reject a Submitted booking.
- [ ] Rejection fails without a Decision Note.
- [ ] A rejected request displays its Decision Note to the requester.
- [ ] A normal internal user can cancel their own Draft or Submitted request.
- [ ] A normal internal user cannot cancel an Approved request.
- [ ] A Booking Manager can cancel an Approved request.
- [ ] Normal internal users cannot view or modify another user's requests.
- [ ] Booking Managers can view all requests.
- [ ] Approval fails when an Approved booking overlaps for the same vehicle.
- [ ] Submitted, Draft, Rejected, and Cancelled bookings do not block approval.
- [ ] Bookings for different vehicles do not conflict.
- [ ] Adjacent bookings can both be approved.
- [ ] An archived vehicle cannot be used for submission or approval.
- [ ] Approved, Rejected, Cancelled, and Submitted bookings cannot be deleted.
- [ ] Status colors come from view decorations, not a stored color field.
- [ ] Ordinary create/write calls cannot bypass workflow transitions, while approved action methods can perform their validated state updates.
- [ ] The MVP uses only standard audit fields and does not add chatter, custom audit fields, or an approval-history model.
- [ ] The automated-test step adds the planned three-file `tests` structure.
- [ ] Odoo restarts successfully with the module installed.
- [ ] A module upgrade completes without errors.
- [ ] No file under `D:\Odoo\odoo` is modified.

### Definition of Done

The MVP is done when:

- Every acceptance criterion above passes.
- The two approved models and five approved states are unchanged.
- The automated tests in `tests/test_vehicle_booking.py` and `tests/test_vehicle_booking_security.py` pass.
- Manual security, workflow, overlap, inactive-vehicle, and adjacent-period checks pass.
- Installation, restart, and module upgrade complete without relevant errors.
- The demo dataset and customer-demo checklist are prepared.
- Documentation and project status are updated.
- No deferred feature or Odoo source modification is included.

Transaction-safe concurrent approval prevention and full workflow audit history are not part of demo Definition of Done; they are mandatory production-readiness items.

## 14. Test Plan

### Manual Positive Tests

1. Install the module and verify role-based menus.
2. Create three vehicles and attach images.
3. Create and submit a complete booking as User A.
4. Approve it as the manager.
5. Submit another request as User B and reject it with a reason.
6. Verify User B can read the reason.
7. Cancel a Draft and a Submitted request as their owner.
8. Cancel an Approved request as the manager.
9. Archive a vehicle and confirm it disappears from normal user selection.

### Manual Validation Failures

- Submit with each required-before-submit field missing.
- Save a booking where start equals end.
- Save a booking where start is after end.
- Submit or approve with an archived vehicle.
- Reject without Decision Note.
- Call each workflow action from an invalid state.
- Attempt to cancel Approved as a normal user.
- Attempt to delete every non-Draft state.

### Manual Security Tests

- User A cannot list, open, edit, cancel, or delete User B's booking.
- A normal user cannot open All Bookings or Vehicles configuration.
- A normal user cannot create, edit, archive, or delete vehicles.
- A normal user cannot approve or reject through the UI or direct RPC.
- Portal and public users cannot access either model.
- A manager can see all bookings and archived vehicles.

### Manual Overlap Edge Cases

Given an Approved booking from 10:00 to 11:00:

- 09:00–10:00: approval succeeds.
- 11:00–12:00: approval succeeds.
- 09:30–10:30: approval fails.
- 10:30–11:30: approval fails.
- 10:00–11:00: approval fails.
- 09:00–12:00: approval fails.
- 10:15–10:45: approval fails.
- The same periods on another vehicle: approval succeeds.
- An overlapping Submitted booking: approval of another Submitted request succeeds if no Approved record conflicts.

### Minimal Automated Tests

Add this structure during the automated-test implementation step:

```text
tests
├── __init__.py
├── test_vehicle_booking.py
└── test_vehicle_booking_security.py
```

Automated tests should cover:

- Module model creation and sequence assignment
- Registration trimming, Latin uppercase normalization, and normalized uniqueness
- Start-before-end constraint
- Acceptance of past and same-day start times
- Successful and invalid state transitions
- Protection against direct state changes without blocking approved action methods
- Required-before-submit checks
- Rejection-note requirement
- Owner cancellation and Approved-manager cancellation
- Normal internal-user record isolation through `base.group_user`
- Manager all-record access
- Approved overlap combinations and adjacent-period boundaries
- Inactive vehicle submit and approve failures
- Deletion restrictions

Use Odoo transaction-based tests. Add browser or tour tests only if the first demo exposes a UI behavior that cannot be validated adequately at the model and security layers.

## 15. Open Technical Decisions

No blocking technical decision remains for creation of the module skeleton.

The demo decisions are resolved:

1. Past and same-day start times are allowed; no current-time validation is implemented.
2. Registration numbers are trimmed and Latin characters are converted to uppercase before normalized uniqueness is applied.
3. The controlled demo accepts the normal search-then-approve race risk; the MVP does not implement explicit locking.

Production-readiness items:

- Transaction-safe concurrent approval serialization is required before production use.
- Full workflow approval/action history must be reviewed before production V1.

These are not blockers for the first demo.

## 16. Implementation Order

1. Create the module skeleton and manifest.
2. Implement both models and the booking sequence.
3. Add the single Booking Manager group, `base.group_user` access, record rules, and server-side ownership protection.
4. Add list, form, search views, actions, and menus.
5. Implement workflow methods, edit/delete enforcement, and validation.
6. Prepare the manual demo dataset and demo checklist.
7. Add the `tests` directory and its three planned files, implement focused automated tests, and execute the manual test plan.
8. Update `README.md`, `CHANGELOG.md`, `AI_CONTEXT.md`, and `docs\PROJECT_STATUS.md`.
9. Validate installation, restart, module upgrade, and logs.
10. Review the complete diff and create a focused Git commit.

Each step should be independently reviewable. No blocking decision remains for module-skeleton creation, but implementation still requires explicit authorization.

## 17. Risks and Deferred Items

### MVP Risks

- A manually prepared demo dataset may be inconsistent unless checked before the session.
- Minimal vehicle fields may require migration when validated customer requirements expand.
- The demo uses only standard audit fields. `write_uid` and `write_date` do not provide full workflow history.
- Users may expect calendar availability even though it is intentionally excluded.

### Security Risks

- ACLs alone are insufficient because normal internal users require write access for their Drafts; record rules and server-side state checks must both be correct.
- UI button visibility does not prevent direct RPC calls; every workflow method must validate roles and ownership.
- Direct writes to protected fields could bypass the workflow unless explicitly blocked.
- The private workflow-transition mechanism must allow validated actions without becoming an external bypass.
- The manager-all record rule must be tested alongside the inherited `base.group_user` own-record rule.

### Timezone and Date-Time Considerations

- Store datetimes using Odoo's standard UTC database behavior.
- Display datetimes in the current user's timezone.
- Compare stored datetimes consistently and avoid converting them to local naive values.
- Test overlap boundaries with users in the intended demo timezone.
- Daylight-saving transitions are not a Thailand demo concern but remain relevant to future deployments.

### Concurrent Approval Risk

Two manager transactions could both find no Approved conflict before either commits, resulting in overlapping approvals. The MVP explicitly accepts this risk for the controlled demo and does not implement locking.

Transaction-safe conflict prevention is a production-readiness blocker. Before production, select a reviewed serialization strategy and add a concurrent test appropriate to that implementation.

### Workflow Audit Risk

Standard Odoo audit fields identify the most recent create/write activity but do not record a complete series of submissions, approvals, rejections, or cancellations. No chatter, approval-history model, or custom audit fields are added to the MVP.

Full approval/action history must be reviewed and designed before production V1 because auditability is a known requirement. It is not a blocker for the first demo.

### Future Refactoring Triggers

Consider extracting reusable capabilities only when:

- A second approved business application needs the same booking semantics.
- Multiple modules need configurable approval behavior.
- Vehicle fields expand into genuine fleet-management requirements.
- Customer-specific behavior cannot be represented through supported configuration.

### Deferred and Not Approved for Implementation

- `aos_booking`
- `aos_approval`
- Multi-level approval, delegation, escalation, and reminders
- Calendar view and availability planner
- Notifications and messaging
- Driver, passenger, fleet, maintenance, fuel, mileage, and cost management
- DMS and attachments
- Multi-company policies
- Reports, dashboards, portal, mobile, maps, GPS, and external integrations
- Customer-specific modules or rules

These items are future options only. They must not be implemented without separate requirements and architecture review.
