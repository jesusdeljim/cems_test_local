var sensoresGlobales = [];

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('machine-form').onsubmit = async function(event) {
        event.preventDefault();

        // Recoger los datos de la máquina
        var formData = {
            nombre: document.getElementById('nombre').value,
            ubicacion: document.getElementById('ubicacion').value,
            descripcion: document.getElementById('descripcion').value,
            sensores: sensoresGlobales
        };


        try {
            const response = await fetch('http://localhost:5000/api/register_machines', {
                method: 'POST',
                body: JSON.stringify(formData),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log(data);
            // Aquí puedes redirigir al usuario o mostrar un mensaje de éxito
            window.location.href = '/maquinas.html';
        } catch (error) {
            console.error('Error al enviar el formulario:', error);
            // Aquí puedes manejar el error
        }
    };
});


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-sensor-btn').addEventListener('click', function() {
        var container = document.getElementById('sensores-container');
        var sensorCount = container.children.length + 1;
        var sensorDiv = document.createElement('div');
        sensorDiv.id = `sensor-${sensorCount}`;
        sensorDiv.innerHTML = `
            <label for="nombre-sensor-${sensorCount}">Nombre:</label>
            <input type="text" id="nombre-sensor-${sensorCount}" name="nombre-sensor-${sensorCount}"><br>
            <label for="tipo-sensor-${sensorCount}">Tipo:</label>
            <input type="text" id="tipo-sensor-${sensorCount}" name="tipo-sensor-${sensorCount}"><br>
            <label for="unidad-sensor-${sensorCount}">Unidad de Medida:</label>
            <input type="text" id="unidad-sensor-${sensorCount}" name="unidad-sensor-${sensorCount}"><br>
            <button type="button" onclick="saveSensor(${sensorCount})">Guardar Sensor</button>
        `;
        container.appendChild(sensorDiv);
    });
});

function saveSensor(sensorId) {
    var sensorDiv = document.getElementById(`sensor-${sensorId}`);
    var nombre = document.getElementById(`nombre-sensor-${sensorId}`).value;
    var tipo = document.getElementById(`tipo-sensor-${sensorId}`).value;
    var unidad = document.getElementById(`unidad-sensor-${sensorId}`).value;

    // Aquí puedes agregar el código para enviar los datos al backend o guardarlos en alguna estructura
    sensoresGlobales.push({
        nombre: nombre,
        tipo: tipo,
        unidad_medida: unidad
    });

    // Reemplaza los campos de entrada por una representación de texto del sensor
    sensorDiv.innerHTML = `
        <span>${nombre} (${tipo}, ${unidad})</span>
        <button type="button" onclick="editSensor(${sensorId})">Editar</button>
        <button type="button" onclick="deleteSensor(${sensorId})">Borrar</button>
    `;
}

function editSensor(sensorId) {
    // Aquí puedes agregar el código para editar la información del sensor
}

function deleteSensor(sensorId) {
    var sensorDiv = document.getElementById(`sensor-${sensorId}`);
    sensorDiv.remove();
}