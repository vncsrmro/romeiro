(() => {
  const asset = name => `/assets/cases/${name}`;
  let mounting = false;
  async function mount() {
    const section = document.querySelector('#projects > div');
    if (mounting || !section || section.querySelector('.vr-case-grid')) return;
    mounting = true;
    const projects = await fetch('/cases.json').then(r => r.json());
    const grid = document.createElement('div');
    grid.className = 'vr-case-grid';
    grid.setAttribute('aria-label', 'Projetos de Vinicius Romeiro');
    grid.innerHTML = projects.map((p,i) => `
      <a class="vr-case-card" href="/cases/${p.id}/" aria-label="Abrir case ${p.name}">
        <span class="vr-case-media">
          <video muted playsinline autoplay loop preload="metadata" poster="${asset(p.image.split('/').pop())}" aria-hidden="true"><source src="${asset(p.id+'-preview.mp4')}" type="video/mp4"></video>
          <span class="vr-case-index">0${i+1} / 0${projects.length}</span>
          <span class="vr-case-open">Ver case <span aria-hidden="true">↗</span></span>
        </span>
        <span class="vr-case-meta"><span>${p.category}</span><span>InovaSys</span></span>
        <span class="vr-case-title">${p.name}<span aria-hidden="true">↗</span></span>
        <span class="vr-case-lead">${p.title}</span>
      </a>`).join('');
    section.append(grid);
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      const video = entry.target.querySelector('video');
      if (!video) return;
      if (entry.isIntersecting) video.play().catch(()=>{}); else video.pause();
    }), {rootMargin:'150px'});
    grid.querySelectorAll('.vr-case-card').forEach(card => observer.observe(card));
    mounting = false;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
  const observer = new MutationObserver(() => { if (!document.querySelector('.vr-case-grid')) mount(); });
  observer.observe(document.documentElement,{childList:true,subtree:true});
})();
