/**
 * Script pour forcer l'affichage des boutons de navigation
 */

console.log('🔧 Script de forçage des boutons chargé');

// Fonction pour créer les boutons de navigation
function createNavigationButtons() {
    console.log('🔧 Création des boutons de navigation...');
    
    const modal = document.getElementById('image-modal');
    if (!modal) {
        console.error('❌ Modal non trouvé');
        return;
    }
    
    // Les événements seront gérés par addButtonEvents()
    
    // Vérifier si la navigation existe déjà
    let nav = modal.querySelector('.modal-navigation');
    if (!nav) {
        console.log('🔧 Création de la navigation...');
        nav = document.createElement('div');
        nav.className = 'modal-navigation';
        nav.innerHTML = `
            <button class="modal-nav-btn" id="prev-image">
                <i class="fas fa-chevron-left"></i>
                Précédent
            </button>
            
            <span class="modal-counter">
                1 / 1
            </span>
            
            <button class="modal-nav-btn" id="next-image">
                Suivant
                <i class="fas fa-chevron-right"></i>
            </button>
        `;
        
        // Insérer la navigation après l'image mais avant les informations
        const modalContent = modal.querySelector('.modal-content');
        const modalImage = modal.querySelector('.modal-image');
        const modalInfo = modal.querySelector('.modal-info');
        
        if (modalImage && modalContent) {
            if (modalInfo) {
                // Insérer avant les informations
                modalInfo.parentNode.insertBefore(nav, modalInfo);
            } else {
                // Insérer après l'image
                modalImage.parentNode.insertBefore(nav, modalImage.nextSibling);
            }
        }
    }
    
    // Ajouter les styles CSS
    addButtonStyles();
    
    // Ajouter les événements
    addButtonEvents();
    
    console.log('✅ Boutons de navigation créés');
}

// Fonction pour ajouter les styles CSS
function addButtonStyles() {
    console.log('🎨 Ajout des styles CSS...');
    
    // Vérifier si les styles sont déjà ajoutés
    if (document.getElementById('force-button-styles')) {
        return;
    }
    
    const style = document.createElement('style');
    style.id = 'force-button-styles';
    style.textContent = `
        .modal-navigation {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 15px !important;
            background: #f8f9fa !important;
            border-top: 1px solid #e0e0e0 !important;
            gap: 15px !important;
            margin-top: 10px !important;
        }
        
        .modal-nav-btn {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            padding: 12px 20px !important;
            background: #8B1538 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
            min-width: 120px !important;
            justify-content: center !important;
        }
        
        .modal-nav-btn:hover:not(:disabled) {
            background: #5C0E26 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(139, 21, 56, 0.3) !important;
        }
        
        .modal-nav-btn:disabled {
            background: #ccc !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }
        
        .modal-nav-btn i {
            font-size: 16px !important;
        }
        
        .modal-counter {
            font-size: 16px !important;
            color: #666 !important;
            font-weight: 500 !important;
            padding: 0 20px !important;
        }
        
        .modal-thumbnails {
            display: flex !important;
            gap: 12px !important;
            padding: 20px !important;
            background: white !important;
            border-top: 1px solid #e0e0e0 !important;
            overflow-x: auto !important;
            scrollbar-width: thin !important;
            scrollbar-color: #2c5530 #f0f0f0 !important;
            min-height: 140px !important;
            align-items: center !important;
            flex-wrap: nowrap !important;
        }
        
        .modal-thumbnail {
            position: relative !important;
            flex-shrink: 0 !important;
            width: 100px !important;
            height: 100px !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            cursor: pointer !important;
            border: 3px solid transparent !important;
            transition: all 0.3s ease !important;
        }
        
        .modal-thumbnail:hover {
            border-color: #8B1538 !important;
            transform: scale(1.05) !important;
        }
        
        .modal-thumbnail.active {
            border-color: #8B1538 !important;
            box-shadow: 0 0 0 2px rgba(139, 21, 56, 0.2) !important;
        }
        
        .modal-thumbnail img {
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            display: block !important;
        }
        
        .thumbnail-overlay {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            background: rgba(0, 0, 0, 0.3) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            opacity: 0 !important;
            transition: opacity 0.3s ease !important;
        }
        
        .modal-thumbnail:hover .thumbnail-overlay {
            opacity: 1 !important;
        }
        
        .thumbnail-number {
            color: white !important;
            font-size: 12px !important;
            font-weight: bold !important;
            background: rgba(0, 0, 0, 0.7) !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
        }
        
        /* Ajustements pour les informations du maillot */
        .modal-info {
            margin-top: 15px !important;
            padding: 15px !important;
            background: white !important;
            border-radius: 8px !important;
        }
        
        .modal-title {
            font-size: 18px !important;
            font-weight: bold !important;
            color: #333 !important;
            margin-bottom: 10px !important;
        }
        
        .modal-description {
            font-size: 14px !important;
            color: #666 !important;
            margin-bottom: 15px !important;
        }
        
        .modal-details {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 10px !important;
            margin-top: 10px !important;
        }
        
        .modal-detail-item {
            display: flex !important;
            justify-content: space-between !important;
            padding: 8px 0 !important;
            border-bottom: 1px solid #eee !important;
        }
        
        .modal-detail-label {
            font-weight: 500 !important;
            color: #666 !important;
        }
        
        .modal-detail-value {
            color: #333 !important;
        }
        
        /* Ajuster la hauteur du modal */
        .modal-content {
            max-height: 90vh !important;
            overflow-y: auto !important;
        }
        
        /* Responsive pour mobile */
        @media (max-width: 768px) {
            .modal-details {
                grid-template-columns: 1fr !important;
            }
            
            .modal-navigation {
                padding: 10px !important;
                gap: 10px !important;
            }
            
            .modal-nav-btn {
                padding: 8px 12px !important;
                font-size: 12px !important;
                min-width: 80px !important;
            }
        }
    `;
    
    document.head.appendChild(style);
    console.log('✅ Styles CSS ajoutés');
}

// Fonction pour ajouter les événements
function addButtonEvents() {
    console.log('🔧 Ajout des événements...');
    
    const prevBtn = document.getElementById('prev-image');
    const nextBtn = document.getElementById('next-image');
    
    if (prevBtn && nextBtn) {
        // Supprimer les anciens événements en clonant les boutons
        const newPrevBtn = prevBtn.cloneNode(true);
        const newNextBtn = nextBtn.cloneNode(true);
        
        // Remplacer les anciens boutons
        prevBtn.parentNode.replaceChild(newPrevBtn, prevBtn);
        nextBtn.parentNode.replaceChild(newNextBtn, nextBtn);
        
        // Ajouter les événements aux nouveaux boutons
        newPrevBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('⬅️ Bouton précédent cliqué');
            navigateImage(-1);
        });
        
        newNextBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('➡️ Bouton suivant cliqué');
            navigateImage(1);
        });
        
        console.log('✅ Événements ajoutés');
    } else {
        console.log('❌ Boutons non trouvés');
    }
}

// Fonction pour naviguer entre les images
function navigateImage(direction) {
    console.log('🖼️ Navigation:', direction);
    
    const modal = document.getElementById('image-modal');
    if (!modal) return;
    
    const modalImage = modal.querySelector('.modal-image');
    const modalTitle = modal.querySelector('.modal-title');
    
    if (!modalImage || !modalTitle) return;
    
    // Trouver le maillot actuel
    const currentJersey = window.jerseyModal?.currentJersey;
    if (!currentJersey || !currentJersey.images) return;
    
    // Calculer le nouvel index
    let newIndex = (window.jerseyModal.currentImageIndex || 0) + direction;
    
    // Vérifier les limites
    if (newIndex < 0) newIndex = currentJersey.images.length - 1;
    if (newIndex >= currentJersey.images.length) newIndex = 0;
    
    console.log('📊 Nouvel index:', newIndex, 'sur', currentJersey.images.length);
    
    // Mettre à jour l'image
    const newImagePath = `${window.CONFIG.IMAGES_BASE_URL}/${currentJersey.images[newIndex]}`;
    modalImage.src = newImagePath;
    
    // Mettre à jour l'index
    if (window.jerseyModal) {
        window.jerseyModal.currentImageIndex = newIndex;
    }
    
    // Mettre à jour les boutons et miniatures
    updateButtons();
    updateThumbnails();
}

// Fonction pour mettre à jour les miniatures
function updateThumbnails() {
    const modal = document.getElementById('image-modal');
    if (!modal) return;
    
    const thumbnails = modal.querySelectorAll('.modal-thumbnail');
    const currentIndex = window.jerseyModal?.currentImageIndex || 0;
    
    thumbnails.forEach((thumb, index) => {
        if (index === currentIndex) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });
}

// Fonction pour changer l'image de couverture depuis une miniature
function changeCoverImageFromThumbnail(jersey, imageIndex) {
    console.log('🖼️ Changement de l\'image de couverture:', jersey.id, imageIndex);
    
    // Mettre à jour le maillot
    jersey.thumbnail = jersey.images[imageIndex];
    
    // Sauvegarder dans le fichier JSON
    fetch('data/jerseys.json')
        .then(response => response.json())
        .then(jerseys => {
            const jerseyIndex = jerseys.findIndex(j => j.id === jersey.id);
            if (jerseyIndex !== -1) {
                jerseys[jerseyIndex].thumbnail = jersey.images[imageIndex];
                
                // Sauvegarder (simulation - dans un vrai projet, ceci serait une requête serveur)
                console.log('✅ Image de couverture mise à jour:', jersey.images[imageIndex]);
                
                // Afficher un message de confirmation
                const confirmMsg = document.createElement('div');
                confirmMsg.style.cssText = `
                    position: fixed;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: #28a745;
                    color: white;
                    padding: 15px 25px;
                    border-radius: 8px;
                    z-index: 2000;
                    font-size: 14px;
                    font-weight: 500;
                `;
                confirmMsg.innerHTML = '✅ Image de couverture mise à jour !';
                document.body.appendChild(confirmMsg);
                
                // Supprimer le message après 3 secondes
                setTimeout(() => {
                    if (confirmMsg.parentElement) {
                        confirmMsg.remove();
                    }
                }, 3000);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la sauvegarde:', error);
        });
}

// Fonction pour mettre à jour les boutons
function updateButtons() {
    console.log('🔧 Mise à jour des boutons...');
    
    const modal = document.getElementById('image-modal');
    if (!modal) return;
    
    const nav = modal.querySelector('.modal-navigation');
    if (!nav) return;
    
    const prevBtn = nav.querySelector('#prev-image');
    const nextBtn = nav.querySelector('#next-image');
    const counter = nav.querySelector('.modal-counter');
    
    // Utiliser les données du modal directement
    const modalImage = modal.querySelector('.modal-image');
    const modalTitle = modal.querySelector('.modal-title');
    
    if (modalImage && modalTitle) {
        // Extraire l'index de l'image actuelle depuis le src
        const src = modalImage.src;
        const match = src.match(/(\d+)\.jpg$/);
        if (match) {
            const imageIndex = parseInt(match[1]);
            const totalImages = 5; // Nombre d'images par maillot
            
            if (counter) {
                counter.textContent = `${imageIndex + 1} / ${totalImages}`;
                console.log(`📊 Compteur mis à jour: ${imageIndex + 1} / ${totalImages}`);
            }
            
            if (prevBtn) {
                prevBtn.disabled = imageIndex === 0;
            }
            
            if (nextBtn) {
                nextBtn.disabled = imageIndex === totalImages - 1;
            }
        }
    }
    
    // Fallback avec jerseyModal si disponible
    if (window.jerseyModal && window.jerseyModal.currentJersey) {
        const currentImage = window.jerseyModal.currentImageIndex + 1;
        const totalImages = window.jerseyModal.currentJersey.images.length;
        
        if (counter) {
            counter.textContent = `${currentImage} / ${totalImages}`;
        }
        
        if (prevBtn) {
            prevBtn.disabled = window.jerseyModal.currentImageIndex === 0;
        }
        
        if (nextBtn) {
            nextBtn.disabled = window.jerseyModal.currentImageIndex === totalImages - 1;
        }
    }
}

// Fonction pour nettoyer les événements
function cleanupEvents() {
    console.log('🧹 Nettoyage des événements...');
    
    // Ne pas supprimer les boutons, juste nettoyer les événements
    // Les événements seront gérés par addButtonEvents()
}

// Fonction pour créer les miniatures
function createThumbnails() {
    console.log('🔧 Création des miniatures...');
    
    const modal = document.getElementById('image-modal');
    if (!modal) return;
    
    // Les événements seront gérés par addButtonEvents()
    
    // Supprimer les anciennes miniatures
    const existingThumbs = modal.querySelector('.modal-thumbnails');
    if (existingThumbs) {
        existingThumbs.remove();
    }
    
    if (!window.jerseyModal || !window.jerseyModal.currentJersey) return;
    
    const totalImages = window.jerseyModal.currentJersey.images.length;
    if (totalImages <= 1) return;
    
    // Créer le conteneur des miniatures
    const thumbnailsContainer = document.createElement('div');
    thumbnailsContainer.className = 'modal-thumbnails';
    
    // Créer les miniatures
    window.jerseyModal.currentJersey.images.forEach((image, index) => {
        const thumbnail = document.createElement('div');
        thumbnail.className = `modal-thumbnail ${index === window.jerseyModal.currentImageIndex ? 'active' : ''}`;
        
        const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${image}`;
        thumbnail.innerHTML = `
            <img src="${imagePath}" alt="Miniature ${index + 1}" loading="lazy">
            <div class="thumbnail-overlay">
                <span class="thumbnail-number">${index + 1}</span>
            </div>
        `;
        
        // Événement de clic pour changer d'image
        thumbnail.addEventListener('click', (e) => {
            e.stopPropagation(); // Empêcher la propagation
            console.log('🖼️ Miniature cliquée:', index);
            
            window.jerseyModal.currentImageIndex = index;
            window.jerseyModal.updateModalContent();
            updateButtons();
            updateThumbnails(); // Utiliser updateThumbnails au lieu de createThumbnails
            
            // En mode admin, changer l'image de couverture
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('admin') === 'true') {
                changeCoverImageFromThumbnail(window.jerseyModal.currentJersey, index);
            }
        });
        
        thumbnailsContainer.appendChild(thumbnail);
    });
    
    // Ajouter les miniatures à la modal
    modal.querySelector('.modal-content').appendChild(thumbnailsContainer);
    
    console.log('✅ Miniatures créées');
}

// Fonction principale
function initForceButtons() {
    console.log('🔧 Initialisation du forçage des boutons...');
    
    // Forcer la création des boutons immédiatement
    setTimeout(() => {
        console.log('🔧 Création forcée des boutons...');
        createNavigationButtons();
    }, 500);
    
    // Attendre que le modal soit ouvert
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                const modal = document.getElementById('image-modal');
                if (modal && modal.style.display === 'block') {
                    console.log('🔧 Modal ouvert détecté');
                    setTimeout(() => {
                        createNavigationButtons();
                        updateButtons();
                        createThumbnails();
                    }, 100);
                }
            }
        });
    });
    
    const modal = document.getElementById('image-modal');
    if (modal) {
        observer.observe(modal, { attributes: true });
    }
    
    // Écouter les clics sur les maillots
    document.addEventListener('click', (e) => {
        if (e.target.closest('.jersey-card')) {
            console.log('🔧 Clic sur maillot détecté');
            setTimeout(() => {
                createNavigationButtons();
                updateButtons();
                createThumbnails();
            }, 200);
        }
    });
    
    // Vérifier toutes les secondes si le modal est ouvert
    setInterval(() => {
        const modal = document.getElementById('image-modal');
        if (modal && modal.style.display === 'block') {
            console.log('🔧 Modal détecté par intervalle');
            createNavigationButtons();
            updateButtons();
            createThumbnails();
        }
    }, 1000);
    
    // Observer les changements d'image
    const imageObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
                console.log('🖼️ Image changée détectée');
                setTimeout(() => {
                    updateButtons();
                }, 100);
            }
        });
    });
    
    // Observer l'image du modal
    const modalImage = document.getElementById('modal-image');
    if (modalImage) {
        imageObserver.observe(modalImage, { attributes: true });
    }
}

// Démarrer quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initForceButtons);
} else {
    initForceButtons();
}
