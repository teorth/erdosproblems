// Theme Toggle Functionality
(function() {
    const THEME_KEY = 'erdos-problems-theme';
    const DARK_THEME = 'dark';
    const LIGHT_THEME = 'light';

    // Detect system preference
    function getSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return DARK_THEME;
        }
        return LIGHT_THEME;
    }

    // Get the default theme based on priority:
    // 1. User's saved preference
    // 2. System preference
    // 3. Light theme (fallback)
    function getDefaultTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved) {
            return saved;
        }
        return getSystemPreference();
    }

    // Apply theme to the body element
    function applyTheme(theme) {
        if (theme === DARK_THEME) {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
    }

    // Save theme preference
    function saveTheme(theme) {
        localStorage.setItem(THEME_KEY, theme);
    }

    // Toggle between themes
    function toggleTheme() {
        const currentTheme = document.body.classList.contains('dark-theme') ? DARK_THEME : LIGHT_THEME;
        const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;

        applyTheme(newTheme);
        saveTheme(newTheme);
    }

    // Initialize theme
    const defaultTheme = getDefaultTheme();
    applyTheme(defaultTheme);

    // Set up toggle button
    const toggleButton = document.getElementById('theme-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleTheme);
    }
})();
