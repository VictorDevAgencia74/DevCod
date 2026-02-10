document.addEventListener('DOMContentLoaded', function() {
    console.log('Fuosteck Portfolio Loaded');

    // Smooth Scroll e Active Link Logic
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    // Função para atualizar o link ativo
    function updateActiveLink() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            // Ajuste de offset para o header fixo (76px)
            if (window.scrollY >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            // Verifica se o href contém o ID da seção atual
            // Ex: href="/#sobre" contém "sobre"
            if (link.getAttribute('href').includes('#' + current)) {
                link.classList.add('active');
            }
        });
    }

    // Evento de Scroll para atualizar o ativo
    if (sections.length > 0) {
        window.addEventListener('scroll', updateActiveLink);
        // Chama uma vez no load para garantir
        updateActiveLink();
    }

    // Smooth Scroll para links internos (ajustado para funcionar com links absolutos que apontam para a mesma página)
    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Extrai apenas a parte do hash (#home, #sobre)
            const hash = href.split('#')[1];
            
            // Se tiver hash e o elemento existir na página atual
            if (hash) {
                const targetElement = document.getElementById(hash);
                if (targetElement) {
                    e.preventDefault();
                    
                    // Remove active de todos e adiciona no clicado imediatamente (feedback visual rápido)
                    navLinks.forEach(link => link.classList.remove('active'));
                    this.classList.add('active');

                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Atualiza a URL sem recarregar (opcional, mas bom para histórico)
                    history.pushState(null, null, '#' + hash);
                }
            }
        });
    });

    // Animação simples ao rolar (Intersection Observer)
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
});
