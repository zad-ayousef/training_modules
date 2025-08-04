# purchase_request

Odoo 18 module for managing purchase requests with a robust approval workflow, status-driven field security, and automated manager notifications.

---

## Key Fields

- **name:** Request name (required)
- **requested_by:** Request creator (defaults to current user)
- **status:** Workflow state
- **order_lines_ids:** List of order lines
- **is_editable:** Controls edit permissions based on status
- **reason:** Rejection reason (readonly)
- **total_price:** Dynamic sum of all request line totals

---

## Core Methods

- **action_submit_for_approval:** Moves request to “to_be_approve”
- **action_approve:** Sets to approved, locks editing, sends email to Purchase Managers
- **action_reject:** Triggers wizard for mandatory rejection reason
- State transitions trigger additional logic (like notifications)

---

## purchase_request_views.xml

- Defines tree and form views for purchase requests
- Adds dynamic workflow buttons for transitions
- Controls field editability, and displays order lines inline

---

## base_menu.xml

- Integrates the module under the standard Odoo Purchase menu

---

## rejected_reason_wizard.py & rejected_reason_wizard_view.xml

- Provides a popup wizard to capture the rejection reason before a request is moved to "Rejected"
- **action_confirm:** Copies the reason to the original request and completes the transition

---

## Key Technologies

- Odoo ORM (regular and transient models)
- One2many / Many2one relationships
- Dynamic compute fields
- Conditional field editability, statusbars
- XML-defined forms and workflow buttons
- Wizard pop-ups for business logic
- Notification emails with mail.mail
- Group-based access control

---

## Business Logic Flow

1. User creates a draft purchase request.
2. Submits for approval; editing is locked.
3. Manager can approve (triggers notification email), reject (opens wizard for reason), or cancel/reset.
4. If rejected, the wizard captures and stores the reason.
5. In approved, rejected, or cancelled states, all fields become readonly for clarity and auditing.

