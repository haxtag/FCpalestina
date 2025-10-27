// Safe no-op stub to avoid load error on missing script.
// Originally referenced to “force” active states on filter buttons; replaced by gallery.js delegation.
// Keeping this file prevents a resource load error that was triggering a global alert.
(function(){
  if (window?.CONFIG?.DEBUG) {
    console.log('[force_buttons] stub loaded');
  }
})();