# Worker brief · global-footer (footer newsletter → Klaviyo)

**Created**: 2026-10-21

### Changelog
| Date | Change |
|------|--------|
| 2026-10-21 | Created at Victor's request: "nieuwe child global-footer en een connectie maken met https://mcp.klaviyo.com/mcp zodat we onze emaillijst kunnen koppelen met de email field in de footer. Zoek de bestpractices om correcte data te koppelen en door te geven aan Klaviyo". |
| 2026-10-21 | Supervision moved to the global coordinator (Victor: "je hebt een coordinator onder soft launch global gemaakt maar die stuurt precies de child niet aan?"). The worker reports to the global coordinator, not to the landing desk. Copy in the child worktree: `docs/global-footer/BRIEF.md`. |

Worktree `/Users/iamvictorious/IdeaProjects/orca-workspaces/karmicare-shopify-theme/global-footer`, branch `karmicare/global-footer` from `karmicare/soft-launch-global` 68dba1f; Orca child of the global lane.

**Your coordinator is the global lane** (`term_b762267d-e1a5-4f62-924d-793690a7046e`). It started you, answers your asks and relays Victor's decisions. It owns `sections/footer.liquid`; its R15 fixes (7efaa1e) are in review. The landing desk (Run `run_32dd5602b983`) only merges, after the global coordinator forwards your "Ready to land".

## Goal

Footer email signups land in the right Klaviyo list with valid consent and the data needed to mail people in their language (NL, FR, EN). Nothing runs before cookie consent.

## Start here

Read `docs/global-footer/KLAVIYO-RESEARCH.md` in this worktree (landing desk research, sources included). Recommended route: browser endpoint `POST /client/subscriptions` with the public key, no klaviyo.js; double opt-in lists, one per language; Shopify subscriber sync to a separate checkout list. Treat items marked *unverified* as open.

Today the footer posts Shopify's `{% form 'customer' %}` with `contact[tags]=newsletter` (`sections/footer.liquid` around l.705-750). The notice reads "By subscribing you agree to the Terms of Use & Privacy Policy" (`kc.footer.consent_html`). It does not say what people receive or that they can unsubscribe, and it bundles consent with the terms.

## Phase 1: inventory and plan (no theme code)

1. **Theme inventory.** Footer form, notice, success and error states, no-JS behaviour, consent banner (Shopify customer privacy), privacy-policy text on Klaviyo, any other signup form (popups, PDP, checkout opt-in).
2. **Klaviyo inventory, read-only via the `klaviyo` MCP.** Lists (name, ID, size, opt-in type if visible), segments, signup forms, flows. Flag the Webflow-era list (`Y8tAjz`). List what the MCP cannot show (Shopify integration settings, double opt-in setting, public key, sender domain, consent sync) as a checklist for Victor to read in Klaviyo's UI.
3. **`docs/global-footer/PLAN.md`.**
   - The route and why.
   - The list design: NL / FR / EN double opt-in plus a checkout list.
   - The exact request payload: list per `request.locale`, `locale` = `nl-BE` / `fr-BE` / `en`, `custom_source` = `Footer newsletter · <lang>`, properties `signup_path` and `consent_text_version`. No `external_id`, no name.
   - A no-JS fallback: the native Shopify form keeps working.
   - One neutral "check your inbox" message for every 202.
   - The error, `aria-invalid` and `role="status"` states.
   - Proof that no Klaviyo request fires before submit.
   - Where the public key and list IDs live (footer section settings, empty by default so the native form stays active until filled).
   - A notice proposal in EN: who, what, unsubscribe any time, a visible privacy link, no terms bundling.
   - The decisions Victor needs to make, each with a recommendation.

   Then send one `ask` to your coordinator with the decisions. Wait for Victor's "ja".

## Phase 2: build (only after "ja" and after your coordinator says global R15 has landed)

- `git merge karmicare/soft-launch-global` first.
- Build in `sections/footer.liquid` plus one small theme asset. Progressive enhancement: the native form stays the fallback.
- New or changed customer strings: do not edit `locales/*.json`. The source-copy lane's `theme_keys.py` is the single writer for locale keys. List each key with its EN text in `docs/global-footer/KEYS.md`; your coordinator routes it to the NL and FR lanes.
- `node --check` and Theme Check (0 errors). Commit pathspec-only.
- Send `worker_done` to your coordinator with the SHA. It checks your work and forwards `Ready to land: global-footer` to the landing desk, which runs the Astra review.

## Rules

- Klaviyo MCP is **read-only** (`?read-only=true`). Never create, subscribe, import, suppress, merge or delete in Klaviyo. Lists are created by Victor in Klaviyo's UI.
- No real-person signups. A live test submit writes customer data and sends a mail. Only Victor does it, with his own address, after the build. You may not submit forms.
- No secrets anywhere. The Klaviyo public key and list IDs are public identifiers. Never a private key (`pk_…`), never an OAuth token.
- Never: push, publish, Shopify or Klaviyo admin writes, settings, permission or MCP config changes, `config/settings_data.json`, Loop widget files, subagents.
- Never: reset, amend, rebase or stash. A denied command stays denied: report it, don't route around it.
- Storefront fetches on `karmicares.myshopify.com` at least 2.5 s apart.
- Victor reads Dutch: short, results first.
