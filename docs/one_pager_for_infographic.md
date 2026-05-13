# School Portal Digest — One-Pager for Infographic

## Core idea

School portals are noisy. Parents need to know what actually matters: actions to take, dates to remember, and a few meaningful prompts to connect with their children.

School Portal Digest is a read-only agent skill that scans authenticated school portals and turns scattered updates into a calm, parent-facing digest.

**Tagline:** Less portal noise. More prepared parents.

## Who it is for

- parents and guardians managing school logistics
- families with multiple children, classrooms, portals, or calendars
- caregivers who want action items without reading every announcement
- AI assistants helping families stay organized without taking unsafe actions

## The problem

School communication is fragmented across:

- ParentSquare
- Schoology
- Seesaw
- ClassDojo
- Canvas
- Google Classroom
- school calendars
- classroom feeds
- inbox-style messages
- forms and permission slips

Parents face recurring friction:

- important forms hide among announcements
- calendar-worthy events are mixed with school-wide noise
- child-specific updates are hard to separate from generic posts
- the same item resurfaces repeatedly
- portals require login and manual checking
- assistants must not accidentally submit, RSVP, pay, or message anyone

## What the skill does

School Portal Digest performs read-only portal checks and produces a concise digest with four sections:

1. **Action Items** — forms, RSVPs, payments, permissions, supplies, replies, decisions
2. **Child-Specific Calendar** — events worth tracking for a specific child/family
3. **Worth Knowing** — classroom or developmental context that helps parents understand the child’s day
4. **Check-In Guidance** — one or two lightweight dinner/bedtime prompts

## Safety posture

The skill is intentionally conservative.

- Read-only by default
- No passwords, cookies, tokens, or MFA codes in chat
- No submit/sign/pay/RSVP/message/volunteer actions without explicit confirmation
- Private family state stays outside the reusable skill package
- Ambiguous items are marked `needs-review`
- Calendar writes are optional and require authorization
- Raw portal dumps are not exposed in summaries

## Dependency boundaries

The skill should not recreate every portal/browser/calendar system. It assumes the host environment may already provide capabilities such as:

- **Browser automation:** authenticated portal navigation, snapshots, readable page text
- **Credential/session handling:** browser profile, OAuth, keychain, secret manager, or manual login refresh
- **Calendar access:** check existing family events, add/update authorized events, or generate `.ics` files
- **Notification delivery:** send digest by chat, email, or local file
- **Local storage:** private config, action state, daily summaries, and calendar fallbacks

The skill adds the family-safe orchestration layer:

```text
existing access tools provide portal/calendar access
School Portal Digest provides classification, dedup, state tracking, safety rules, and parent-facing output
```

## Signal classification

Every finding is classified as one of:

- `action` — parent likely needs to do something
- `calendar` — child-specific event worth tracking
- `worth_knowing` — useful classroom/development context
- `check_in` — lightweight prompt for parent-child conversation
- `noise` — generic, stale, repeated, or low-value
- `needs_review` — ambiguous or partially visible item

## Local state model

A family setup keeps private state outside the skill package:

- `config.json` — portal, child labels, calendar policy, digest preferences
- `site-config.json` — portal routes, labels, scan order
- `action-items.json` — persistent open/completed/dismissed/needs-review state
- `summary-YYYY-MM-DD.md` — daily digest artifact
- `calendar/` — optional `.ics` fallback files

## Build/repo expectations

A reusable repo should include:

- skill instructions
- setup script
- config schemas
- example redacted config
- output examples
- tests for validation and idempotency
- one-pager and infographic source
- clear privacy/safety notes

## Infographic visual suggestion

Use a four-panel flow:

```text
Portal Noise → Read-Only Scan → Parent Signal Filter → Calm Family Digest
```

Show portal inputs on the left: forms, posts, messages, calendar.  
Show digest outputs on the right: action items, child calendar, worth knowing, check-in prompts.  
Use a safety banner underneath: “Read-only by default. Parent confirms before any external action.”
