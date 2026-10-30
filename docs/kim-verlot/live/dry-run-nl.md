# Live dry run · NL

Read only: nothing was written. Store karmicares.myshopify.com, API 2026-10, 2026-10-30 13:08 CET.
Theme: supplied ID 187295564157, published per read: themes(roles: MAIN).
NL and FR are published: an approved write is live at once.

| Item result | Items |
|---|---:|
| missing | 2 |

**Mutations in this approval:** 0 register, 0 remove (1 removals proposed, not approved: rerun with --remove-never). **Checksum `d02fb55588863a85`.**

To write exactly this (an operator attestation must carry the date of the write):

```sh
python3 docs/localization/registration/register.py --lang nl --theme-id 187295564157 --theme-attested '2026-10-30 Codex verified Shopify CLI live karmicare/main' --write --approve d02fb55588863a85
```

## Mutations (0)

## Proposed removals, not in this approval (1)

| Resource | Key | EN | Current |
|---|---|---|---|
| `gid://shopify/Metaobject/515475276157` | `handle_item` | The Karmicare Year | Het Karmicare-jaar |

## Not written: stale, missing, ambiguous, conflict or unproven (2)

| Item | Result | Resource · key | EN | Why |
|---|---|---|---|---|
| `index:trusted_professionals_HAqYth/card_qAPajg/hover_text` | missing | — · — | &lt;p>“Supporting my biorhythm is important to me. Brushing my teeth with Karmicare fits into my daily ritual to help my nervous system transition between day and night. I also find that it helps me enormously to keep my receding gums under control.”&lt;/p> | no live key with this identity (hints trusted_professionals_HAqYth, card_qAPajg, hover_text) |
| `product.subscription-item:trusted_professionals_HAqYth/card_qAPajg/hover_text` | missing | — · — | &lt;p>“Supporting my biorhythm is important to me. Brushing my teeth with Karmicare fits into my daily ritual to help my nervous system transition between day and night. I also find that it helps me enormously to keep my receding gums under control.”&lt;/p> | no live key with this identity (hints trusted_professionals_HAqYth, card_qAPajg, hover_text) |

## API contract seen in this run

For the review of key formats and ownership (R18b): samples only, no translations.

- Token scopes: read_metaobjects, read_products, read_themes, write_translations

| Type | Resources | Sample GIDs | Sample keys | Invalid content entries |
|---|---:|---|---|---:|
| METAOBJECT | 185 | `gid://shopify/Metaobject/56564220086`, `gid://shopify/Metaobject/56564252854`, `gid://shopify/Metaobject/398314340733` | `title`, `description`, `image`, `author_firstname`, `author_country` | 0 |
| ONLINE_STORE_THEME_JSON_TEMPLATE | 10 | `gid://shopify/OnlineStoreThemeJsonTemplate/article?theme_id=187295564157`, `gid://shopify/OnlineStoreThemeJsonTemplate/index?theme_id=187295564157`, `gid://shopify/OnlineStoreThemeJsonTemplate/list-collections?theme_id=187295564157` | `section.article.json.main.share.share_label:3syj88j5f6ixv`, `section.article.json.featured_product_kc_blog.kc_hero_am_still:1i5mggacrx6lh`, `section.article.json.featured_product_kc_blog.kc_hero_pm_still:1i5t8vpaa15uc`, `section.article.json.featured_product_kc_blog.title_4znD88.custom_title:1s0r97stdhszw`, `section.article.json.featured_product_kc_blog.loop_subscriptions_7dde8c.pricing_summary_care_credit_title:2aspqcms6oale` | 0 |
| ONLINE_STORE_THEME_SECTION_GROUP | 3 | `gid://shopify/OnlineStoreThemeSectionGroup/footer-group?theme_id=187295564157`, `gid://shopify/OnlineStoreThemeSectionGroup/header-group?theme_id=187295564157`, `gid://shopify/OnlineStoreThemeSectionGroup/practitioner-group?theme_id=187295564157` | `section.sections/footer-group.json.footer.logo_svg:151dyqkcwqq2r`, `section.sections/footer-group.json.footer.slogan:225zqlvjzqd71`, `section.sections/footer-group.json.footer.copyright_text:2tjp2nkt2fjbm`, `section.sections/footer-group.json.footer.newsletter_heading:3mws8faawdff7`, `section.sections/footer-group.json.footer.klaviyo_public_key:2t5n3vt25hgzw` | 0 |
| (by ID) | 0 |  |  | 0 |

