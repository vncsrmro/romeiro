const id=location.pathname.split('/').filter(Boolean).at(-1);
const asset=name=>`/assets/cases/${name}`;
const escapeHTML=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const projects=await fetch('/cases.json').then(r=>r.json());
const mediaData=await fetch('/case-media.json').then(r=>r.json());
const index=projects.findIndex(p=>p.id===id);
if(index<0){document.body.innerHTML='<main class="case-shell"><h1>Case não encontrado.</h1><a href="/#projects">Voltar aos projetos ↗</a></main>';}else{
  const p=projects[index];const next=projects[(index+1)%projects.length];
  const media=mediaData[p.id]||{};
  document.title=`${p.name} — Case | Vinicius Romeiro`;
  document.querySelector('meta[name="description"]').content=p.lead;
  const parts=p.category.split(' · ');
  const gallery=[p.image.split('/').pop(),...p.gallery.map(x=>x[0])];
  const captions=[p.caption,...p.gallery.map(x=>x[1])];
  const brandSection=media.brand?.length?`<section class="case-section case-reveal"><span class="case-kicker">03 / Identidade</span><div class="case-section-head" style="margin-top:26px"><h2>${escapeHTML(media.brandTitle)}</h2><p class="case-lead">${escapeHTML(media.brandIntro)}</p></div><div class="case-gallery case-brand-gallery">${media.brand.map(([file,caption])=>`<figure class="case-image"><button class="case-media-button" type="button" data-image="${asset(file)}" data-caption="${escapeHTML(caption)}" aria-label="Ampliar: ${escapeHTML(caption)}"><img loading="lazy" src="${asset(file)}" alt="${escapeHTML(caption)}"><span>Ampliar ↗</span></button><figcaption>${escapeHTML(caption)}</figcaption></figure>`).join('')}</div></section>`:'';
  const extraSection=media.extra?.length?`<section class="case-section case-reveal"><span class="case-kicker">${media.brand?.length?'04':'03'} / Exploração</span><div class="case-section-head" style="margin-top:26px"><h2>${escapeHTML(media.extraTitle)}</h2><p class="case-lead">${escapeHTML(media.extraIntro)}</p></div>${media.worldVideo?`<div class="case-world-video"><video autoplay muted loop playsinline poster="${asset('brand/tidle-cinematic.png')}"><source src="${asset(media.worldVideo)}" type="video/webm"></video></div>`:''}<div class="case-gallery">${media.extra.map(([file,caption])=>`<figure class="case-image"><button class="case-media-button" type="button" data-image="${asset(file)}" data-caption="${escapeHTML(caption)}" aria-label="Ampliar: ${escapeHTML(caption)}"><img loading="lazy" src="${asset(file)}" alt="${escapeHTML(caption)}"><span>Ampliar ↗</span></button><figcaption>${escapeHTML(caption)}</figcaption></figure>`).join('')}</div></section>`:'';
  const visualNumber=media.brand?.length?(media.extra?.length?'05':'04'):(media.extra?.length?'04':'03');
  document.body.innerHTML=`<div class="case-shell">
    <nav class="case-nav" aria-label="Navegação"><a class="case-brand" href="/">VINICIUS<b>.</b>ROMEIRO</a><div class="case-nav-actions"><a class="case-back" href="/#projects">← Todos os projetos</a><a class="case-pill" href="/#contact">Vamos conversar ↗</a></div></nav>
    <main>
      <header class="case-hero"><div class="case-eyebrow">Case 0${index+1} / 0${projects.length} · ${escapeHTML(parts[0])}</div><h1 class="${p.name.length>14?'long':''}">${escapeHTML(p.name)}</h1><p class="case-subtitle">${escapeHTML(p.title)}</p><div class="case-reel"><video autoplay muted loop playsinline poster="${asset(gallery[0])}"><source src="${asset(p.id+'-preview.mp4')}" type="video/mp4"></video></div><div class="case-facts"><div><span>Projeto</span><strong>${escapeHTML(p.name)}</strong></div><div><span>Entregas</span><strong>${escapeHTML(p.category.replaceAll(' · ',' / '))}</strong></div><div><span>Papel</span><strong>Design, produto e execução digital</strong></div></div></header>
      <section class="case-section case-section-head case-reveal"><span class="case-kicker">01 / O projeto</span><div><h2>Uma ideia com<br>forma e função.</h2><p class="case-lead">${escapeHTML(p.lead)}</p></div></section>
      <section class="case-section case-reveal"><span class="case-kicker">02 / Da estratégia à entrega</span><h2 style="margin-top:26px">O que construímos.</h2><div class="case-feature-grid">${p.features.map(([title,body],i)=>`<article class="case-feature"><span class="case-feature-number">0${i+1} / 0${p.features.length}</span><h3>${escapeHTML(title)}</h3><p>${escapeHTML(body)}</p></article>`).join('')}</div></section>
      ${brandSection}${extraSection}
      <section class="case-section case-reveal"><span class="case-kicker">${visualNumber} / Produto digital</span><h2 style="margin-top:26px">O projeto em cena.</h2><div class="case-gallery">${gallery.map((file,i)=>`<figure class="case-image"><button class="case-media-button" type="button" data-image="${asset(file)}" data-caption="${escapeHTML(captions[i]||p.name)}" aria-label="Ampliar: ${escapeHTML(captions[i]||p.name)}"><img loading="lazy" src="${asset(file)}" alt="${escapeHTML(captions[i]||p.name)}"><span>Ampliar ↗</span></button><figcaption>${escapeHTML(captions[i]||p.name)}</figcaption></figure>`).join('')}</div></section>
      <section class="case-cta case-reveal"><span class="case-kicker">Próximo passo</span><h2>Vamos criar o<br>próximo case?</h2><div class="case-cta-links"><a class="case-button" href="/#contact">Falar com Vinicius <span>↗</span></a>${p.website?`<a class="case-button secondary" href="${escapeHTML(p.website)}" target="_blank" rel="noopener noreferrer">Visitar o projeto <span>↗</span></a>`:''}<a class="case-button secondary" href="/cases/${next.id}/">Próximo: ${escapeHTML(next.name)} <span>↗</span></a></div></section>
    </main><footer class="case-footer"><span>© Vinicius Romeiro</span><a href="/#projects">Ver todos os projetos ↑</a></footer>
  </div><dialog class="case-lightbox" aria-label="Imagem ampliada"><button class="case-lightbox-close" type="button" aria-label="Fechar imagem">Fechar ×</button><img alt=""><p></p></dialog>`;
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');observer.unobserve(e.target)}}),{threshold:.1});
  document.querySelectorAll('.case-reveal').forEach(el=>observer.observe(el));
  const lightbox=document.querySelector('.case-lightbox');
  document.querySelectorAll('.case-media-button').forEach(button=>button.addEventListener('click',()=>{lightbox.querySelector('img').src=button.dataset.image;lightbox.querySelector('img').alt=button.dataset.caption;lightbox.querySelector('p').textContent=button.dataset.caption;lightbox.showModal()}));
  lightbox.querySelector('button').addEventListener('click',()=>lightbox.close());
  lightbox.addEventListener('click',event=>{if(event.target===lightbox)lightbox.close()});
}
