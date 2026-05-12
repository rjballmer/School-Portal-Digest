---
name: school-portal-digest
description: Create parent-facing school portal digests from ParentSquare, Schoology, Seesaw, ClassDojo, Canvas, Google Classroom, email-like school portals, or similar authenticated parent sites. Use for read-only school checks, action-item tracking, kid-specific calendar extraction, parent reminders, and lightweight dinner/check-in guidance while preserving privacy and avoiding accidental portal actions.
---

# School Portal Digest

## Purpose
Turn noisy school-portal updates into a calm parent digest:
1. what needs parent action
2. what belongs on the family calendar
3. what is worth knowing about the child’s day or development
4. what to ask about at dinner or bedtime

This skill is designed for autonomous, read-only authenticated browsing after the parent chooses an approved local authentication model. It should reduce parent cognitive load without submitting forms, sending messages, RSVP-ing, volunteering, or changing school data.

## Requirements

- Browser automation is required for authenticated portal walkthroughs.
- Calendar access is optional; without it, produce calendar recommendations or `.ics` files instead of checking/updating a live calendar.
- A local project folder such as `school-portal/` is required for private config and run state.

## Safety rules

1. **Personal parent use only.** This skill is for parents or guardians accessing their own authorized school portals. Review the portal's terms of service before scheduling recurring scans; do not use it for bulk, commercial, or unauthorized access.
2. **Read-only by default.** Never submit, sign, RSVP, pay, volunteer, post, message, or acknowledge anything unless the user explicitly asks and confirms the exact action.
3. **Do not expose children’s private data.** Keep names, school IDs, class names, teacher names, and portal URLs in local config, not in reusable skill files or public output examples.
4. **Never print credentials, cookies, tokens, or raw portal dumps.** Summarize only the parent-relevant findings.
5. **Separate school-wide noise from child-specific signals.** School-wide announcements do not automatically belong in the family calendar.
6. **Prefer uncertainty over false confidence.** Mark ambiguous, stale, or partially visible items as `needs-review`.
7. **Do not delete calendar entries without explicit confirmation.** If calendar tools are available, add/update only when the user has allowed that behavior.

## Onboarding a new family

When setting this up for a new family or portal, first read `references/onboarding.md` and use the setup prompt there. Discover only the minimum family-specific details needed for safe operation: portal name/URL, child labels or aliases, actionable categories, calendar preferences, suppression preferences, digest cadence, and privacy constraints.

Use `scripts/init_school_portal_digest.py` to create the local setup folder when possible. It creates config, site-config, empty action state, a calendar folder, and a starter summary for today. Use `--validate --target <folder>` to check an existing setup without changing files.

For families using multiple portals, prefer one local config folder per portal unless the user explicitly asks for a combined setup.

Do not ask for passwords in chat. During onboarding, ask how the parent wants authentication managed for scheduled runs: dedicated browser session, official OAuth/API token, OS keychain/secret manager, environment token, or fail-closed manual refresh when login expires. Read `references/credential-model.md` when deciding how authentication should work.

## Scheduled operation

For recurring checks, keep all family-specific state outside the skill package. A scheduled run should load local config/state, use the configured auth mode, perform a read-only scan, update `action-items.json`, write the daily summary, and deliver the digest if configured.

For parent evening check-ins, prefer a post-school-day run before dinner so same-day signals are captured while they are still useful.

Read `references/scheduled-runs.md` before creating or modifying a recurring job.

## Expected local files

Use project-local files outside the skill package, for example `school-portal/`:

- `config.json` — private account, children, school, calendar, and portal details; never commit if it contains real data
- `site-config.json` — portal routes, labels, selectors, and scan order
- `action-items.json` — persistent action state; start empty for a new family
- `summary-YYYY-MM-DD.md` — daily digest artifact
- `calendar/` — optional generated `.ics` fallback files

Use `assets/config.example.json` and `assets/site-config.example.json` as starting templates. Use `assets/action-items.empty.json` for live state. Use `assets/action-items.example.json` only as an example reference, not as a starting state file. Use `assets/config.schema.json`, `assets/site-config.schema.json`, and `assets/action-items.schema.json` as machine-readable structure contracts when validating or extending local state.

## Browser approach

If using OpenClaw browser control:
1. start or reuse the managed browser profile
2. confirm login state
3. open the configured portal landing page
4. inspect pages via snapshots / readable text
5. click only navigation, expansion, filtering, and read-more controls
6. stop and ask if a page presents a submit/sign/pay/send/RSVP action

For fragile portals, use stable labels or URLs from `site-config.json` rather than relying on remembered UI state.

## Signal surfaces

Scan the portal in this priority order when available:

1. **Forms / permissions / action center** — highest value for parent action
2. **Posts / announcements / classroom feed** — best for dates and developmental context
3. **Messages / inbox** — exceptions, direct asks, teacher notes
4. **Calendar / events** — dates, times, locations, duplicates
5. **Alerts / notices** — include only if materially important
6. **Student dashboards** — optional, when needed for child-specific context

Portal-specific names vary. Map them in `site-config.json`.

## Classification model

Classify each finding as one of:

- `action` — parent must sign, RSVP, pay, register, bring, complete, confirm, reply, or decide
- `calendar` — child-specific event with enough date/time/location detail to track
- `worth_knowing` — teacher/classroom/developmental signal useful to the parent
- `check_in` — lightweight question or encouragement for the child
- `noise` — generic, repeated, stale, or low-value
- `needs_review` — ambiguous or potentially stale item

## Action state rules

Use `action-items.json` to prevent resurfacing the same item forever.

Statuses:
- `open` — clearly unresolved
- `completed` — portal shows done, item disappeared in a resolution-like way, or user marked it handled
- `needs-review` — ambiguous, stale, or low-confidence
- `dismissed` — user explicitly said to ignore/suppress

When a completed item is tied to a future event, keep it visible briefly as a reassuring “done” signal until the event passes.

## Calendar handling

Before recommending or adding events:
1. identify child relevance
2. extract title, date, time, location, child, source, and confidence
3. check the family calendar if available
4. avoid duplicating existing entries
5. add/update only if the user has authorized calendar writes
6. otherwise produce a clear recommendation or `.ics` fallback

Do not add broad school-wide events to a child/family calendar unless the user wants them there.

## Date handling

At the start of each run, determine today's local date and use it consistently for generated files and headings, e.g. `summary-YYYY-MM-DD.md` and `# School Portal Digest — YYYY-MM-DD`. Never reuse example dates from templates or previous summaries.

## Output contract

Produce a concise parent-facing digest with four sections:

### 1. Action Items
Only what the parent likely needs to handle. Include status and recommendation.

### 2. Child-Specific Calendar
Events worth tracking. State whether each is already present, missing, duplicated, incomplete, or needs review.

### 3. Worth Knowing
Context that helps the parent understand school life without creating admin burden.

### 4. Check-In Guidance
One or two specific, lightweight child-aware prompts. Do not manufacture insight when signals are quiet.

See `references/output-contract.md` for examples and formatting guidance.

## Quality bar

Good digest:
- short enough to read in one minute
- action-first
- child-specific where possible
- explicit about uncertainty
- avoids generic parenting advice
- preserves privacy

Bad digest:
- repeats the whole portal
- mixes action items with school newsletter noise
- nags about already-handled forms
- invents developmental meaning from weak signals
- includes raw IDs, links, credentials, or private portal text dumps

## When to read references

- Read `references/onboarding.md` when setting up a new family, portal, calendar policy, or local config.
- Read `references/credential-model.md` when handling login, browser session reuse, MFA, API credentials, or secret-storage questions.
- Read `references/scheduled-runs.md` when creating recurring checks, cron prompts, or run-state behavior.
- Read `references/output-contract.md` when producing or revising the digest format.
- Read `references/portal-patterns.md` when adapting the workflow to a new portal.
