const toggleButton = document.getElementById('toggle-mode');
const repoUrl = document.getElementById('repo_url')
const outputfilename = document.getElementById('output_filename')
const re = new RegExp(".com\/(.*)\/tree");

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

repoUrl.addEventListener('keyup', () => {
    // Busca en base a la expresion regular el nombre del repo
    let downloadname = re.exec(repoUrl.value)
    if (downloadname !== null) {
        if (downloadname[1] !== null){
            // Esto solo se ejecuta si se encuentra coincidencia con (.*)
            outputfilename.value = downloadname[1].replaceAll("/", "_") + ".txt"
        }
    }
    else {
        outputfilename.value = ""
    }
});