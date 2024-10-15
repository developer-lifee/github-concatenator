const toggleButton = document.getElementById('toggle-mode');

// Verificar si el modo oscuro está habilitado en localStorage
if (localStorage.getItem('dark-mode') === 'true') {
    document.body.classList.add('dark-mode');
    toggleButton.textContent = 'Cambiar a Modo Claro';
}

toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    toggleButton.textContent = isDarkMode ? 'Cambiar a Modo Claro' : 'Cambiar a Modo Oscuro';
    localStorage.setItem('dark-mode', isDarkMode);
});

