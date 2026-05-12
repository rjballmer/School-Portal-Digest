# School Portal Digest

A privacy-first OpenClaw skill that turns school portal noise into a short parent digest:

1. parent action items
2. child-specific calendar signals
3. worth-knowing school context
4. lightweight dinner/check-in prompts

Works with ParentSquare-like portals, Schoology, Seesaw, ClassDojo, Canvas, Google Classroom, email-like school portals, or similar authenticated parent sites.

## Requirements

- OpenClaw with browser automation available
- A managed browser profile the user can log into locally
- Optional calendar access if you want live calendar checks or writes

## Terms of service

This skill is intended for personal parent/guardian use against school portals you are already authorized to access. Review your portal's terms of service before enabling scheduled scans. Do not use this for bulk access, commercial monitoring, credential sharing, or unauthorized accounts.

## Safety model

Default mode is read-only.

The skill will not:
- submit forms
- sign permission slips
- RSVP
- pay fees
- message teachers
- volunteer
- acknowledge notices
- bypass login, MFA, CAPTCHA, or access controls

The user logs into the portal locally in the browser. The skill reuses the authenticated browser session but does not ask for or store passwords.

## What it cannot do

This skill cannot bypass login, MFA, CAPTCHA, paywalls, portal restrictions, or terms-of-service limits. It cannot guarantee that every school portal layout will work without a discovery pass. It should stop and ask when a page requires an action or when the permission boundary is unclear.

## Setup

Install the skill, then ask your OpenClaw assistant:

```text
Set up school portal digest.
```

The assistant should start with five basics:
- portal name
- portal URL
- child labels
- calendar recommendation/write preference
- digest cadence

Use initials or Child A / Child B if you prefer not to store names. The assistant can ask optional tuning questions after the first digest.

You can also initialize the local folder directly:

```bash
python3 scripts/init_school_portal_digest.py \
  --target school-portal \
  --portal-name ParentSquare \
  --login-url 'https://example.edu/login' \
  --children 'Child A,Child B'
```

The script creates today's starter summary using your local date.

## Local files

The skill creates local state outside the skill package, usually:

```text
school-portal/
  config.json
  site-config.json
  action-items.json
  summary-YYYY-MM-DD.md
  calendar/
```

Do not commit real `config.json`, raw portal text, screenshots, cookies, or private family data to a public repository.

## Authentication

Recommended path:

1. The assistant opens the school portal in the managed browser.
2. You log in yourself.
3. You complete any MFA/CAPTCHA/SSO flow.
4. The assistant continues only after login succeeds.

If a scheduled run finds that login expired, it stops and reports `Login required`.

## Multiple portals

If your school uses multiple portals — for example one for announcements and another for classroom updates — set up one local config per portal first. After each portal works reliably, you can combine the summaries.

## Scheduling

After first-run review, ask:

```text
Schedule this school portal digest for weekday mornings.
```

Recommended schedules:
- weekday morning before school
- Sunday evening weekly digest
- on-demand only

Recurring jobs should load local config/state, perform a read-only scan, update action state, write the digest, and deliver the summary if configured.

## Privacy best practices

- Use child labels instead of full names if desired.
- Store summaries, not raw portal dumps.
- Avoid screenshots unless truly needed.
- Keep calendar writes recommendation-only until you trust the workflow.
- Review the first few digests before enabling recurrence.

## Public example policy

All examples in this repo should use fake portals, fake children, and fake school data.
