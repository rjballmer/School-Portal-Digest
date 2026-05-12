# Scheduled Runs

## Mental model

The skill package stays generic. The user’s local setup lives outside the skill package.

- `SKILL.md` = reusable behavior and guardrails
- `school-portal/config.json` = private family/portal preferences
- `school-portal/site-config.json` = discovered portal navigation map
- `school-portal/action-items.json` = persistent state across runs
- `school-portal/summary-YYYY-MM-DD.md` = generated digest
- `digest.deliveryMode` = whether to announce, write file only, or stay silent
- cron job = when and where to run the digest

A scheduled run should never need to rediscover everything. It should load local config/state, determine today's local date, perform a read-only scan, update state, write today's digest, and deliver the summary.

## First-run flow

1. User installs the skill.
2. User asks: “Set up school portal digest.”
3. Agent reads `references/onboarding.md`.
4. Agent asks the onboarding questions.
5. Agent creates local files with `scripts/init_school_portal_digest.py` when possible. If creating manually, use:
   - `school-portal/config.json` from `assets/config.example.json`
   - `school-portal/site-config.json` from `assets/site-config.example.json`
   - `school-portal/action-items.json` from `assets/action-items.empty.json`
6. User chooses an authentication mode: dedicated browser session, official OAuth/API token, local OS keychain/secret manager, or fail-closed manual refresh when login expires.
7. User completes first login or local secret setup as appropriate. Do not collect credentials in chat.
8. Agent performs a read-only walkthrough.
9. Agent records navigation labels/routes in `site-config.json`.
10. Agent produces the first digest.
11. User reviews what was useful, noisy, missing, or too sensitive.
12. Agent updates config/suppression rules.
13. Only after review should the user schedule recurring runs.

## Local config acquisition

The skill should acquire details in three ways:

### 1. User answers
Used for preferences and private family context:
- child labels / aliases
- actionable categories
- calendar policy
- digest cadence and schedule timing
- authentication mode and fallback preference
- privacy constraints
- categories to suppress

### 2. Browser walkthrough
Used for portal structure:
- route URLs
- navigation labels
- page names
- visible sections
- whether login/MFA is required
- which pages contain actions, posts, messages, calendar, alerts

### 3. Run feedback
Used to improve future runs:
- user says “this is noise” → add suppression rule
- user says “this is handled” → mark completed/dismissed
- user says “always include these” → update priority rules
- user says “never store raw text” → enforce privacy rule

Do not acquire:
- passwords in chat
- raw portal dumps by default
- screenshots unless necessary and approved
- school/student IDs in public examples or committed files

## Scheduled run contract

A recurring run should use this prompt shape:

```markdown
Run the School Portal Digest using the existing local config/state.

Rules:
- Determine today's local date first and use it for the summary filename and heading.
- Read `school-portal/config.json`, `school-portal/site-config.json`, and `school-portal/action-items.json`.
- Use the configured authentication mode and managed browser profile.
- Scheduled operation should be autonomous when the configured auth mode is valid; do not require manual login every run.
- Stay read-only in the school portal.
- Do not submit, sign, RSVP, pay, post, message, volunteer, or acknowledge anything.
- If login, MFA, CAPTCHA, payment, signature, consent, or irreversible action appears, stop and report the blocker.
- Scan configured surfaces in priority order: actions/forms, posts/feed, messages, calendar/events, alerts/notices, dashboards if configured.
- Classify findings as action, calendar, worth_knowing, check_in, noise, or needs_review.
- Update action-items state conservatively.
- Write `school-portal/summary-YYYY-MM-DD.md` using today's local date, not an example or previous-run date.
- Deliver a concise parent-facing digest with four sections: Action Items, Child-Specific Calendar, Worth Knowing, Check-In Guidance.
- Mention uncertainty and blockers plainly.
- Respect `digest.deliveryMode`: `announce`, `file-only`, or `none`.
```

## Cron setup guidance

Use OpenClaw cron for scheduled runs rather than shell sleep loops.

Recommended default for parent dinner/check-in use:
- **post-school-day update before dinner** so same-day signals can shape that evening's parent/child conversation

Other valid patterns:
- weekday mornings before school for logistics-first families
- Sunday evening weekly digest
- school-night evening digest

Use an isolated `agentTurn` job unless the user specifically wants the main session updated.

Example schedule concepts:
- `0 17 * * 1-5` for weekday 5:00 PM local post-school update
- `0 17 * * 0-5` for Sunday-through-Friday 5:00 PM local school-night/dinner rhythm
- `0 7 * * 1-5` for weekday 7:00 AM logistics review
- `0 18 * * 0` for Sunday 6:00 PM weekly review

Delivery mode should live in `config.json`:
- `announce` — send the digest in chat and write the file
- `file-only` — write the file, then send only a brief completion note if appropriate
- `none` — write files only; no chat delivery unless blocked

Use `digest.maxRetentionDays` to decide when old summaries can be archived or removed.

## Stale site-config recovery

If portal layout changes:
1. stop rather than guessing through the new UI
2. report which configured surface failed
3. preserve `action-items.json`
4. rerun only the navigation-discovery portion of onboarding
5. update `site-config.json.lastVerified`
6. retry the scan after the user confirms the new mapping looks reasonable

## State update rules during scheduled runs

- If an item remains visible and unresolved, update `lastSeen`.
- If an item is clearly completed, mark `completed`.
- If an item disappears and likely resolved, mark `completed` with low/medium confidence.
- If an item is stale or ambiguous, mark `needs-review`.
- If the user dismissed it, keep it suppressed.
- Do not resurrect dismissed items unless a new source/date clearly shows a new instance.

## Retention

Default retention is 30 days unless `digest.maxRetentionDays` says otherwise.

Prefer:
- keep recent summaries for trend/context
- archive or delete older generated summaries
- never retain raw portal dumps unless the user explicitly approved it
- preserve `action-items.json` longer than summaries because it prevents resurfacing handled items

## Failure modes

Stop and report:
- configured auth mode failed
- login expired
- MFA required
- CAPTCHA
- portal layout changed too much
- calendar access unavailable
- page requires submit/acknowledge to proceed
- permission boundary unclear

Do not silently skip the portal and produce a confident digest. Say what could and could not be checked.
