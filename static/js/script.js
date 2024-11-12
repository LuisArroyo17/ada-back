// Función para permitir el arrastre sobre el área de drop
function dragOverHandler(event) {
    event.preventDefault();
}

// Función para manejar el evento de drop
function dropHandler(event, area) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        displayFile(file, area);
    }
}

// Función para mostrar el archivo en el área correspondiente
function displayFile(file, area) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const displayElement = area === 'left' 
            ? document.getElementById('fileDisplayLeft') 
            : document.getElementById('fileDisplayRight');
        displayElement.innerText = `Archivo: ${file.name}`;
    };
    reader.readAsText(file);
}

// Lógica para el botón "Analizar"
document.getElementById('btnAnalizar').addEventListener('click', function() {
    const leftFileContent = document.getElementById('fileDisplayLeft').innerText;
    const rightFileContent = document.getElementById('fileDisplayRight').innerText;
    
    if (leftFileContent && rightFileContent) {
        // Lógica para analizar los archivos
        console.log('Analizando los archivos:', leftFileContent, rightFileContent);
        alert('Archivos listos para ser analizados.');
    } else {
        alert('Por favor, arrastra ambos archivos antes de analizar.');
    }
});
