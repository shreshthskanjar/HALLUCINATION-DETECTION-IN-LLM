// theme.js — handles dark/light toggle + localStorage

function applyTheme(theme) {
  if (theme === 'light') {
    document.documentElement.classList.add('light');
  } else {
    document.documentElement.classList.remove('light');
  }
  // Update toggle buttons
  document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });
}

function toggleTheme(theme) {
  localStorage.setItem('factra-theme', theme);
  applyTheme(theme);
}

// On page load — apply saved theme immediately
(function() {
  const saved = localStorage.getItem('factra-theme') || 'dark';
  applyTheme(saved);
})();