# Credential Model

## Best-practice default: local browser-session authentication

The recommended credential model is: **the user logs into the school portal locally in a managed browser profile; the skill reuses that authenticated browser session for read-only navigation.**

The skill must not ask the user to paste passwords, MFA codes, cookies, session tokens, or recovery codes into chat.

This skill is intended for personal parent/guardian use against portals the user is already authorized to access. The user should review their portal’s terms of service before enabling recurring scans. Do not use this skill for bulk access, commercial monitoring, credential sharing, or unauthorized accounts.

## Why this is the default

School portals often use:
- SSO
- MFA / 2FA
- CAPTCHA
- district identity providers
- mobile-app confirmation
- short-lived sessions
- anti-automation protections

Direct credential storage is fragile and risky. Browser-session auth is safer, more compatible, and keeps the user in control of login and MFA.

## Authentication hierarchy

Use the safest available option:

1. **Managed browser session** — default for most portals.
2. **Official API OAuth / scoped token** — only when the portal documents and supports it.
3. **OS keychain / secret manager** — advanced local setup, only when unavoidable.
4. **Environment variables** — acceptable for non-public local API tokens, not preferred for passwords.
5. **Plaintext credentials in config or chat** — do not use.

## First login flow

1. Start or open the configured managed browser profile.
2. Navigate to the portal login URL.
3. If login is required, ask the user to complete login in the browser.
4. If MFA/CAPTCHA/SSO appears, wait for the user to complete it.
5. After login succeeds, continue the read-only onboarding walkthrough.
6. Do not read, export, print, screenshot, or store cookies/tokens.

## Profile isolation

Prefer a dedicated browser profile for school-portal work.

Benefits:
- limits accidental cross-site data exposure
- keeps login state separate from general browsing
- makes troubleshooting easier
- lets the user revoke access by clearing that profile

Do not commit browser profile directories, cookies, local storage, cache files, screenshots, or traces.

## What may be stored locally

Allowed in `school-portal/config.json`:
- portal name
- login URL / home URL
- browser profile name
- child labels or aliases
- digest cadence
- calendar policy
- privacy preferences
- suppression categories

Avoid storing:
- passwords
- MFA secrets
- recovery codes
- cookies
- bearer tokens
- raw screenshots
- raw portal dumps
- full message exports
- unnecessary school/student IDs

## Optional advanced modes

### Password manager assisted login
If the user's browser or password manager fills credentials, let the user control that. Do not extract, log, or persist the password.

### Official API mode
Use API credentials only when all are true:
- the portal offers a documented API or approved export mechanism
- the user explicitly chooses API mode
- access can be scoped or revoked
- secrets live in an OS keychain, secret manager, or local environment outside git
- logs redact tokens and response bodies by default

Do not invent unofficial credential flows for school portals.

### Environment variables
Environment variables may be acceptable for local API tokens in advanced setups. Avoid using them for raw passwords unless the user explicitly accepts the risk and there is no better option.

Use names that make the portal-specific boundary clear, for example:

```bash
SCHOOL_PORTAL_API_TOKEN=
SCHOOL_PORTAL_CLIENT_ID=
```

Do not include real values in docs, examples, logs, or committed files.

### OS keychain / secret store
For advanced local setups, credentials may live in an OS keychain or secret manager. The skill should still avoid printing secrets and should prefer read-only access.

## Scheduled-run auth behavior

A scheduled run should first test whether the browser session is authenticated.

If authenticated:
- proceed with read-only scan

If not authenticated:
- stop and report: `Login required`
- do not ask for password in chat
- ask the user to log in through the browser

If MFA/CAPTCHA appears:
- stop and report the blocker
- do not attempt bypass

If the portal blocks automation or terms are unclear:
- stop and report the issue
- ask the user how they want to proceed

## Logging and retention

Default to minimal retention:
- store summaries and action state, not raw portal pages
- redact names in shared examples
- avoid screenshots unless required for debugging and approved
- delete temporary page dumps after extraction
- never include secrets in error messages

## Public examples

Public examples must use fake portal URLs, fake child labels, fake school names, fake dates, and no real account details.
