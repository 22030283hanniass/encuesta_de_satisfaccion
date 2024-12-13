document.getElementById('departamento').addEventListener('change', function () {
    const departamento = this.value.trim(); // Eliminar espacios innecesarios
    const empleadoSelect = document.getElementById('empleado');
    const errorMessage = document.getElementById('error-message');

    // Mostrar estado de carga inicial
    empleadoSelect.innerHTML = '<option value="">-- Cargando empleados... --</option>';
    errorMessage.classList.add('hidden'); // Ocultar mensaje de error

    if (departamento) {
        fetch(`/empleados/${encodeURIComponent(departamento)}`) // Corregir el uso de backticks
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                empleadoSelect.innerHTML = '<option value="">-- Selecciona un empleado --</option>';

                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(empleado => {
                        const option = document.createElement('option');
                        option.value = empleado;
                        option.textContent = empleado;
                        empleadoSelect.appendChild(option);
                    });
                } else {
                    empleadoSelect.innerHTML = '<option value="">-- No hay empleados disponibles --</option>';
                }
            })
            .catch(error => {
                console.error('Error al cargar empleados:', error);
                empleadoSelect.innerHTML = '<option value="">-- Error al cargar empleados --</option>';
                errorMessage.textContent = 'Error al cargar los empleados. Intenta nuevamente.';
                errorMessage.classList.remove('hidden'); // Mostrar mensaje de error
            });
    } else {
        empleadoSelect.innerHTML = '<option value="">-- Selecciona un empleado --</option>';
    }
});
