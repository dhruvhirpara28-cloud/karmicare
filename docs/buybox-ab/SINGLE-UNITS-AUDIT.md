# Single units: why they stay available, and how to hide them but keep the Loop upsell

Audit for Victor via the desk (task_1365bc4c87bf), 27 Nov 2026. Read only: live storefront in an isolated
Orca tab (theme `karmicare/main` 187295564157, role main), Shopify admin and Loop admin read in Victor's
logged-in tab (no click on Save, no toggle changed), theme files at `karmicare/buybox-ab`, Loop and Shopify
docs. Helpers: `docs/buybox-ab/preview/su_fetch.py`, `su_admin.py`.

**Reading of "single units".** The products sold on their own next to the Duo: **Awake** and **Asleep**
as single tubes (€30 each), and the three **Welcome Kit accessories**, which are also on sale on their own:
Morning Toothbrush (€6), Evening Toothbrush (€6) and Whitening Charcoal Floss (€9). No product has a
single-unit *variant*: every product has one variant. The accessories differ from the tubes in one way
that matters: they are the Welcome Kit lines the buybox adds to the cart, so they must stay buyable and
readable in Liquid (section 2).

## 1. Inventory

### Products (admin, 27 Nov)

| Product | Handle | Price | Status | Stock | Collections |
|---|---|---|---|---|---|
| Awake Morning Toothpaste | `awake-morning-toothpaste-2-0` (NL `awake-ochtend-tandpasta-1`, FR `awake-dentifrice-du-matin-1`) | €30 | Active | 22 | Karmicare Collection, VGBC2025 |
| Asleep Evening Toothpaste | `asleep-evening-toothpaste-2-0` | €30 | Active | 48 | Karmicare Collection, VGBC2025 |
| Morning Toothbrush | `morning-toothbrush-2-0` | €6 | Active | 1,598 | Complete Oral Hygiene Kit, Karmicare Collection, VGBC2025 |
| Evening Toothbrush | `evening-toothbrush-2-0` | €6 | Active | 1,598 | same |
| Whitening Charcoal Floss | `whitening-charcoal-dental-floss` | €9 | Active | 1,573 | same |
| *Duo, for reference* | `karmicare-biorhythmic-oral-care-system` | €67 | Active | 369 | none |

Not reachable for visitors: two **Draft** Duo products ("Founder members €49", "Karmicare Biorhythmic Oral
Care System") and six **Archived** 1.0 products (Awake, Asleep, brushes, Duo, Complete Hygiene Kit). The
collections count 11 (Karmicare Collection, VGBC2025) and 6 (Complete Oral Hygiene Kit) products, and
show only the active ones.

### Sales channels and catalogs (admin "Manage publishing", 27 Nov)

| Channel | Awake | Asleep | Brushes (each) | Floss | Duo |
|---|---|---|---|---|---|
| Online Store | on | on | on | on | on |
| Point of Sale | on | on | on | on | on |
| Shop (Shop app) | on | on | on | on | on |
| Shopify GraphiQL App | on | on | on | on | on |
| KARMICARE: Shopify Storefront | off | on | on | on | off |
| Facebook & Instagram | on | on | on | on | on |
| Google & YouTube | on (warning: missing shipping info BG, HR, MT) | on | on | on | **off** |
| Inbox | on | on | on | on | off |
| TikTok | on | on | on | on | off |
| Karmicare Headless | off | off | off | on | on |
| Agentic (Shopify Catalog) | 1 | 1 | 1 | 1 | 1 |
| Market catalogs (Regions) | 3 | 3 | 3 | 3 | 3 |

Worth knowing on its own: on Google & YouTube and TikTok the shop offers the single tubes and the
accessories, **but not the Duo**.

### Every place a visitor can reach them

| Path | Reachable? | Evidence (live 27 Nov; theme file:line) |
|---|---|---|
| Header and footer menus | no | The home page (EN, NL) links only to the Duo; header CTA `sections/header-group.json:56` |
| Home page | no | Every product reference is the Duo: `templates/index.json:38`, `:210`, `:216`, `:220`, `:335` |
| Duo PDP | no link | The kit tiles open an info popup, no product link: `assets/loop-widget.js:2208`, `:2257` to `:2268` |
| Single PDPs, direct URL | **yes**, with a buy button at €30 | `templates/product.json:13` (main-product), `:75` (buy_buttons); no `robots` meta, canonical to itself; NL/FR handles as above. "You may also like" is off: `templates/product.json:218` to `:221` (`disabled: true`) |
| `/collections/all` | **yes**, all 6 | not linked anywhere; `templates/collection.json:13`, `:21`; loop `sections/main-collection-product-grid.liquid:160` |
| Collection pages | **yes** | `/collections/karmicare-collection`, `/collections/vgbc2025` (5 singles each), `/collections/biorhythmic-oral-hygiene-kit` (3 accessories); all three in the sitemap |
| Store search | **yes** | Header search is off (`sections/header-group.json:57`, `show_search: false`), but `/search?q=awake` lists Awake and the brushes: `templates/search.json:13`, `sections/main-search.liquid:66` |
| Predictive search | **yes** | `predictive_search_enabled: true` (`config/settings_data.json:153`); `/search/suggest.json?q=toothpaste` returns all 5 singles: `sections/predictive-search.liquid:113` |
| Sitemap | **yes**, all 5 | `sitemap_products_1.xml` in EN, NL and FR; `robots.txt` allows `/products/` |
| Public JSON | **yes** | `/products.json`, `/collections/*/products.json` |
| Supplemental feed views | **yes** for Awake and Asleep | `templates/collection.kc-feed-google.liquid` (loop from line 27) and `templates/collection.kc-feed-meta.liquid:27` to `:28` read `/collections/all`; the live NL output has rows for Asleep, Duo and Awake (products with a gallery metafield) |
| Google & YouTube (free listings, Shopping) | **yes** | channel on for all singles, off for the Duo |
| Facebook & Instagram (catalog, shop) | **yes** | on for all |
| TikTok | **yes** | on for the singles |
| Shop app | **yes** | Shop channel on for all |
| AI agents | **yes** | Agentic channel (Shopify Catalog); `/agents.md` and UCP let agents search and check out |
| Shopify Inbox | **yes** | on for the singles (product cards in chat) |
| Cart | no upsell | `/cart` redirects to checkout: `templates/cart.json:11` to `:14`, `sections/kc-cart-redirect.liquid`. No cart upsell block in the theme |
| Checkout and post-purchase | none found | Loop "Checkout upgrades" and "Post purchase offers" are not set up. The Shopify checkout editor was not read |
| Loop customer portal | **yes, by design** | Upsell active, offers all 6 (section 3) |
| Klaviyo emails | likely | Earlier finding (31 Oct, not re-checked): the abandoned-checkout feed renders the whole catalog, Unlisted included |
| Marketplaces | outside Shopify | Farmaline and bol are not Shopify sales channels in this store. Their listings are managed in their own portals and do not follow Shopify status or channels |
| Other sites | **yes** | A web search (27 Nov) shows the single 32 ml tubes and the Duo at nutritionalwholesaler.com, and an old Big Cartel store with the kit (`karmicare.bigcartel.com`) |
| Amazon MCF | no listing | Fulfilment app only (tag `MCF`, inventory location "Amazon MCF") |

## 2. Why they stay available

- **Status Active and published to the Online Store.** This alone opens the PDP, `/collections/all`, the
  store and predictive search, the sitemap and the public JSON.
- **Collection membership.** Karmicare Collection, VGBC2025 and the Complete Oral Hygiene Kit hold them,
  and each collection has its own page in the sitemap.
- **No `seo.hidden` metafield.** The single PDPs carry no `noindex`.
- **Channel publication.** Google & YouTube, Facebook & Instagram, TikTok, Shop, Inbox and Agentic are on,
  so the feeds, the Shop app and AI agents carry them.
- **A full product template.** `templates/product.json` gives every single its own buybox.
- **Loop needs part of this.** Its upsell takes a product only if it "is available to sell on your online
  store" (section 3). Whatever hides them has to keep the Online Store publication.
- **The kit needs the accessories.** The Welcome Kit lines are these products. The theme reads them through
  `product_list` settings: `settings.welcome_kit_free_product` (`config/settings_data.json:176` to `:180`,
  read in `snippets/kc-plan-config.liquid:39`, `snippets/buy-buttons.liquid:88`,
  `snippets/sticky-cart-block.liquid:23`) and the Loop block's `welcome_kit_products`
  (`sections/main-product.liquid:2946`; values in `templates/product.subscription-item.json:84` to `:86`,
  `templates/index.json:757` to `:759`, `templates/article.json:63` to `:65`). The add goes through
  `/cart/add.js`.

## 3. What Loop needs for the upsell

**What runs today** (Loop admin, read 27 Nov):

- **Grow > Upsells (customer portal)** is Active, with both customer permissions on: "add a one-time purchase
  to their upcoming subscription order" and "add item(s) in their existing subscription".
  - **General profile**, "only recommended items": Asleep, Duo, Awake, Evening Toothbrush, Morning Toothbrush,
    Floss; nothing excluded; 33 views in 30 days, 3.03 % added, 0 sold.
  - **Personalized profile "prepaid"** (condition: prepaid subscription), Active, the same six; 4 views, 0 sold.
- **Selling plans for the recurring add-on.** "only for upsell items 60 day plan" (every 60 days) and "only
  for upsell items yearly plan" (every 6 months) are available in the customer portal and admin portal only,
  not on the storefront. They are attached to Awake (its admin page) so that a single can join a subscription
  at the contract's frequency.
- **Not set up:** Cart (beta, storefront), Checkout upgrades, Post purchase offers, Upgrades, Volume discounts.
- **No sales channel of its own.** Loop has none in the publishing list. It relies on the product being on
  the Online Store.

**Loop's conditions for a product to show as an upsell**
([Upsell and cross-sell](https://help.loopwork.co/en/articles/12703297-upsell-and-cross-sell)):

- "The product is available to sell on your online store."
- If inventory is tracked and selling out of stock is off, stock above 0.
- Not on the excluded list.
- "The product's selling frequency matches the subscription's contract frequency."

**Unlisted products in Loop**
([Settings FAQs](https://help.loopwork.co/en/articles/12858166-settings-faqs),
[Customer portal FAQs](https://help.loopwork.co/en/articles/12858156-customer-portal-faqs)):

- Staff can add, swap and remove Unlisted products in the admin portal, Bulk actions and Flows.
- "Unlisted products remain restricted from customer-facing touchpoints and will not appear in areas such
  as swap recommendations or other customer product discovery surfaces."
- "To make the product available on the portal, you'll need to relist the item on Shopify again."
- Unlisted products raise no "inactive product" alert, so subscriptions that hold them keep working.
- A search summary mentioned a portal setting "Show unlisted products". No Loop page I could open confirms
  it, and it is not in Loop's Settings overview. **Ask Loop support before relying on Unlisted.**

### Test: Awake set to Unlisted (Victor, 27 Nov evening)

Victor asked for it: "put Awake to unlisted and see if it's available in Loop portal". Awake was **Unlisted
from 20:52 to 21:10 UTC** (Shopify admin, status only), then set back to Active.

- **Loop portal.** I checked one active 60-Day subscription's portal, opened with "Access customer portal"
  in the Loop admin (Victor's own subscriptions are cancelled or paused, and those show no add-ons).
  - Awake stayed offered in "Goes well with your next order" and in "See more products", with its ADD /
    SELECT button. That held from the first check to 17 minutes after the change (11 reloads,
    `preview/unlisted_portal_watch.py`).
  - Only the list was read. No ADD was clicked, so whether adding an Unlisted product goes through is
    **not** tested. Nothing about the customer was recorded.
- **Store, about 2 minutes after the change.**
  - Gone: `/collections/all`, the Karmicare Collection, `/products.json` and the sitemap.
  - The PDP carried `noindex,nofollow` and still sold by direct URL (3 buy forms).
  - The predictive search still suggested it (cache).
- **After setting it back:** `/products.json` lists Awake again and the PDP has no `robots` meta.

**What this changes.** Loop's help says Unlisted products are kept out of customer-facing surfaces, but on
this store its portal upsell kept offering Awake. That makes option A workable for the single tubes.

Before relying on it, check two things:
1. That ADD works for an Unlisted product. Use a test subscription, never a customer's.
2. That the portal still offers it a day later, after Loop's own product sync.

The accessories stay Active either way (kit lines, `product_list` settings).

## 4. Options

**What each one hides:**

| Option | Visitors: PDP, collections, search | SEO | Google / Meta / TikTok feeds | Shop app, AI agents |
|---|---|---|---|---|
| **A. Shopify status "Unlisted"** | Gone from collections, search, predictive search and recommendations; the PDP still opens and still sells by direct URL | `noindex,nofollow`, out of the sitemap | "hides products from … all sales channels" (Shopify changelog) | Hidden from Shopify Catalog; Shop app "not supported" (unclear) |
| **B. Unpublish from the Online Store only** | PDP 404, gone from collections and search | Gone from the sitemap | Unchanged unless also unpublished there | Unchanged |
| **C. Keep Active and on the Online Store, hide everywhere else** | Theme redirects the PDP to the Duo and skips them in collections and search | `seo.hidden` = 1: `noindex`, out of the sitemap and the store search | Off by unpublishing those channels | Off by unpublishing Shop and Agentic |
| D. Theme only, no admin change | PDP redirect and theme filters | Sitemap and indexing stay | Unchanged | Unchanged |
| E. Draft | Gone everywhere | Gone | Gone | Gone |

**What each one breaks or keeps:**

| Option | Loop portal upsell | Kit lines (accessories) | Existing subscribers with a single | Marketplaces |
|---|---|---|---|---|
| **A** | **At risk**: Loop says Unlisted is kept out of customer-facing surfaces (section 3) | At risk: cart and checkout treat Unlisted as active, but Unlisted products "aren't selectable" in theme product settings ([community](https://community.shopify.dev/t/unlisted-products-arent-selectable-in-product-type-settings/26911)), and the kit is read through `product_list` settings | Keep working (no Loop alert) | Unaffected |
| **B** | **Breaks** ("available to sell on your online store") | **Breaks** (the cart add needs the Online Store) | Keep working | Unaffected |
| **C** | **Kept** (still active and on the Online Store) | Kept | Unchanged | Unaffected |
| D | Kept | Kept | Unchanged | Unaffected |
| E | Breaks | Breaks | Loop flags them inactive | Unaffected |

**Notes per option:**

- **A.** Still needs the theme redirect, because the direct URL keeps selling ([Skio](https://help.skio.com/docs/what-is-the-unlisted-product-status-in-shopify-and-can-i-use-it-with-skio): "Shopify does not block customers from adding unlisted products to cart from the product page"). Klaviyo still shows Unlisted products.
- **B.** Not usable for this goal.
- **C.** Needs admin steps plus a small theme change. `/products.json` still lists the products, which only bots read.
- **D.** Not enough on its own.
- **E.** Not usable for this goal.

## 5. Recommendation

**Option C for the single tubes, and the same for the accessories if Victor wants them out of sight.** It
keeps the products active and on the Online Store, which is what Loop's upsell and the Welcome Kit lines
depend on. It takes them off every other surface.

Unlisted (A) would be the one-switch version. The 27 Nov test (section 3) shows the portal upsell keeping an
Unlisted Awake, so A is open for the single tubes once ADD and the next-day check pass. Even then keep the
accessories Active (kit). The theme redirect is needed in A and C alike.

### Theme changes (this lane, later, on Victor's go)

| # | Change |
|---|---|
| T1 | `templates/product.kc-redirect.json` (or `.liquid` on `layout/kc-redirect`, as `templates/cart.json`): a product assigned to it sends the visitor to the Duo (`window.location.replace`, a plain link without JS) with `noindex`. Reversible per product by switching the template back. |
| T2 | Collection grid, search results and predictive search skip products tagged `kc-hidden` (`sections/main-collection-product-grid.liquid:160`, `sections/main-search.liquid:66`, `sections/predictive-search.liquid:113`). Covers `/collections/all`, which no admin change can empty. |
| T3 | The two feed views skip `kc-hidden` products (`templates/collection.kc-feed-google.liquid`, `templates/collection.kc-feed-meta.liquid:28`), so the supplemental rows do not point at unpublished items. |
| T4 | Optional, a product decision: every collection page redirects to the Duo (the store sells one product). The feed views are separate templates and keep working. |

T1 to T3 do nothing until a product gets the tag or the template, so they can land first.

### Admin changes (Victor)

| # | Change |
|---|---|
| A1 | Keep Awake, Asleep and the accessories **Active** and published to the **Online Store** (Loop upsell, kit lines). |
| A2 | Unpublish them from Google & YouTube, Facebook & Instagram, TikTok, Shop, Inbox and Agentic (Shopify Catalog). Point of Sale and the two headless channels are harmless; clean them up if they are unused. |
| A3 | Metafield definition `seo.hidden` (namespace `seo`, key `hidden`, integer), value 1 on each single: out of the sitemap and the store search, `noindex` ([Shopify blog](https://www.shopify.com/blog/noindex-shopify-page), [shopify.dev SEO](https://shopify.dev/docs/apps/build/marketing/optimize-storefront-seo)). |
| A4 | Take the singles out of Karmicare Collection and VGBC2025 (and the Complete Oral Hygiene Kit if the accessories go too). Check first that no Loop bundle or rule uses those collections: Loop syncs all three, but the upsell profiles list products, not collections. |
| A5 | Tag each single `kc-hidden` (after T2 and T3 are live). |
| A6 | Assign the theme template `product.kc-redirect` to each single (after T1 is live). |
| A7 | Klaviyo: keep the singles out of recommendation and catalog feeds (email lane). |
| A8 | Loop: nothing to change. After A2 to A6, check that the portal upsell preview still lists the singles. |
| A9 | Outside Shopify: decide about the reseller listings (nutritionalwholesaler.com) and the old Big Cartel store. |
| A10 | Separate decision: the Duo is off on Google & YouTube and TikTok. After A2 the shop has no toothpaste product on those channels unless the Duo goes on. |

### Open, to verify

- **Loop support:** are Unlisted products offered in customer portal upsells (one-time and subscription
  add-on), and does a "Show unlisted products" setting exist? This decides between A and C.
- **After A2:** the Shop channel off should not touch Shop Pay at checkout (it controls the Shop app
  listing). Check one test order path without payment.
- **Existing subscriptions with a single as a line:** the count needs Loop's subscription list filtered by
  product (customer data; Victor). Loop's upsell stats show 0 sold in 30 days.
- **VGBC2025:** what the collection is for, before it changes.
- **Theme spots after T1 to T3:** the lane can check them read only (sitemap, search, collections, PDP
  redirect, feeds).

Sources: [Shopify unlisted products](https://shopify.dev/docs/apps/build/product-merchandising/unlisted-products),
[Shopify changelog](https://shopify.dev/changelog/new-unlisted-product-status),
[Loop upsell and cross-sell](https://help.loopwork.co/en/articles/12703297-upsell-and-cross-sell),
[Loop settings FAQs](https://help.loopwork.co/en/articles/12858166-settings-faqs),
[Loop customer portal FAQs](https://help.loopwork.co/en/articles/12858156-customer-portal-faqs),
[Skio on Unlisted](https://help.skio.com/docs/what-is-the-unlisted-product-status-in-shopify-and-can-i-use-it-with-skio),
[Shopify community: Unlisted in product settings](https://community.shopify.dev/t/unlisted-products-arent-selectable-in-product-type-settings/26911),
[Shopify blog: noindex](https://www.shopify.com/blog/noindex-shopify-page).
