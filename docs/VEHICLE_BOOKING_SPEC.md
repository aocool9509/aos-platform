# Vehicle Booking MVP Specification

## 1. Business Objective

Provide a minimum internal Vehicle Booking application that demonstrates how an employee requests a vehicle for a defined period and how a manager reviews that request.

The proposed module is `aos_vehicle_booking`, classified as a **Business** module. Vehicle-specific behavior remains outside reusable AOS core modules. No generic booking or approval engine is introduced at this stage.

## 2. In Scope

- Maintain a simple list of bookable vehicles.
- Allow an internal user to create and submit a vehicle booking request.
- Allow a booking manager to approve or reject a submitted request.
- Allow permitted users to cancel a request.
- Prevent approval of overlapping bookings for the same vehicle.
- Show users their requests and managers all requests.
- Demonstrate the complete workflow using standard Odoo views.

## 3. Out of Scope

- Driver assignment or driver scheduling
- Vehicle maintenance, fuel, mileage, or fleet operations
- Recurring or multi-vehicle bookings
- Passenger manifests
- Route planning, maps, GPS, or travel-time calculations
- Cost allocation, expenses, invoicing, or accounting
- Email, SMS, or mobile notifications
- Calendar synchronization
- Attachments or document management
- Advanced approval levels, delegation, escalation, or an approval engine
- Customer-specific rules
- Portal or public access
- PDF reports
- Reusable booking framework extraction

## 4. User Roles

### Booking User

An internal user who can:

- View active vehicles needed to prepare a request.
- Create and edit their own draft requests.
- Submit their own requests.
- View their own requests and decisions.
- Cancel their own draft or submitted requests.

### Booking Manager

An internal user who can:

- Perform all Booking User actions.
- View and manage all vehicle booking requests.
- Create and maintain vehicle records.
- Approve or reject submitted requests.
- Cancel requests when operationally necessary.

## 5. User Stories

- As a Booking User, I want to view active vehicles so that I can select one for my request.
- As a Booking User, I want to create a request with a vehicle, period, destination, and purpose.
- As a Booking User, I want to submit my draft request for review.
- As a Booking User, I want to see the current status of my requests.
- As a Booking User, I want to cancel a request that is no longer needed before it is approved.
- As a Booking Manager, I want to review all submitted requests.
- As a Booking Manager, I want to approve an available vehicle for the requested period.
- As a Booking Manager, I want to reject a request and record the reason.
- As a Booking Manager, I want to maintain the list of bookable vehicles.

## 6. Business Workflow

### Request States

1. **Draft** — The requester prepares the booking.
2. **Submitted** — The request is ready for manager review.
3. **Approved** — The manager confirms the vehicle and period.
4. **Rejected** — The manager declines the request and records a reason.
5. **Cancelled** — The requester or manager ends a request that should no longer proceed.

### Allowed Transitions

| From | Action | To | Performed By |
| --- | --- | --- | --- |
| Draft | Submit | Submitted | Request owner or Booking Manager |
| Draft | Cancel | Cancelled | Request owner or Booking Manager |
| Submitted | Approve | Approved | Booking Manager |
| Submitted | Reject | Rejected | Booking Manager |
| Submitted | Cancel | Cancelled | Request owner or Booking Manager |
| Approved | Cancel | Cancelled | Booking Manager |

Rejected and cancelled requests are terminal for the MVP. A new request is created when circumstances change.

## 7. Required Menus

```text
Vehicle Booking
├── My Bookings
├── All Bookings        # Booking Manager only
└── Configuration
    └── Vehicles        # Booking Manager only
```

No dashboard, reporting, or additional configuration menu is required for the MVP.

## 8. Required Data Models

### Vehicle

Represents one vehicle that may be selected for booking.

Suggested technical model: `aos.vehicle`

### Vehicle Booking

Represents one employee request for one vehicle over one continuous time period.

Suggested technical model: `aos.vehicle.booking`

These models belong to the Vehicle Booking business module for the MVP. Reuse must be demonstrated before any capability is moved into a core module.

## 9. Required Fields

### Vehicle Fields

| Field | Purpose | Required | Default |
| --- | --- | --- | --- |
| Name | Human-readable vehicle name | Yes | None |
| Registration Number | Unique vehicle registration or plate | Yes | None |
| Active | Controls whether the vehicle can be selected for new requests | Yes | Enabled |

### Vehicle Booking Fields

| Field | Purpose | Required | Default |
| --- | --- | --- | --- |
| Reference | Unique booking identifier | Yes | Automatically assigned |
| Requester | Internal user requesting the vehicle | Yes | Current user |
| Vehicle | Requested vehicle | Yes before submission | None |
| Start Date and Time | Beginning of the requested period | Yes before submission | None |
| End Date and Time | End of the requested period | Yes before submission | None |
| Destination | Concise destination description | Yes before submission | None |
| Purpose | Business reason for the request | Yes before submission | None |
| Status | Current workflow state | Yes | Draft |
| Decision Note | Manager's reason or decision context | Required on rejection | None |

Odoo's standard audit fields provide creation and modification history. Duplicate custom audit fields are not required.

## 10. Validation Rules

- Registration Number must be unique among vehicle records.
- A submitted request must contain a vehicle, requester, start, end, destination, and purpose.
- End Date and Time must be later than Start Date and Time.
- A vehicle must be active when a request is submitted or approved.
- Only a Submitted request can be approved or rejected.
- Decision Note is required when a request is rejected.
- An Approved request must not overlap another Approved request for the same vehicle.
- Two periods overlap when each begins before the other ends. Adjacent periods where one ends exactly when another begins are allowed.
- Only a Booking Manager may approve, reject, or cancel an Approved request.
- Terminal requests cannot return to Draft in the MVP.

Whether past start times are prohibited is an open business decision and is not assumed.

## 11. Access Rights

| Resource | Booking User | Booking Manager |
| --- | --- | --- |
| Active Vehicles | Read | Create, read, update, and archive |
| Own Draft Bookings | Create, read, update, delete, submit, or cancel | Full access |
| Own Submitted Bookings | Read or cancel | Full access |
| Own Approved, Rejected, or Cancelled Bookings | Read | Full access |
| Other Users' Bookings | No access | Full access |
| Approval and Rejection Actions | No access | Allowed |

Additional access principles:

- Access is limited to authenticated internal users.
- Booking Users must be restricted to records where they are the requester.
- Booking Users must not change workflow decisions or another user's request.
- Vehicle maintenance and manager actions require the Booking Manager role.
- Deletion should be limited to a request owner's Draft records; later states retain an auditable history.

## 12. Future Enhancements

The following items are explicitly outside the MVP and require separate review:

- Reusable `aos_booking` foundation after cross-application reuse is confirmed
- Multi-level approvals and the planned `aos_approval` capability
- Approval delegation, escalation, and reminders
- Vehicle availability search or calendar visualization
- Driver and passenger management
- Recurring bookings
- Email or in-app notifications
- Attachments through a future document-management capability
- Fleet, maintenance, fuel, mileage, and cost integrations
- Multi-company and customer-specific policies
- Operational dashboards, analytics, and PDF reports
- Portal, mobile, GPS, map, or calendar integrations

Listing an enhancement does not approve or schedule its implementation.

## 13. Open Questions

1. Must a request start in the future, or may managers record same-day or past bookings?
2. May a Booking User cancel an Approved request, or must a manager always do so?
3. Is selecting a specific vehicle required from the requester, or may the manager assign it during review?
4. Is the destination required as free text, or should the first demo use a controlled location list?
5. Should a rejection reason always be visible to the requester?
6. Are all internal users allowed to request vehicles, or is membership in the Booking User role explicitly assigned?
7. Does the first customer demo require multi-company separation?
8. What minimum demo data should be prepared for vehicles and users?

These questions must be resolved before implementation where their answers affect models, workflow, security, or acceptance criteria.
