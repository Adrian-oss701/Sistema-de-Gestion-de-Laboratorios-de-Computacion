verificarSesion();
let idEditarIncidencia = null;

async function cargarSelects() {
    const labsResp = await fetch(API_URL + '/laboratorios');
    const labs = await labsResp.json();
    const labSelect = document.getElementById('id_laboratorio');
    labSelect.innerHTML = '<option value="">Seleccione laboratorio</option>';
    labs.forEach(lab => {
        labSelect.innerHTML += `<option value="${lab.id_laboratorio}">${lab.nombre}</option>`;
    });

    const equiposResp = await fetch(API_URL + '/equipos');
    const equipos = await equiposResp.json();
    const equipoSelect = document.getElementById('id_equipo');
    equipoSelect.innerHTML = '<option value="">Sin equipo específico</option>';
    equipos.forEach(eq => {
        equipoSelect.innerHTML += `<option value="${eq.id_equipo}">${eq.codigo} - ${eq.descripcion}</option>`;
    });
}

async function cargarIncidencias() {
    const respuesta = await fetch(API_URL + '/incidencias');
    const datos = await respuesta.json();
    const tbody = document.getElementById('tablaIncidencias');
    tbody.innerHTML = '';

    datos.forEach(i => {
        tbody.innerHTML += `
            <tr>
                <td>${i.id_incidencia}</td>
                <td>${i.laboratorio}</td>
                <td>${i.equipo || 'Ambiente'}</td>
                <td>${i.descripcion}</td>
                <td>${i.fecha}</td>
                <td>${i.estado}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick='editarIncidencia(${JSON.stringify(i)})'>Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarIncidencia(${i.id_incidencia})">Eliminar</button>
                </td>
            </tr>`;
    });
}

document.getElementById('formIncidencia').addEventListener('submit', async function(e) {
    e.preventDefault();

    const idEquipo = document.getElementById('id_equipo').value;
    const incidencia = {
        id_laboratorio: document.getElementById('id_laboratorio').value,
        id_equipo: idEquipo === '' ? null : idEquipo,
        descripcion: document.getElementById('descripcion').value,
        fecha: document.getElementById('fecha').value,
        estado: document.getElementById('estado').value
    };

    const url = idEditarIncidencia ? API_URL + '/incidencias/' + idEditarIncidencia : API_URL + '/incidencias';
    const metodo = idEditarIncidencia ? 'PUT' : 'POST';

    const respuesta = await fetch(url, {
        method: metodo,
        headers: headersJSON(),
        body: JSON.stringify(incidencia)
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    idEditarIncidencia = null;
    this.reset();
    cargarIncidencias();
});

function editarIncidencia(i) {
    idEditarIncidencia = i.id_incidencia;
    document.getElementById('id_laboratorio').value = i.id_laboratorio;
    document.getElementById('id_equipo').value = i.id_equipo || '';
    document.getElementById('descripcion').value = i.descripcion;
    document.getElementById('fecha').value = i.fecha;
    document.getElementById('estado').value = i.estado;
}

async function eliminarIncidencia(id) {
    if (!confirm('¿Está seguro de eliminar esta incidencia?')) return;

    const respuesta = await fetch(API_URL + '/incidencias/' + id, {
        method: 'DELETE',
        headers: headersJSON()
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    cargarIncidencias();
}

async function buscarIncidenciasLaboratorio() {
    const id = document.getElementById('idLabBuscar').value;
    if (!id) {
        alert('Ingrese el ID del laboratorio');
        return;
    }
    const respuesta = await fetch(API_URL + '/incidencias/laboratorio/' + id);
    const datos = await respuesta.json();
    const div = document.getElementById('resultadoIncidenciasLab');
    div.innerHTML = '<h5>Incidencias encontradas</h5>';
    if (datos.length === 0) {
        div.innerHTML += '<div class="alert alert-warning">No hay incidencias en ese laboratorio.</div>';
        return;
    }
    datos.forEach(i => {
        div.innerHTML += `<div class="alert alert-danger">${i.fecha} | ${i.descripcion} | ${i.estado}</div>`;
    });
}

cargarSelects();
cargarIncidencias();
