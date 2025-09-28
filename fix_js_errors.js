// Script de correction des erreurs JavaScript
// À exécuter dans la console du navigateur

console.log('🔧 Correction des erreurs JavaScript...');

// Vérifier si les fonctions existent
if (typeof debounce === 'undefined') {
    console.log('⚠️ Fonction debounce manquante');
}

if (typeof handleError === 'undefined') {
    console.log('⚠️ Fonction handleError manquante');
}

if (typeof toggleLoading === 'undefined') {
    console.log('⚠️ Fonction toggleLoading manquante');
}

// Vérifier CONFIG
if (typeof window.CONFIG === 'undefined') {
    console.log('⚠️ CONFIG manquant');
} else {
    console.log('✅ CONFIG disponible:', window.CONFIG);
}

// Vérifier les modules
if (typeof jerseyAPI === 'undefined') {
    console.log('⚠️ jerseyAPI manquant');
} else {
    console.log('✅ jerseyAPI disponible');
}

if (typeof gallery === 'undefined') {
    console.log('⚠️ gallery manquant');
} else {
    console.log('✅ gallery disponible');
}

console.log('🎯 Vérification terminée');
