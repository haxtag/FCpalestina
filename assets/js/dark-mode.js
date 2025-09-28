/**
 * DARK MODE TOGGLE - FC PALESTINA
 * Gestion du mode sombre avec persistance localStorage
 */

class DarkModeToggle {
    constructor() {
        this.themeToggle = null;
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Appliquer le thème sauvegardé
        this.applyTheme(this.currentTheme);
        
        // Attendre que le DOM soit chargé
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.bindEvents());
        } else {
            this.bindEvents();
        }
    }

    bindEvents() {
        this.themeToggle = document.getElementById('theme-toggle');
        
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
            this.updateToggleIcon();
            console.log('🌙 Dark mode toggle initialisé');
        } else {
            console.warn('⚠️ Bouton theme-toggle introuvable');
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        this.updateToggleIcon();
        
        // Sauvegarder la préférence
        localStorage.setItem('theme', this.currentTheme);
        
        console.log(`🎨 Thème basculé vers: ${this.currentTheme}`);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
    }

    updateToggleIcon() {
        if (this.themeToggle) {
            const icon = this.themeToggle.querySelector('i');
            if (icon) {
                if (this.currentTheme === 'dark') {
                    icon.className = 'fas fa-sun';
                    this.themeToggle.title = 'Basculer en mode clair';
                } else {
                    icon.className = 'fas fa-moon';
                    this.themeToggle.title = 'Basculer en mode sombre';
                }
            }
        }
    }

    // Méthode pour forcer un thème depuis l'extérieur
    setTheme(theme) {
        if (theme === 'light' || theme === 'dark') {
            this.currentTheme = theme;
            this.applyTheme(theme);
            this.updateToggleIcon();
            localStorage.setItem('theme', theme);
        }
    }

    // Getter pour le thème actuel
    getTheme() {
        return this.currentTheme;
    }
}

// Initialiser immédiatement (avant même le DOMContentLoaded)
const darkModeToggle = new DarkModeToggle();

// Exposer globalement pour le debug
window.darkModeToggle = darkModeToggle;