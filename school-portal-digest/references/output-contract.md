# Output Contract

## Date rule

Always use today's local date for the digest title and filename. If today is 2026-05-11, the file should be `summary-2026-05-11.md` and the heading should be `# School Portal Digest — 2026-05-11`. Do not copy dates from examples.

## Digest template

```markdown
# School Portal Digest — YYYY-MM-DD

## Scan Status
- Portal: Checked / Partially checked / Blocked
- Surfaces checked: [Forms, Posts, Messages, Calendar]
- Blockers: [None / Login required / MFA required / Calendar unavailable / Layout changed]

## 1. Action Items
- 🚨 **[Title]** — [Child / Family]
  - Status: Open / Completed / Needs review
  - Why it matters: [one short sentence]
  - Recommendation: [what parent should do next]

## 2. Child-Specific Calendar
- 📅 **[Event]** — [Child]
  - When: [date/time if known]
  - Where: [location if known]
  - Calendar status: Already present / Missing / Needs cleanup / Details incomplete
  - Recommendation: [add/update/ignore/review]

## 3. Worth Knowing
- 💬 [Specific classroom, teacher, social, academic, logistics, or developmental signal]

## 4. Check-In Guidance
- Ask [Child]: “[one natural question]”
- Optional family note: [one short tone recommendation]
```

## Style rules

- Lead with action. Parents are busy.
- Keep each item short and decision-oriented.
- Say “no clear action items” when quiet; do not invent work.
- Use child names only in private/local outputs. Public examples should use Child A / Child B.
- Do not include raw portal IDs, internal URLs, screenshots, or copied long portal text.
- Prefer exact dates and times over vague phrasing.
- If the portal is ambiguous, say what is missing.

## Partial-failure template

Use this when a run is blocked or incomplete:

```markdown
# School Portal Digest — YYYY-MM-DD

## Scan Status
- Portal: Partially checked
- Surfaces checked: Posts, Calendar
- Not checked: Forms, Messages
- Blocker: Login expired before Forms/Messages could load

## 1. Action Items
No new action items confirmed. Forms could not be checked, so this is incomplete.

## 2. Child-Specific Calendar
- 📅 **Class performance** — Child A
  - When: Thu May 14, 6:00–7:00 PM
  - Calendar status: Needs review; calendar access was unavailable.

## 3. Worth Knowing
- 💬 One classroom post was readable and mentioned the class performance.

## 4. Check-In Guidance
- Ask Child A: “How are you feeling about the performance?”
```

## Good examples

### Action item

```markdown
- 🚨 **Field trip permission form** — Child A
  - Status: Open
  - Why it matters: The form appears required before the class trip next Friday.
  - Recommendation: Review and sign in the portal.
```

### Completed reassurance

```markdown
- ✅ **Museum trip permission form** — Child B
  - Status: Completed
  - Why it matters: The portal shows the form as approved/signed; keeping it visible until the trip passes so you do not second-guess it.
```

### Calendar item

```markdown
- 📅 **Class performance** — Child A
  - When: Thu May 14, 6:00–7:00 PM
  - Where: School auditorium
  - Calendar status: Missing from Family calendar
  - Recommendation: Add to Family calendar.
```

### Worth knowing

```markdown
- 💬 Child B’s class has been working on persuasive writing this week. Good dinner question: “What argument did you make, and did you convince anyone?”
```

## Bad examples

### Too vague

```markdown
There are some school things to keep an eye on.
```

### Too much raw portal text

```markdown
The announcement says: [three paragraphs pasted from the school portal]
```

### Fake certainty

```markdown
Child A is clearly becoming more confident socially.
```

Better:

```markdown
Child A’s teacher mentioned a group presentation. If you ask about it, listen for whether the group work felt easy or stressful.
```
