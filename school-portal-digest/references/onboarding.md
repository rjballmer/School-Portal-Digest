# Onboarding Prompt

Use this when setting up the skill for a new family or school portal. The goal is to discover enough local context to run safely without collecting unnecessary private detail.

## Setup prompt

Use this shorter first prompt. Do not lead with a 13-question form unless the user asks for full manual setup.

```markdown
I can set this up in read-only mode. I won’t submit forms, RSVP, pay fees, message teachers, volunteer, or change school data.

To start, I only need five things:

1. Which portal do you use? ParentSquare, Schoology, Seesaw, ClassDojo, Canvas, Google Classroom, other?
2. What is the portal login URL or homepage?
3. What child labels should I use? First names, initials, or Child A / Child B are all fine.
4. Should calendar items be recommendation-only for now? Default: yes.
5. Do you want daily, weekly, or on-demand digests? Default: on-demand until the first review.

I’ll use privacy-safe defaults: no passwords in chat, browser login only, no raw portal text stored, avoid screenshots, no calendar writes yet.
```

After the user answers, create local files, do the read-only walkthrough, produce a first digest, and then ask optional tuning questions about aliases, suppression categories, calendar policy, delivery mode, and privacy.

Prefer using `scripts/init_school_portal_digest.py` to create local files. It stamps the setup with today's local date and creates a starter `summary-YYYY-MM-DD.md` so the first-run date is unambiguous.

## Optional tuning questions

Ask these after the first digest or if the user wants detailed setup:

1. Do you use more than one portal for the same child or school? If yes, set up a separate local config for each portal and combine summaries later.
2. Are there aliases I should recognize for each child? Examples: full name, nickname, classroom label.
3. What should count as parent-actionable? Examples: permission slips, forms, payments, volunteer asks, supplies to bring, registration, teacher replies.
4. What should go on the family calendar? Child-specific field trips, performances, conferences, sports, deadlines, school-wide events, or only some of those?
5. Should calendar entries stay recommendation-only, require confirmation, or eventually auto-add trusted event types?
6. Which calendar should be used for child-specific events, if any?
7. Are there categories you want suppressed? Examples: fundraisers, school-wide newsletters, lunch menus, generic district notices.
8. Where should local state live? Default: `school-portal/` in the current workspace.
9. Any privacy constraints? Examples: redact names in summaries, never store raw portal text, avoid screenshots, do not retain attachments.

## Minimal local config fields

Create or update `school-portal/config.json` from `assets/config.example.json`. Use these fields at minimum:

```json
{
  "portal": {
    "name": "",
    "loginUrl": "",
    "homeUrl": "",
    "browserProfile": "openclaw"
  },
  "family": {
    "children": [
      {
        "label": "Child A",
        "portalAliases": [],
        "calendarName": "Family"
      }
    ],
    "calendarWriteMode": "recommend-only"
  },
  "digest": {
    "cadence": "on-demand",
    "suppressCategories": [],
    "actionableCategories": ["forms", "permissions", "payments", "teacher replies", "supplies", "registration"],
    "calendarCategories": ["child-specific events", "field trips", "performances", "conferences"],
    "deliveryMode": "announce",
    "maxRetentionDays": 30
  },
  "privacy": {
    "redactNamesInSharedOutputs": true,
    "storeRawPortalText": false,
    "avoidScreenshots": true
  }
}
```

## First walkthrough checklist

0. Determine today's local date before creating files. Use that date for `summary-YYYY-MM-DD.md` and the digest heading; do not reuse template/example dates.
1. Start managed browser profile.
2. Open portal homepage.
3. Confirm whether user is logged in.
4. If login/MFA is needed, stop and ask the user to complete it.
5. Identify main navigation labels for:
   - forms / permissions / action center
   - posts / announcements / classroom feed
   - messages / inbox
   - calendar / events
   - alerts / notices
   - student dashboards
6. Create `site-config.json` from `assets/site-config.example.json` with discovered routes/labels.
7. Create `action-items.json` from `assets/action-items.empty.json`; do not copy sample items from `action-items.example.json` into live state.
8. Check `privacy.avoidScreenshots` before taking any screenshots for debugging.
9. Do a read-only test scan.
10. Produce a first digest with confidence notes.
11. Ask the user what was useful, noisy, missing, or too sensitive.

## Onboarding quality bar

Good onboarding:
- asks for labels, not unnecessary full identity
- lets the parent choose privacy level
- separates calendar recommendations from calendar writes
- treats portal login/MFA as user-owned
- creates config that can be edited later

Bad onboarding:
- asks for passwords in chat
- stores raw portal data by default
- assumes all school announcements matter
- enables calendar writes without explicit permission
- builds around one family’s private details
