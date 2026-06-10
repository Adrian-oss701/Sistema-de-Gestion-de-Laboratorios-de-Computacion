verificarSesion();
let idEditar = null;

async function cargarLaboratorios() {
    const respuesta = await fetch(API_URL + '/laboratorios');
    const datos = await respuesta.json();
    const tbody = document.getElementById('tablaLaboratorios');
    tbody.innerHTML = '';

    datos.forEach(lab => {
        tbody.innerHTML += `
            <tr>
                <td>${lab.id_laboratorio}</td>
                <td>${lab.nombre}</td>
                <td>${lab.ubicacion}</td>
                <td>${lab.capacidad}</td>
                <td>${lab.estado}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick='editar(${JSON.stringify(lab)})'>Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminar(${lab.id_laboratorio})">Eliminar</button>
                </td>
            </tr>`;
    });
}

document.getElementById('formLaboratorio').addEventListener('submit', async function(e) {
    e.preventDefault();

    const laboratorio = {
        nombre: document.getElementById('nombre').value,
        ubicacion: document.getElementById('ubicacion').value,
        capacidad: document.getElementById('capacidad').value,
        estado: document.getElementById('estado').value
    };

    const url = idEditar ? API_URL + '/laboratorios/' + idEditar : API_URL + '/laboratorios';
    const metodo = idEditar ? 'PUT' : 'POST';

    const respuesta = await fetch(url, {
        method: metodo,
        headers: headersJSON(),
        body: JSON.stringify(laboratorio)
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    idEditar = null;
    this.reset();
    cargarLaboratorios();
});

function editar(lab) {
    idEditar = lab.id_laboratorio;
    document.getElementById('nombre').value = lab.nombre;
    document.getElementById('ubicacion').value = lab.ubicacion;
    document.getElementById('capacidad').value = lab.capacidad;
    document.getElementById('estado').value = lab.estado;
}

async function eliminar(id) {
    if (!confirm('¿Está seguro de eliminar este laboratorio?')) return;

    const respuesta = await fetch(API_URL + '/laboratorios/' + id, {
        method: 'DELETE',
        headers: headersJSON()
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    cargarLaboratorios();
}

async function consultarDisponibles() {
    const fecha = document.getElementById('fechaConsulta').value;
    if (!fecha) {
        alert('Seleccione una fecha');
        return;
    }

    const respuesta = await fetch(API_URL + '/laboratorios/disponibles?fecha=' + fecha);
    const datos = await respuesta.json();
    const div = document.getElementById('resultadoDisponibles');
    div.innerHTML = '<h5>Laboratorios disponibles</h5>';

    if (datos.length === 0) {
        div.innerHTML += '<div class="alert alert-warning">No hay laboratorios disponibles para esa fecha.</div>';
        return;
    }

    datos.forEach(lab => {
        div.innerHTML += `<div class="alert alert-success">${lab.nombre} - ${lab.ubicacion} - Capacidad: ${lab.capacidad}</div>`;
    });
}

cargarLaboratorios();
