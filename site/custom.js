(() => {
  const substitutions = [
    [/Rohit Anand/g, 'Vinicius Romeiro'],
    [/Rohit/g, 'Vinicius'],
    [/Anand/g, 'Romeiro'],
    [/Desenvolvedor Full-Stack, Orquestrador de IA & Product Designer|Brand & Product Designer/g, 'Full-Stack, IA & Product Designer'],
    [/With a decade of experience, I'm a Brand desiner turned UI designer with a strong background in design psychology having expertise mainly in SaaS and B2B brands\./g, 'A intersecção entre design de excelência e engenharia de software moderna. Construo plataformas escaláveis do zero, unindo interfaces impecáveis e arquiteturas orientadas por IA.'],
    [/I turn ideas into meaningful products|Do primeiro pixel ao último deploy|Produtos digitais pensados por inteiro\./g, 'Design apurado. Código à altura.'],
    [/Do primeiro pixel ao deploy, meu foco é entregar/g, 'Meu foco é criar'],
    [/Book Meeting/g, 'Vamos conversar'],
    [/Design that sparks engagement and inspires action/g, 'Design de excelência. Engenharia moderna.'],
    [/Learning through every path/g, 'Aprendizado em cada projeto'],
    [/My 11 years journey/g, 'Minha jornada criativa'],
    [/Reach me out here:/g, 'Vamos construir algo juntos:'],
    [/Contact Now/g, 'Design. Engenharia. IA.'],
    [/View Project Website|View Project Site/g, 'Ver site do projeto'],
  ];
  const labels = new Map([
    ['Home','Início'], ['Work','Projetos'], ['Skills','Especialidades'], ['Gallery','Galeria'],
    ['Experience','Experiência'], ['About','Sobre'], ['Contact','Contato'], ['Projects','Projetos'],
    ['FAQs','Dúvidas'], ['What Clients Say','O que dizem os clientes'],
    ['Websites','Sites'], ['Years In Design','Anos em design'], ['Websites Done','Sites entregues'],
    ['Design Awards','Prêmios de design'], ['2015-Present','2015–hoje'],
    ['Product Design & UI/UX','Design de produto e UI/UX'],
    ['Full-Stack & Mobile','Desenvolvimento Full-Stack e Mobile'],
    ['Brand Design','Design de marca'], ['UI Design','Design de interface'],
    ['Product Design','Design de produto'], ['Freelance','Autônomo'],
    ['Sites','Pesquisa e UX'], ['Páginas de conversão','Design systems'],
    ['Portfólios e sites pessoais','Interfaces corporativas'],
    ['Interfaces responsivas','Next.js e React'], ['Animações e interações','React Native e Expo'],
    ['CMS e SEO','TypeScript e Supabase'], ['Design de logotipos','Agentes autônomos'],
    ['Cores e tipografia','Function Calling'], ['Linguagem visual','APIs de LLMs'],
    ['Year','Ano'], ['Client','Cliente'], ['Service','Serviço'], ['Website','Site'],
    ['View Project','Ver o'],
    ['Problem','Desafio'], ['Solution','Solução'], ['Responsibilities','Responsabilidades'],
    ['Key Features','Recursos principais'], ['Design Approach','Direção de design'],
    ['Technology Stack','Tecnologias'], ['Tech Stack','Tecnologias'],
    ['Outcome','Resultado'], ['Highlights','Destaques'],
    ['Name','Nome'], ['Email','E-mail'], ['Message','Mensagem'], ['Budget','Orçamento'],
    ['Select…','Selecione…'], ['Submit','Enviar'],
    ['Copy component','Copiar'], ['Copied','Copiado'],
    ['Follow','Siga'], ['me',''], ['here','aqui'],
  ]);
  let busy = false;
  function update() {
    if (busy) return;
    busy = true;
    try {
      if (document.title !== 'Vinicius Romeiro — Portfolio') document.title = 'Vinicius Romeiro — Portfolio';
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (const node of nodes) {
        let text = node.nodeValue;
        for (const [find, to] of substitutions) text = text.replace(find, to);
        const trimmed = text.trim();
        if (labels.has(trimmed)) {
          const translated = trimmed === 'Full-Stack & Mobile' && location.pathname !== '/' ? 'Desenvolvimento Framer' : labels.get(trimmed);
          text = text.replace(trimmed, translated);
        }
        if (text !== node.nodeValue) node.nodeValue = text;
      }
      for (const element of document.querySelectorAll('[aria-label],[placeholder],[title]')) {
        for (const attribute of ['aria-label','placeholder','title']) {
          const value = element.getAttribute(attribute);
          if (value && labels.has(value)) element.setAttribute(attribute, labels.get(value));
        }
      }
      if (location.pathname === '/') {
        const about = document.querySelector('#about');
        if (about) {
          const aboutWalker = document.createTreeWalker(about, NodeFilter.SHOW_TEXT);
          const aboutLabels = new Map([['Framer','Next.js'], ['Designer','Cofundador'], ['Autônomo','InovaSys & MSH'], ['2015–hoje','10+ anos de design']]);
          while (aboutWalker.nextNode()) {
            const node = aboutWalker.currentNode;
            const value = node.nodeValue.trim();
            if (aboutLabels.has(value)) node.nodeValue = node.nodeValue.replace(value, aboutLabels.get(value));
          }
        }
      }
      for (const img of document.images) {
        if (img.src.includes('1Go0aoemW4bbp7qzvSvMvOm4tA')) { img.srcset = ''; img.src = '/assets/vinicius-hero.png'; }
        if (img.src.includes('JeThM72vsACAWs91NJsLDZCjPE')) { img.srcset = ''; img.src = '/assets/vinicius-about.png'; }
        if (img.src.includes('5eTbrewZ7DPzNMNSWuxzv5VXhY') && !img.parentElement.querySelector('.vinicius-signature')) {
          img.draggable = false;
          const signature = document.createElement('span'); signature.className = 'vinicius-signature'; signature.textContent = 'Vinicius Romeiro'; img.parentElement.style.position = 'relative'; img.parentElement.append(signature);
        }
      }
      const faq = document.getElementById('contact');
      if (faq && !faq.classList.contains('romeiro-contact')) faq.id = 'faq';
      const originalGallery = document.querySelector('#gallery:not(.romeiro-gallery)');
      if (originalGallery) originalGallery.id = 'gallery-template';
      const galleryContinuation = document.getElementById('gallery-1');
      if (galleryContinuation) galleryContinuation.id = 'gallery-template-2';
      if (originalGallery && !document.querySelector('.romeiro-gallery')) {
        const gallery = document.createElement('section');
        gallery.id = 'gallery';
        gallery.className = 'romeiro-gallery';
        gallery.innerHTML = '<div class="romeiro-gallery-head"><span>PROJETOS EM DETALHE</span><h2>O trabalho fala<br>em imagens.</h2><p>Marcas, interfaces e produtos construídos com o mesmo cuidado.</p></div><div class="romeiro-gallery-grid"><a href="/cases/paperx/"><img loading="lazy" src="/assets/cases/paperx-app.webp" alt="Interface do PaperX"><span>01 / PAPERX</span></a><a href="/cases/stival/"><img loading="lazy" src="/assets/cases/stival-brand.webp" alt="Identidade Stival"><span>02 / STIVAL</span></a><a href="/cases/recebidos/"><img loading="lazy" src="/assets/cases/recebidos-aplicacoes.webp" alt="Aplicações da marca Recebidos do Bem"><span>03 / RECEBIDOS DO BEM</span></a><a href="/cases/tidle/"><img loading="lazy" src="/assets/cases/tidle.webp" alt="Universo visual TIDLE"><span>04 / TIDLE</span></a></div>';
        originalGallery.before(gallery);
      }
      const originalContact = document.querySelector('.framer-1v25gyv-container');
      if (originalContact && !document.querySelector('.romeiro-contact')) {
        const contact = document.createElement('section');
        contact.id = 'contact';
        contact.className = 'romeiro-contact';
        contact.innerHTML = '<div class="romeiro-contact-inner"><span class="romeiro-contact-kicker">VAMOS CONVERSAR</span><h2>Design apurado.<br>Engenharia à altura.</h2><p>Do conceito ao produto digital, combino direção visual, desenvolvimento e inteligência artificial para criar experiências que fazem sentido para o negócio e para as pessoas.</p><a href="https://wa.me/5519960003434?text=Ol%C3%A1%21%20Conheci%20o%20portf%C3%B3lio%20do%20Vinicius%20Romeiro%20e%20gostaria%20de%20conversar%20sobre%20um%20projeto." target="_blank" rel="noopener noreferrer">Conversar pelo WhatsApp da InovaSys <span>↗</span></a></div>';
        originalContact.before(contact);
      }
      for (const link of document.querySelectorAll('a[href]')) {
        try {
          const href = new URL(link.href);
          if (href.protocol === 'tel:' || href.protocol === 'mailto:') {
            link.removeAttribute('href');
          } else if (href.protocol.startsWith('http') && href.origin !== location.origin && !href.hostname.endsWith('wa.me')) {
            link.href = '#contact'; link.removeAttribute('target');
          }
          if (/Get this template|Download Resume/i.test(link.textContent || '')) link.parentElement.style.display = 'none';
        } catch {}
      }
      for (const form of document.forms) {
        if (!form.dataset.viniciusDisabled) {
          form.dataset.viniciusDisabled = 'true';
          form.addEventListener('submit', e => { e.preventDefault(); e.stopImmediatePropagation(); alert('O contato será ativado quando Vinicius definir o e-mail profissional.'); }, true);
        }
      }
      const copyButton = document.getElementById('Of30EWZRx');
      if (copyButton && !copyButton.dataset.viniciusDisabled) {
        copyButton.dataset.viniciusDisabled = 'true';
        copyButton.addEventListener('click', e => { e.preventDefault(); e.stopImmediatePropagation(); alert('Este contato ainda é do template. O contato profissional de Vinicius será incluído antes da publicação.'); }, true);
      }
    } finally { busy = false; }
  }
  update();
  const observer = new MutationObserver(() => { if (!busy) requestAnimationFrame(update); });
  observer.observe(document.documentElement, { subtree: true, childList: true, characterData: true });
})();
