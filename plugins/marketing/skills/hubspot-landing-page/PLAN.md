# Idea: Automate HubSpot uploads

Right now nothing in this repo actually uploads to HubSpot — assets are
uploaded manually through the HubSpot UI. The library just guesses the resulting URL from a hardcoded
uploaded manually through the HubSpot UI.

## The idea

Add a small upload script that calls
HubSpot's Files API directly to upload an asset and get back the real
hosted URL from the API response.

## Where the API key goes

Not in the plugin. A HubSpot private-app token would be a local environment
variable (`HUBSPOT_API_KEY`), set per-person on their own machine — via
their shell profile or Claude Code's `settings.local.json` (gitignored,
never committed). The script reads it from the environment and fails with
clear setup instructions if it's missing. Document the variable name (no
real value) in a `.env.example` so it's discoverable.

## Rough shape

1. Script takes a local file + target HubSpot folder, uploads via the Files
   API, and returns the asset's real `url` from the response.
2. If wired into the media-library catalog, that real URL replaces the
   guessed one currently written by `sync-hubspot-links.mjs`.
3. Needs a HubSpot private app with file-manager scopes — someone has to
   create that in the HubSpot account and hand out a token per user (or a
   shared one, if that's acceptable for this team).

## Open questions to answer before building

- Shared HubSpot token for the team, or one per person?
- Rate limits / retry behavior for batch uploads.
