# School Portal Digest

School portals bury the important stuff — permission slips, event dates, teacher notes, forms, reminders — inside a stream of announcements and classroom updates.

School Portal Digest is a read-only parent assistant that scans authenticated school portals and turns noisy updates into a calm daily digest: what needs action, what belongs on the family calendar, what is worth knowing, and what to ask about at dinner.

It is designed for portals such as ParentSquare, Schoology, Seesaw, ClassDojo, Canvas, Google Classroom, and similar authenticated school sites. The current implementation ships as an OpenClaw skill, but the core pattern is portable: browser/API access, local private state, careful classification, and explicit parent confirmation before any external action.

## What it does

- identifies parent action items
- extracts child-specific calendar signals
- separates school-wide noise from useful family context
- produces lightweight dinner/check-in guidance
- keeps private family state outside the reusable skill package

## Safety posture

- read-only by default
- autonomous scheduled operation after the parent chooses an auth mode
- no passwords, MFA codes, cookies, or tokens in chat
- supports dedicated browser-session auth, official OAuth/API tokens, or local keychain/secret-manager references
- no submit/sign/pay/RSVP/message/volunteer actions without explicit confirmation
- local config and state stay outside the skill package

## Contents

- `school-portal-digest/` — source skill
- `school-portal-digest/assets/*.schema.json` — machine-readable config/state schemas
- `school-portal-digest/scripts/init_school_portal_digest.py` — local setup and validation helper
- `tests/` — automated tests for setup, validation, URL checks, dry-run, and idempotency
- `dist/school-portal-digest.skill` — packaged skill artifact

## Local setup

Install the skill, then ask your OpenClaw assistant to set up School Portal Digest.

The skill includes an initializer:

```bash
python3 school-portal-digest/scripts/init_school_portal_digest.py \
  --target school-portal \
  --portal-name ParentSquare \
  --login-url 'https://example.edu/login' \
  --children 'Child A,Child B'
```

This creates local private state files and a starter summary for today's local date. The default cadence is a post-school-day update before dinner, so same-day school signals can shape evening check-ins. Do not commit real `school-portal/` runtime folders.

Validate an existing local setup without changing files:

```bash
python3 school-portal-digest/scripts/init_school_portal_digest.py \
  --target school-portal \
  --validate
```

Preview setup without writing files:

```bash
python3 school-portal-digest/scripts/init_school_portal_digest.py \
  --target school-portal \
  --dry-run
```

Run the automated tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## License

MIT License. See `LICENSE`.
