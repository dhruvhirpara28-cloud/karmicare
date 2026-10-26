location.protocol !== 'https:' ? 'BLANK' : (async () => {
  const text = async (u) => (await fetch(u)).text();
  const P = new DOMParser();
  const out = { fetched: new Date().toISOString(), shell: {}, index: [], articles: {}, product: null };

  // Page shells (header, footer, head) for the fixture
  for (const [k, u] of [['article', '/blogs/news/nano-hydroxyapatite'], ['blog', '/blogs/news']]) {
    out.shell[k] = await text(u);
  }

  // Index cards in blog order: handle and excerpt (article.excerpt as the card prints it)
  for (const u of ['/blogs/news', '/blogs/news?page=2']) {
    const d = P.parseFromString(await text(u), 'text/html');
    Array.from(d.querySelectorAll('.blog-articles__article')).forEach((c) => {
      const a = c.querySelector('a[href*="/blogs/news/"]');
      const ex = c.querySelector('.article-card__excerpt');
      out.index.push({
        handle: a ? a.getAttribute('href').split('/').pop().split('?')[0] : null,
        excerpt: ex ? ex.textContent.trim() : '',
      });
    });
  }

  // Each article: title, date, featured image, body
  for (const item of out.index) {
    const d = P.parseFromString(await text('/blogs/news/' + item.handle), 'text/html');
    const hero = d.querySelector('.article-template__hero-container img');
    const body = d.querySelector('.article-template__content');
    const time = d.querySelector('.article-template__title ~ * time, header time, time');
    out.articles[item.handle] = {
      title: (d.querySelector('.article-template__title') || {}).textContent.trim(),
      published_at: time ? time.getAttribute('datetime') : null,
      image: hero ? {
        src: hero.getAttribute('src'),
        width: +hero.getAttribute('width'),
        height: +hero.getAttribute('height'),
        alt: hero.getAttribute('alt') || '',
      } : null,
      content: body ? body.innerHTML : '',
    };
  }

  // The Duo, for the end-of-article CTA
  const pr = await fetch('/products/karmicare-biorhythmic-oral-care-system.js');
  if (pr.ok) {
    const p = await pr.json();
    out.product = { title: p.title, handle: p.handle, url: '/products/' + p.handle, featured_image: p.featured_image, images: p.images.slice(0, 6) };
  }
  return JSON.stringify(out);
})()
