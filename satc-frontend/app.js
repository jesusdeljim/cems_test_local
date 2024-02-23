document.addEventListener('DOMContentLoaded', function() {
    const addMachineBtn = document.getElementById('add-machine');
    const addMachineForm = document.getElementById('add-machine-form');

    addMachineBtn.addEventListener('click', function() {
        addMachineForm.style.display = 'block'; // Muestra el formulario
    });

    addMachineForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita el envío del formulario por defecto
        const nombre = document.getElementById('nombre').value;
        const ubicacion = document.getElementById('ubicacion').value;
        const descripcion = document.getElementById('descripcion').value;

        const machineData = { nombre, ubicacion, descripcion, sensores: [] }; // Asume que sensores es un array vacío por ahora

        const response = await fetch('http://localhost:5000/add_machine', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(machineData)
        });
        if (response.ok) {
            const result = await response.json();
            console.log('Máquina añadida con éxito:', result);
            // Aquí puedes limpiar el formulario o actualizar la interfaz de usuario
        } else {
            console.error('Error al añadir máquina');
        }
    });
});