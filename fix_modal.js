/**
 * Script de correction pour le modal principal
 */

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Script de correction du modal chargé');
    
    // Attendre que tous les scripts soient chargés
    setTimeout(() => {
        fixModal();
    }, 1000);
});

function fixModal() {
    console.log('🔧 Correction du modal en cours...');
    
    // Vérifier si le modal existe
    const modal = document.getElementById('image-modal');
    if (!modal) {
        console.error('❌ Modal non trouvé');
        return;
    }
    
    // Vérifier si jerseyModal existe
    if (typeof window.jerseyModal === 'undefined') {
        console.error('❌ jerseyModal non défini');
        return;
    }
    
    console.log('✅ Modal trouvé, correction en cours...');
    
    // Remplacer la méthode open du modal
    const originalOpen = window.jerseyModal.open.bind(window.jerseyModal);
    
    window.jerseyModal.open = function(jersey) {
        console.log('🔍 Modal.open() appelé avec:', jersey);
        
        if (!jersey) {
            console.error('❌ Aucun maillot fourni à la modal');
            return;
        }

        this.currentJersey = jersey;
        this.currentImageIndex = 0;
        this.jerseys = this.getJerseysInCategory(jersey.category);
        
        console.log('📸 Images du maillot:', jersey.images);
        console.log('📸 Nombre d\'images:', jersey.images ? jersey.images.length : 0);
        
        this.updateModalContent();
        this.show();
        
        // Animation d'entrée
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        console.log('✅ Modal ouvert avec succès');
    };
    
    // Remplacer la méthode updateModalContent
    const originalUpdateModalContent = window.jerseyModal.updateModalContent.bind(window.jerseyModal);
    
    window.jerseyModal.updateModalContent = function() {
        console.log('🔄 updateModalContent() appelé');
        console.log('📸 currentJersey:', this.currentJersey);
        console.log('📸 currentImageIndex:', this.currentImageIndex);
        
        if (!this.currentJersey) {
            console.error('❌ Aucun maillot actuel');
            return;
        }

        if (!this.currentJersey.images || this.currentJersey.images.length === 0) {
            console.error('❌ Aucune image dans le maillot');
            return;
        }

        const currentImage = this.currentJersey.images[this.currentImageIndex];
        const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${currentImage}`;

        console.log('🖼️ Image actuelle:', currentImage);
        console.log('🖼️ Chemin complet:', imagePath);

        // Mettre à jour l'image
        if (this.modalImage) {
            this.modalImage.src = imagePath;
            this.modalImage.alt = this.currentJersey.title;
            console.log('✅ Image mise à jour dans le modal');
        } else {
            console.error('❌ Élément modalImage non trouvé');
        }

        // Mettre à jour le titre
        if (this.modalTitle) {
            this.modalTitle.textContent = this.currentJersey.title;
        }

        // Mettre à jour la description
        if (this.modalDescription) {
            this.modalDescription.innerHTML = this.createDescriptionHTML();
        }

        // Mettre à jour la navigation
        this.updateNavigation();
        
        console.log('✅ updateModalContent() terminé');
    };
    
    // Remplacer la méthode updateNavigation
    const originalUpdateNavigation = window.jerseyModal.updateNavigation.bind(window.jerseyModal);
    
    window.jerseyModal.updateNavigation = function() {
        console.log('🧭 updateNavigation() appelé');
        
        // Supprimer l'ancienne navigation si elle existe
        const existingNav = this.modal.querySelector('.modal-nav');
        if (existingNav) {
            existingNav.remove();
            console.log('🗑️ Ancienne navigation supprimée');
        }

        // Créer la nouvelle navigation
        const nav = document.createElement('div');
        nav.className = 'modal-nav';
        
        const totalImages = this.currentJersey.images.length;
        const currentImage = this.currentImageIndex + 1;
        
        console.log('📊 Navigation - Total images:', totalImages, 'Image actuelle:', currentImage);
        
        nav.innerHTML = `
            <button class="modal-nav-btn" id="prev-image" ${this.currentImageIndex === 0 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i>
                Précédent
            </button>
            
            <span class="modal-counter">
                ${currentImage} / ${totalImages}
            </span>
            
            <button class="modal-nav-btn" id="next-image" ${this.currentImageIndex === totalImages - 1 ? 'disabled' : ''}>
                Suivant
                <i class="fas fa-chevron-right"></i>
            </button>
        `;

        // Ajouter la navigation à la modal
        const modalContent = this.modal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.appendChild(nav);
            console.log('✅ Navigation ajoutée au modal');
        } else {
            console.error('❌ Élément .modal-content non trouvé');
        }

        // Créer les miniatures
        this.createThumbnails();

        // Liaison des événements de navigation
        const prevBtn = nav.querySelector('#prev-image');
        const nextBtn = nav.querySelector('#next-image');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                console.log('⬅️ Bouton Précédent cliqué');
                this.previousImage();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                console.log('➡️ Bouton Suivant cliqué');
                this.nextImage();
            });
        }
        
        console.log('✅ updateNavigation() terminé');
    };
    
    // Remplacer la méthode createThumbnails
    const originalCreateThumbnails = window.jerseyModal.createThumbnails.bind(window.jerseyModal);
    
    window.jerseyModal.createThumbnails = function() {
        console.log('🖼️ createThumbnails() appelé');
        
        // Supprimer les anciennes miniatures
        const existingThumbs = this.modal.querySelector('.modal-thumbnails');
        if (existingThumbs) {
            existingThumbs.remove();
        }

        const totalImages = this.currentJersey.images.length;
        if (totalImages <= 1) {
            console.log('ℹ️ Une seule image, pas de miniatures');
            return;
        }

        console.log(`Création de ${totalImages} miniatures`);

        // Créer le conteneur des miniatures
        const thumbnailsContainer = document.createElement('div');
        thumbnailsContainer.className = 'modal-thumbnails';
        
        // Créer les miniatures
        this.currentJersey.images.forEach((image, index) => {
            const thumbnail = document.createElement('div');
            thumbnail.className = `modal-thumbnail ${index === this.currentImageIndex ? 'active' : ''}`;
            
            const imagePath = `${window.CONFIG.IMAGES_BASE_URL}/${image}`;
            thumbnail.innerHTML = `
                <img src="${imagePath}" alt="Miniature ${index + 1}" loading="lazy">
                <div class="thumbnail-overlay">
                    <span class="thumbnail-number">${index + 1}</span>
                </div>
            `;
            
            // Événement de clic pour changer d'image
            thumbnail.addEventListener('click', () => {
                this.currentImageIndex = index;
                this.updateModalContent();
                console.log(`✅ Miniature cliquée: ${index + 1}`);
            });
            
            thumbnailsContainer.appendChild(thumbnail);
        });

        // Ajouter les miniatures à la modal
        this.modal.querySelector('.modal-content').appendChild(thumbnailsContainer);
        
        console.log('✅ Miniatures créées');
    };
    
    // Ajouter le support du glissement tactile
    addTouchSupport();
    
    // Forcer l'application des styles CSS
    forceApplyStyles();
    
    console.log('✅ Modal corrigé avec succès !');
}

function addTouchSupport() {
    console.log('📱 Ajout du support tactile...');
    
    let startX = 0;
    let startY = 0;
    let endX = 0;
    let endY = 0;
    let isSwiping = false;
    
    const modal = document.getElementById('image-modal');
    const modalImage = document.getElementById('modal-image');
    
    if (!modal || !modalImage) {
        console.error('❌ Éléments du modal non trouvés pour le support tactile');
        return;
    }
    
    // Événements tactiles
    modalImage.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        isSwiping = true;
        console.log('👆 Début du glissement');
    }, { passive: true });
    
    modalImage.addEventListener('touchmove', (e) => {
        if (!isSwiping) return;
        
        endX = e.touches[0].clientX;
        endY = e.touches[0].clientY;
        
        // Calculer la direction du glissement
        const deltaX = endX - startX;
        const deltaY = endY - startY;
        
        // Si le glissement horizontal est plus important que le vertical
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            e.preventDefault(); // Empêcher le scroll de la page
        }
    }, { passive: false });
    
    modalImage.addEventListener('touchend', (e) => {
        if (!isSwiping) return;
        
        const deltaX = endX - startX;
        const deltaY = endY - startY;
        
        // Si le glissement horizontal est significatif
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            if (deltaX > 0) {
                // Glissement vers la droite = image précédente
                console.log('⬅️ Glissement vers la droite - Image précédente');
                if (window.jerseyModal) {
                    window.jerseyModal.previousImage();
                }
            } else {
                // Glissement vers la gauche = image suivante
                console.log('➡️ Glissement vers la gauche - Image suivante');
                if (window.jerseyModal) {
                    window.jerseyModal.nextImage();
                }
            }
        }
        
        isSwiping = false;
    }, { passive: true });
    
    // Ajouter un indicateur de glissement sur mobile
    const swipeHint = document.createElement('div');
    swipeHint.className = 'modal-swipe-hint';
    swipeHint.innerHTML = '👈 Glissez pour naviguer 👉';
    modal.querySelector('.modal-content').appendChild(swipeHint);
    
    // Afficher l'indice au début
    setTimeout(() => {
        swipeHint.classList.add('show');
        setTimeout(() => {
            swipeHint.classList.remove('show');
        }, 3000);
    }, 1000);
    
    console.log('✅ Support tactile ajouté');
}

function forceApplyStyles() {
    console.log('🎨 Application forcée des styles CSS...');
    
    // Créer un style inline pour s'assurer que les boutons sont visibles
    const style = document.createElement('style');
    style.textContent = `
        .modal-nav-btn {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            padding: 12px 20px !important;
            background: #2c5530 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            font-weight: 500 !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
            min-width: 120px !important;
            justify-content: center !important;
            margin: 0 10px !important;
        }
        
        .modal-nav-btn:hover:not(:disabled) {
            background: #1e3a21 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(44, 85, 48, 0.3) !important;
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
        
        .modal-navigation {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 20px !important;
            background: #f8f9fa !important;
            border-top: 1px solid #e0e0e0 !important;
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
        }
        
        .modal-thumbnail {
            position: relative !important;
            flex-shrink: 0 !important;
            width: 80px !important;
            height: 80px !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            cursor: pointer !important;
            border: 3px solid transparent !important;
            transition: all 0.3s ease !important;
        }
        
        .modal-thumbnail:hover {
            border-color: #2c5530 !important;
            transform: scale(1.05) !important;
        }
        
        .modal-thumbnail.active {
            border-color: #2c5530 !important;
            box-shadow: 0 0 0 2px rgba(44, 85, 48, 0.2) !important;
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
        
        .modal-swipe-hint {
            position: absolute !important;
            bottom: 20px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            background: rgba(0, 0, 0, 0.7) !important;
            color: white !important;
            padding: 8px 16px !important;
            border-radius: 20px !important;
            font-size: 12px !important;
            opacity: 0 !important;
            transition: opacity 0.3s ease !important;
            pointer-events: none !important;
        }
        
        .modal-swipe-hint.show {
            opacity: 1 !important;
        }
    `;
    
    document.head.appendChild(style);
    console.log('✅ Styles CSS forcés appliqués');
}
