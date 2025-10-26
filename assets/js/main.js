/**
 * Script principal du portfolio FC Palestina
 */

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Portfolio FC Palestina initialisé');
    
    // Initialiser les modules
    initializeApp();
    
    // Écouter les événements de mise à jour de l'admin
    document.addEventListener('forceReloadGallery', (event) => {
        console.log('🔄 Événement de rechargement reçu, mise à jour des données...');
        loadInitialData();
    });
    
    document.addEventListener('adminDataUpdated', (event) => {
        console.log('🔄 Données admin mises à jour, synchronisation...');
        loadInitialData();
    });
});

/**
 * Initialisation de l'application
 */
async function initializeApp() {
    try {
        // Afficher le loading
        toggleLoading(true);
        
        // Initialiser les composants
        initializeNavigation();
        initializeGallery();
        initializeScrollEffects();
        initializeContactForm();
        
        // Charger les données initiales
        await loadInitialData();
        
        console.log('✅ Application initialisée avec succès');
        
    } catch (error) {
        // Journaliser en détail et afficher un message plus informatif
        console.error('❌ Erreur lors de l\'initialisation de l\'application:', error);
        handleError(error, 'App initialization');
        const msg = (error && (error.message || error.toString())) || 'Erreur inconnue';
        showNotification(`Erreur d\'initialisation: ${msg}`, 'error');
    } finally {
        toggleLoading(false);
    }
}

/**
 * Initialiser la navigation
 */
function initializeNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const header = document.querySelector('.header');

    // Toggle du menu mobile
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    // Fermer le menu mobile au clic sur un lien
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // Effet de scroll sur le header
    if (header) {
        window.addEventListener('scroll', throttle(() => {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }, 100));
    }

    // Navigation fluide
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    // Marquer le lien comme actif immédiatement
                    navLinks.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                }
            }
        });
    });

    // ScrollSpy: activer le lien correspondant à la section visible
    const sections = document.querySelectorAll('section[id]');
    if (sections.length && navLinks.length) {
        const linkById = new Map();
        navLinks.forEach(l => {
            const href = l.getAttribute('href');
            if (href && href.startsWith('#')) {
                linkById.set(href.slice(1), l);
            }
        });

        // Conserver le dernier ratio de chaque section pour éviter l'état bloqué
        const lastRatios = new Map();

        const applyActive = (sectionIdFallback = null) => {
            // Choisir la section avec le ratio le plus élevé (> 0)
            let bestId = null;
            let bestRatio = 0;
            lastRatios.forEach((ratio, id) => {
                if (ratio > bestRatio) {
                    bestRatio = ratio;
                    bestId = id;
                }
            });

            // Fallback explicite en haut de page
            if (!bestId && sectionIdFallback) {
                bestId = sectionIdFallback;
            }

            if (bestId) {
                const activeLink = linkById.get(bestId);
                if (activeLink) {
                    navLinks.forEach(l => l.classList.remove('active'));
                    activeLink.classList.add('active');
                }
            }
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(en => {
                // Stocker le dernier ratio connu (0 si non intersecté)
                lastRatios.set(en.target.id, en.isIntersecting ? en.intersectionRatio : 0);
            });

            // Quand on est tout en haut, forcer Accueil
            const atTop = (window.scrollY || window.pageYOffset) < 120;
            applyActive(atTop ? 'home' : null);
        }, {
            root: null,
            // Compenser la hauteur du header fixe pour l'activation
            rootMargin: '-96px 0px -60% 0px',
            threshold: [0, 0.25, 0.5, 0.75, 1]
        });

        sections.forEach(sec => {
            lastRatios.set(sec.id, 0);
            observer.observe(sec);
        });

        // Sécurité: mettre Accueil actif au chargement
        navLinks.forEach(l => l.classList.remove('active'));
        const homeLink = linkById.get('home');
        if (homeLink) homeLink.classList.add('active');

        // Fallback sur scroll (utile sur certains navigateurs)
        window.addEventListener('scroll', throttle(() => {
            const atTop = (window.scrollY || window.pageYOffset) < 120;
            if (atTop) {
                navLinks.forEach(l => l.classList.remove('active'));
                const hl = linkById.get('home');
                if (hl) hl.classList.add('active');
            }
        }, 150));
    }
}

/**
 * Initialiser la galerie
 */
function initializeGallery() {
    // Attendre que le DOM soit complètement chargé
    setTimeout(() => {
        try {
            // Vérifier si l'élément de la galerie existe
            const galleryGrid = document.getElementById('gallery-grid');
            if (!galleryGrid) {
                console.error('❌ Élément gallery-grid non trouvé');
                return;
            }
            
            // Initialiser la galerie
            window.gallery = new Gallery();
            console.log('📸 Galerie initialisée avec succès');
            
        } catch (error) {
            console.error('❌ Erreur initialisation galerie:', error);
        }
    }, 100);
}

/**
 * Initialiser les effets de scroll
 */
function initializeScrollEffects() {
    // Animation des éléments au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observer les sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });

    // Observer les éléments de la galerie
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        observer.observe(item);
    });
}

/**
 * Initialiser le formulaire de contact
 */
function initializeContactForm() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(contactForm);
            const data = {
                name: formData.get('name') || contactForm.querySelector('input[type="text"]').value,
                email: formData.get('email') || contactForm.querySelector('input[type="email"]').value,
                message: formData.get('message') || contactForm.querySelector('textarea').value
            };

            // Validation
            if (!data.name || !data.email || !data.message) {
                showNotification('Veuillez remplir tous les champs', 'warning');
                return;
            }

            if (!isValidEmail(data.email)) {
                showNotification('Veuillez entrer une adresse email valide', 'warning');
                return;
            }

            try {
                // Simuler l'envoi du formulaire
                await submitContactForm(data);
                showNotification('Message envoyé avec succès !', 'success');
                contactForm.reset();
            } catch (error) {
                handleError(error, 'Contact form submission');
                showNotification('Erreur lors de l\'envoi du message', 'error');
            }
        });
    }
}

/**
 * Charger les données initiales
 */
async function loadInitialData() {
    try {
        console.log('🔄 Chargement des données initiales...');
        
        // Charger les catégories directement depuis le fichier JSON avec cache-busting
        const ts = Date.now();
        const categoriesResponse = await fetch(`/data/categories.json?t=${ts}`, { cache: 'no-store' });
        if (categoriesResponse.ok && categoriesResponse.headers.get('content-type')?.includes('application/json')) {
            const categories = await categoriesResponse.json();
            updateCategoryFilters(categories);
            console.log('📂 Catégories chargées:', categories.length);
        } else {
            console.warn('⚠️ Impossible de charger categories.json');
        }
        
        // Charger les statistiques
        const stats = await loadStats();
        updateStats(stats);
        
        console.log('✅ Données initiales chargées');
        
    } catch (error) {
        console.warn('Impossible de charger les données initiales:', error);
    }
}

/**
 * Mettre à jour les filtres de catégories
 * @param {Array} categories - Liste des catégories
 */
function updateCategoryFilters(categories) {
    const filterContainer = document.querySelector('.gallery-filters');
    if (!filterContainer) return;

    // Supprimer les boutons existants (sauf "Tous")
    const existingButtons = filterContainer.querySelectorAll('.filter-btn:not([data-filter="all"])');
    existingButtons.forEach(btn => btn.remove());

    // Déterminer la catégorie active actuelle (si la galerie est initialisée)
    const currentCat = (window.gallery && window.gallery.currentCategory) ? window.gallery.currentCategory : 'all';

    // Ajouter les nouvelles catégories
    categories.forEach(category => {
        console.log('🎨 Catégorie:', category.name, 'Couleur:', category.color);
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.dataset.filter = category.id;
        button.textContent = category.name;
        
        // Appliquer la couleur de la catégorie
        if (category.color) {
            button.style.backgroundColor = category.color;
            button.style.borderColor = category.color;
            button.style.color = 'white';
            // Hover et active state
            button.addEventListener('mouseenter', () => {
                if (!button.classList.contains('active')) {
                    button.style.opacity = '0.8';
                }
            });
            button.addEventListener('mouseleave', () => {
                if (!button.classList.contains('active')) {
                    button.style.opacity = '1';
                }
            });
            console.log('✅ Couleur appliquée:', category.color);
        } else {
            console.log('❌ Pas de couleur pour:', category.name);
        }
        
        // L'état actif sera géré par la délégation d'événements dans Gallery
        
        filterContainer.appendChild(button);
    });
    
    // Appliquer l'état actif visuel cohérent
    const allButtons = filterContainer.querySelectorAll('.filter-btn');
    allButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.filter === currentCat));
    if (![...allButtons].some(b => b.classList.contains('active'))) {
        const allBtn = filterContainer.querySelector('.filter-btn[data-filter="all"]');
        if (allBtn) allBtn.classList.add('active');
    }
    
    console.log(`🔄 ${categories.length} catégories ajoutées aux filtres`);
}

/**
 * Charger les statistiques
 * @returns {Object} - Statistiques
 */
async function loadStats() {
    try {
        const jerseys = await jerseyAPI.getJerseys({ limit: 1000 });
        return {
            totalJerseys: jerseys.jerseys.length,
            categories: jerseys.jerseys.reduce((acc, jersey) => {
                acc[jersey.category] = (acc[jersey.category] || 0) + 1;
                return acc;
            }, {}),
            totalViews: jerseys.jerseys.reduce((sum, jersey) => sum + (jersey.views || 0), 0)
        };
    } catch (error) {
        return {
            totalJerseys: 0,
            categories: {},
            totalViews: 0
        };
    }
}

/**
 * Mettre à jour les statistiques
 * @param {Object} stats - Statistiques
 */
function updateStats(stats) {
    // Mettre à jour les statistiques dans la section About
    const statElements = document.querySelectorAll('.stat-number');
    if (statElements.length >= 3) {
        statElements[0].textContent = `${stats.totalJerseys}+`;
        statElements[1].textContent = '100%';
        statElements[2].textContent = '24/7';
    }
}

/**
 * Soumettre le formulaire de contact
 * @param {Object} data - Données du formulaire
 */
async function submitContactForm(data) {
    // Simuler l'envoi du formulaire
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simuler un succès
            console.log('Formulaire envoyé:', data);
            resolve();
        }, 1000);
    });
}

/**
 * Synchroniser avec Yupoo
 */
async function syncWithYupoo() {
    try {
        showNotification('Synchronisation avec Yupoo en cours...', 'info');
        const success = await jerseyAPI.syncWithYupoo();
        
        if (success) {
            // Recharger la galerie
            const gallery = window.gallery;
            if (gallery) {
                gallery.refresh();
            }
        }
    } catch (error) {
        handleError(error, 'Yupoo sync');
    }
}

/**
 * Gestion des erreurs globales
 */
window.addEventListener('error', (e) => {
    handleError(e.error, 'Global error');
});

window.addEventListener('unhandledrejection', (e) => {
    handleError(e.reason, 'Unhandled promise rejection');
});

/**
 * Gestion de la visibilité de la page
 */
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page cachée - économiser les ressources
        console.log('Page cachée');
    } else {
        // Page visible - reprendre les activités
        console.log('Page visible');
    }
});

/**
 * Gestion du redimensionnement de la fenêtre
 */
window.addEventListener('resize', debounce(() => {
    // Recalculer les dimensions si nécessaire
    console.log('Fenêtre redimensionnée');
}, 250));

/**
 * Gestion du scroll
 */
window.addEventListener('scroll', throttle(() => {
    // Mettre à jour la position de scroll si nécessaire
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    document.documentElement.style.setProperty('--scroll-top', `${scrollTop}px`);
}, 16));

/**
 * Initialiser les raccourcis clavier
 */
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K pour la recherche
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Échap pour fermer les modals
    if (e.key === 'Escape') {
        const modal = document.getElementById('image-modal');
        if (modal && modal.classList.contains('active')) {
            const closeBtn = modal.querySelector('.modal-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }
    }
});

/**
 * Exposer les fonctions globales
 */
window.syncWithYupoo = syncWithYupoo;
window.jerseyAPI = jerseyAPI;
window.jerseyModal = jerseyModal;

// ===== PERFORMANCE MONITORING =====
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('📊 Performance:', {
                loadTime: Math.round(perfData.loadEventEnd - perfData.loadEventStart),
                domContentLoaded: Math.round(perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart),
                firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
                firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
            });
        }, 0);
    });
}

console.log('🎯 Portfolio FC Palestina prêt !');
