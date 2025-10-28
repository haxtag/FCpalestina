/**
 * Utilitaires et fonctions helper pour le portfolio FC Palestina
 */

// ===== CONSTANTES =====
// CONFIG est maintenant défini dans config.js

// ===== FONCTIONS UTILITAIRES =====

/**
 * Debounce function pour optimiser les performances
 * @param {Function} func - Fonction à exécuter
 * @param {number} wait - Délai d'attente en ms
 * @returns {Function} - Fonction debounced
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function pour limiter la fréquence d'exécution
 * @param {Function} func - Fonction à exécuter
 * @param {number} limit - Limite de temps en ms
 * @returns {Function} - Fonction throttled
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Animation d'apparition progressive des éléments
 * @param {NodeList} elements - Éléments à animer
 * @param {number} delay - Délai entre chaque élément
 */
function animateElements(elements, delay = CONFIG.ANIMATION_DELAY) {
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('fade-in-up');
        }, index * delay);
    });
}

/**
 * Formatage des dates
 * @param {string|Date} date - Date à formater
 * @returns {string} - Date formatée
 */
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(date).toLocaleDateString('fr-FR', options);
}

/**
 * Génération d'un ID unique
 * @returns {string} - ID unique
 */
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

/**
 * Validation d'email
 * @param {string} email - Email à valider
 * @returns {boolean} - Email valide ou non
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Sanitisation du HTML pour éviter les XSS
 * @param {string} str - Chaîne à sanitiser
 * @returns {string} - Chaîne sanitisée
 */
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

/**
 * Gestion des erreurs avec logging
 * @param {Error} error - Erreur à logger
 * @param {string} context - Contexte de l'erreur
 */
function handleError(error, context = 'Unknown') {
    console.error(`[${context}]`, error);
    
    // Log uniquement (pas d'alert intrusif, car les erreurs sont souvent gérées ailleurs)
    // Si showNotification est disponible, on peut l'utiliser pour un message discret
    if (typeof showNotification === 'function' && window.CONFIG && window.CONFIG.DEBUG) {
        const msg = (error && (error.message || error.toString())) || 'Erreur inconnue';
        showNotification(`Erreur [${context}]: ${msg}`, 'error', 5000);
    }
}

/**
 * Affichage de notifications
 * @param {string} message - Message à afficher
 * @param {string} type - Type de notification (success, error, info, warning)
 * @param {number} duration - Durée d'affichage en ms
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Supprimer les notifications existantes
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Créer la notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${sanitizeHTML(message)}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Styles de la notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Fermeture automatique
    const autoClose = setTimeout(() => {
        closeNotification(notification);
    }, duration);
    
    // Fermeture manuelle
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        clearTimeout(autoClose);
        closeNotification(notification);
    });
}

/**
 * Fermeture d'une notification
 * @param {HTMLElement} notification - Élément notification
 */
function closeNotification(notification) {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

/**
 * Obtenir l'icône de notification
 * @param {string} type - Type de notification
 * @returns {string} - Nom de l'icône
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Obtenir la couleur de notification
 * @param {string} type - Type de notification
 * @returns {string} - Couleur CSS
 */
function getNotificationColor(type) {
    const colors = {
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8'
    };
    return colors[type] || '#17a2b8';
}

/**
 * Gestion du loading spinner
 * @param {boolean} show - Afficher ou masquer le spinner
 */
function toggleLoading(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.classList.toggle('active', show);
    }
}

/**
 * Copier du texte dans le presse-papiers
 * @param {string} text - Texte à copier
 * @returns {Promise<boolean>} - Succès de la copie
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copié dans le presse-papiers !', 'success');
        return true;
    } catch (err) {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showNotification('Copié dans le presse-papiers !', 'success');
            return true;
        } catch (fallbackErr) {
            handleError(fallbackErr, 'Copy to clipboard');
            return false;
        } finally {
            document.body.removeChild(textArea);
        }
    }
}

/**
 * Lazy loading des images
 * @param {NodeList} images - Images à charger
 */
function lazyLoadImages(images) {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback pour les navigateurs sans IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * Formatage des nombres avec séparateurs
 * @param {number} num - Nombre à formater
 * @returns {string} - Nombre formaté
 */
function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

/**
 * Génération d'un slug à partir d'une chaîne
 * @param {string} str - Chaîne à convertir
 * @returns {string} - Slug généré
 */
function slugify(str) {
    return str
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_-]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// ===== EXPORT POUR UTILISATION MODULAIRE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        debounce,
        throttle,
        animateElements,
        formatDate,
        generateId,
        isValidEmail,
        sanitizeHTML,
        handleError,
        showNotification,
        toggleLoading,
        copyToClipboard,
        lazyLoadImages,
        formatNumber,
        slugify,
        CONFIG: window.CONFIG
    };
}
