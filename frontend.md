# Frontend Overview

This document describes the frontend layer for the Django-based Employee Management App, covering UI architecture, page templates, styling, utilities, and how to customize or troubleshoot.

## Stack and Architecture

- Templating: Django Template Language with template inheritance via `base.html`
- CSS Framework: Bulma (via CDN with runtime fallback)
- Icons: Font Awesome (via CDN)
- App Overrides: `static/css/app.css` (lightweight custom styles)
- Template Utilities: Custom filters (`add_class`, `add_attr`) to style Django form widgets without extra dependencies

Directory layout:
- templates/
  - base.html
  - registration/
    - login.html
  - employee/
    - home.html
    - register.html
    - profile.html
    - profile_edit.html
  - poll/
    - poll_list.html
    - poll_detail.html
    - poll_create.html
    - choice_create.html
- static/css/
  - app.css
- employee/templatetags/
  - __init__.py
  - form_extras.py

Relevant Django settings:
- `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`

Project URLs (`ems/urls.py`):
- `path('accounts/', include('django.contrib.auth.urls'))` (login/logout/password routes)
- `path('', include('employee.urls'))`
- `path('polls/', include('poll.urls'))`

## Base Layout: templates/base.html

Purpose: Provide a shared shell for all pages (navbar, messages, layout container, and overridable blocks).

Key features:
- CSS and Icons
  - Bulma (primary): `https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css`
  - Font Awesome: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css`
  - App overrides: `{% static 'css/app.css' %}`
- CDN Fallback
  - On `DOMContentLoaded`, a small JS probe checks if Bulma styles are applied. If not, it injects a jsDelivr Bulma stylesheet:
    - `https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css`
  - This increases the chance CSS loads even if a single CDN is blocked.
- Navbar (Bulma)
  - Left: Home, Polls
  - Right (auth-aware):
    - Authenticated: Profile, Logout
    - Anonymous: Login, Register
  - HR (staff-only) dropdown: Create Poll, Create Choice
- Messages
  - Renders Django messages using Bulma `notification` components (`is-success`, `is-danger`, `is-warning`, `is-info`), with close buttons
- Blocks for extension
  - `block title` — sets document title
  - `block content` — main page content
  - `block extra_css` — page-specific styles, if needed
  - `block extra_js_head` & `block extra_js` — page-specific scripts
- Small JS utilities
  - Navbar burger toggle (mobile view)
  - Notification close button behavior

## Styling: static/css/app.css

`app.css` contains small, framework-friendly adjustments that complement Bulma without a build step:
- Basic spacing for sections, boxes, and utility margin classes (`.mt-*`, `.mb-*`)
- Baseline styles for Django-rendered widgets in case a field doesn’t have Bulma classes applied
- Button and table minor tweaks

Use cases:
- Provide consistent spacing and polish across pages
- Add page-specific overrides within templates using `block extra_css` when necessary

## Template Utilities: employee/templatetags/form_extras.py

Custom filters to style Django form fields directly in templates:
- `add_class(field, css)`: add extra CSS classes to the widget
  - Example: `{{ form.username|add_class:"input" }}`
- `add_attr(field, "key:value")`: add or override a single widget attribute
  - Example: `{{ form.username|add_attr:"placeholder:Your username" }}`

These filters help keep styling near the templates (Bulma class names), with zero additional dependencies like crispy-forms.

## Pages

### Authentication

- templates/registration/login.html
  - Uses Django auth’s login view, styled with Bulma via `add_class`
  - Provides “Forgot password?” (`password_reset`) link from built-in auth URLs
  - Buttons: Login + link to Register

### Employee

- templates/employee/home.html
  - Light hero-style welcome with quick actions:
    - View Polls
    - If authenticated: Profile
    - Else: Login / Register
  - Quick links box (e.g., All Polls, Create Poll/Choice for staff, Profile actions)
- templates/employee/register.html
  - Registration using Django’s `UserCreationForm`
  - `add_class` and `add_attr` apply Bulma styling and placeholders
- templates/employee/profile.html
  - Displays logged-in user details (username, first/last name, email)
  - Shows linked `Profile` data (designation, salary) if present
  - Buttons to Edit Profile and View Polls
- templates/employee/profile_edit.html
  - Simple POST form to update `designation` and `salary`
  - Bulma inputs and grouped action buttons

### Polls

- templates/poll/poll_list.html
  - Lists polls split into “Active” and “Inactive” cards
  - Staff users see a “Create Poll” CTA
  - Each poll card links to `poll_detail`
- templates/poll/poll_detail.html
  - Displays poll title, date tags, and “Active/Inactive” status
  - Radio-list choices; Submit button is disabled if inactive or no choices
  - On submission, shows Django messages (note: vote persistence is not implemented in current models—UI only)
- templates/poll/poll_create.html
  - Staff-only form to create polls (title, start/end dates, active flag)
- templates/poll/choice_create.html
  - Staff-only form to add choices to an existing poll (select poll + text input)

## URL Navigation (Frontend-Relevant)

- Navbar routes:
  - Home: `name='home'`
  - Polls: `name='poll_list'`
  - HR Dropdown:
    - `name='poll_create'`
    - `name='choice_create'`
  - Auth:
    - `name='login'`, `name='logout'`, `name='register'`
  - Profile:
    - `name='profile'`, `name='profile_edit'`
- The navbar uses named URLs so links remain stable if path segments change.

## How to View Locally

1. Ensure dependencies are installed for the Django project.
2. Start the development server:
   ```
   python manage.py runserver
   ```
3. Visit:
   - Home: `http://127.0.0.1:8000/`
   - Login: `/accounts/login/`
   - Register: `/register/`
   - Profile: `/profile/` (edit at `/profile/edit/`)
   - Polls: `/polls/` (staff: `/polls/create/`, `/polls/choice/create/`)
4. Hard refresh (Ctrl+F5 / Cmd+Shift+R) to bypass cache when validating CSS changes.

## Customization Tips

- Colors and Components
  - Swap Bulma classes like `is-primary`, `is-link`, `is-warning`, etc. for different color accents.
  - Use Bulma components (`hero`, `section`, `box`, `columns`) for consistent layout patterns.
- Forms
  - Apply `add_class:"input"` to input fields in templates to guarantee Bulma styling.
  - For `<select>`, wrap with Bulma’s `.select` container when not using Django widget rendering that adds classes.
- Page-Specific Styles or Scripts
  - Add CSS within `block extra_css`.
  - Add JS in `block extra_js_head` (before body content) or `block extra_js` (end of body).

## Troubleshooting

- “Page looks plain/un-styled”
  - Confirm Internet access to CDNs (cdnjs & jsDelivr). The fallback attempts jsDelivr if cdnjs fails to apply.
  - Open DevTools → Network and verify `bulma.min.css` loads with status 200.
  - Ensure `static/css/app.css` is served (in dev, `DEBUG=True` does this automatically).
  - If both CDNs are blocked (offline/firewalled), vendor Bulma locally by copying the stylesheet into `static/` and updating `base.html` to reference the local file.
- “Icons not visible”
  - Verify Font Awesome CSS loads and that icons use the correct class names (e.g., `fa-solid fa-user`).

## Future Enhancements

- Optional React polling widget:
  - Mount a React component on `poll_detail` to submit votes via `fetch` and update results dynamically.
  - Keep current templates for no-build simplicity; React would be a progressive enhancement.
- Vote persistence & results view:
  - Add `Vote/Answer` model and render counts/totals; display a summary graph or table in `poll_detail`.
