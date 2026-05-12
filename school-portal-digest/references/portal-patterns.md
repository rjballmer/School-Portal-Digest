# Portal Patterns

## ParentSquare-like portals

Common surfaces:
- Forms / permissions
- Posts / feed
- Messages / chats
- Alerts / notices
- Student dashboards

Best workflow:
1. Forms first for open actions.
2. Expand visible form cards; collapsed status is often insufficient.
3. Treat approved/signed forms as completed, but still extract event logistics if useful.
4. Posts second for classroom events and developmental context.
5. Messages third for direct asks and exceptions.
6. Notices last unless urgent.

Common failure mode:
- Re-raising approved permission slips as open actions.

## LMS-style portals

Examples: Canvas, Schoology, Google Classroom.

Common surfaces:
- assignments
- grades / missing work
- announcements
- calendar
- messages

Best workflow:
1. Check missing/late assignments separately from announcements.
2. Do not turn every assignment into a parent action.
3. Surface only items requiring parent awareness, support, or logistics.
4. For older children, avoid creating micromanagement unless the user asks.

Common failure mode:
- Flooding parents with every assignment instead of exceptions and patterns.

## Classroom-sharing apps

Examples: Seesaw, ClassDojo, Bloomz.

Common surfaces:
- photos / activity posts
- behavior notes
- teacher messages
- event reminders

Best workflow:
1. Separate sentimental updates from actions.
2. Extract one or two good conversation hooks.
3. Avoid overinterpreting behavior points or one-off comments.
4. Flag direct teacher asks clearly.

Common failure mode:
- Turning every cute update into a fake developmental insight.

## Calendar-first school systems

Common surfaces:
- school calendar
- subscribed calendars
- district announcements

Best workflow:
1. Separate school-wide dates from child-specific events.
2. Dedupe against family calendar.
3. Add/update only with user-authorized calendar writes.
4. Preserve source and confidence in notes.

Common failure mode:
- Polluting the family calendar with every district-wide event.

## Authentication and blockers

Stop and ask the user when you encounter:
- login required and no stored credential path
- MFA/2FA
- CAPTCHA
- account chooser ambiguity
- payment/signature screens
- irreversible action prompts
- portal terms or consent flows

Do not try to bypass security controls.
