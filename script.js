// script.js
// Función para mapear coordenadas del clic al mapa a lat/long aproximadas de Soacha
function getLatLongFromClick(event, mapElement) {
  const rect = mapElement.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  const width = rect.width;
  const height = rect.height;

  // Aproximación de límites de Soacha: lat 4.57-4.59, long -74.22 a -74.20
  const lat = 4.59 - (y / height) * 0.02;
  const long = -74.22 + (x / width) * 0.02;

  return { lat: lat.toFixed(4), long: long.toFixed(4) };
}

// Evento de clic en el mapa
document.getElementById('map').addEventListener('click', function(event) {
  const coords = getLatLongFromClick(event, this);
  document.getElementById('latitude').value = coords.lat;
  document.getElementById('longitude').value = coords.long;
});

// Manejo de carga de archivos
document.getElementById('dropzone-file').addEventListener('change', function(event) {
  const files = event.target.files;
  const preview = document.getElementById('file-preview');
  preview.innerHTML = '';

  if (files.length > 0) {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (file.size > 10 * 1024 * 1024) { // 10MB
        alert('El archivo ' + file.name + ' es demasiado grande. Máximo 10MB.');
        continue;
      }

      const fileItem = document.createElement('div');
      fileItem.className = 'flex items-center gap-2 mt-2';
      fileItem.innerHTML = `
        <span class="material-symbols-outlined text-sm">attach_file</span>
        <span class="text-sm text-black dark:text-white">${file.name}</span>
        <span class="text-xs text-black/50 dark:text-white/50">(${ (file.size / 1024 / 1024).toFixed(2) } MB)</span>
      `;
      preview.appendChild(fileItem);
    }
  }
});

// Validación y envío del formulario
document.getElementById('reportForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  const report = {
    eventType: formData.get('event-type'),
    dateTime: formData.get('event-date'),
    latitude: document.getElementById('latitude').value,
    longitude: document.getElementById('longitude').value,
    description: formData.get('description'),
    files: []
  };

  // Validar campos requeridos
  if (!report.eventType || !report.dateTime || !report.latitude || !report.longitude || !report.description) {
    showError('Por favor, complete todos los campos requeridos.');
    return;
  }

  // Agregar archivos
  const files = document.getElementById('dropzone-file').files;
  for (let i = 0; i < files.length; i++) {
    report.files.push({
      name: files[i].name,
      size: files[i].size,
      type: files[i].type
    });
  }

  // En una aplicación real, aquí se enviaría a un servidor
  // Por ahora, guardamos en localStorage para simulación
  saveReport(report);

  showSuccess();
  this.reset();
  document.getElementById('file-preview').innerHTML = '';
});

function saveReport(report) {
  const reports = JSON.parse(localStorage.getItem('communityReports') || '[]');
  reports.push({ ...report, id: Date.now(), timestamp: new Date().toISOString() });
  localStorage.setItem('communityReports', JSON.stringify(reports));
}

function showSuccess() {
  const successMsg = document.getElementById('success-message');
  const errorMsg = document.getElementById('error-message');
  successMsg.style.display = 'block';
  errorMsg.style.display = 'none';
  setTimeout(() => successMsg.style.display = 'none', 5000);
}

function showError(message) {
  const errorMsg = document.getElementById('error-message');
  const successMsg = document.getElementById('success-message');
  errorMsg.textContent = message;
  errorMsg.style.display = 'block';
  successMsg.style.display = 'none';
  setTimeout(() => errorMsg.style.display = 'none', 5000);
}

// Inicializar valores por defecto
document.getElementById('event-date').value = new Date().toISOString().slice(0, 16);