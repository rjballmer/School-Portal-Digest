# School Portal Digest

Read-only OpenClaw skill that does a daily check of school portals, providing high-signal parent action items, family calendar management, and check-in guidance at dinner with topics from the day to chat about.

It is designed for authenticated parent portals such as ParentSquare, Schoology, Seesaw, ClassDojo, Canvas, Google Classroom, and similar school sites.

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
