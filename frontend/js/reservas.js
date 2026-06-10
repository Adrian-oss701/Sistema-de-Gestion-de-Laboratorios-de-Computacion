verificarSesion();
let idEditarReserva = null;

async function cargarLaboratoriosSelect() {
    const respuesta = await fetch(API_URL + '/laboratorios');
    const labs = await respuesta.json();
    const select = document.getElementById('id_laboratorio');
    select.innerHTML = '<option value="">Seleccione laboratorio</option>';
    labs.forEach(lab => {
        select.innerHTML += `<option value="${lab.id_laboratorio}">${lab.nombre}</option>`;
    });
}

async function cargarReservas() {
    const respuesta = await fetch(API_URL + '/reservas');
    const datos = await respuesta.json();
    const tbody = document.getElementById('tablaReservas');
    tbody.innerHTML = '';

    datos.forEach(r => {
        tbody.innerHTML += `
            <tr>
                <td>${r.id_reserva}</td>
                <td>${r.laboratorio}</td>
                <td>${r.usuario}</td>
                <td>${r.fecha}</td>
                <td>${r.hora_inicio}</td>
                <td>${r.hora_fin}</td>
                <td>${r.estado}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick='editarReserva(${JSON.stringify(r)})'>Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarReserva(${r.id_reserva})">Eliminar</button>
                </td>
            </tr>`;
    });
}

document.getElementById('formReserva').addEventListener('submit', async function(e) {
    e.preventDefault();

    const reserva = {
        id_laboratorio: document.getElementById('id_laboratorio').value,
        fecha: document.getElementById('fecha').value,
        hora_inicio: document.getElementById('hora_inicio').value,
        hora_fin: document.getElementById('hora_fin').value,
        estado: document.getElementById('estado').value
    };

    const url = idEditarReserva ? API_URL + '/reservas/' + idEditarReserva : API_URL + '/reservas';
    const metodo = idEditarReserva ? 'PUT' : 'POST';

    const respuesta = await fetch(url, {
        method: metodo,
        headers: headersJSON(),
        body: JSON.stringify(reserva)
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    idEditarReserva = null;
    this.reset();
    cargarReservas();
});

function editarReserva(r) {
    idEditarReserva = r.id_reserva;
    document.getElementById('id_laboratorio').value = r.id_laboratorio;
    document.getElementById('fecha').value = r.fecha;
    document.getElementById('hora_inicio').value = r.hora_inicio;
    document.getElementById('hora_fin').value = r.hora_fin;
    document.getElementById('estado').value = r.estado;
}

async function eliminarReserva(id) {
    if (!confirm('¿Está seguro de eliminar esta reserva?')) return;

    const respuesta = await fetch(API_URL + '/reservas/' + id, {
        method: 'DELETE',
        headers: headersJSON()
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    cargarReservas();
}

async function buscarReservasPorFecha() {
    const fecha = document.getElementById('fechaBuscar').value;
    if (!fecha) {
        alert('Seleccione una fecha');
        return;
    }
    const respuesta = await fetch(API_URL + '/reservas/fecha/' + fecha);
    const datos = await respuesta.json();
    const div = document.getElementById('resultadoReservasFecha');
    div.innerHTML = '<h5>Reservas encontradas</h5>';
    if (datos.length === 0) {
        div.innerHTML += '<div class="alert alert-warning">No hay reservas para esa fecha.</div>';
        return;
    }
    datos.forEach(r => {
        div.innerHTML += `<div class="alert alert-info">${r.laboratorio} | ${r.hora_inicio} - ${r.hora_fin} | ${r.estado}</div>`;
    });
}

cargarLaboratoriosSelect();
cargarReservas();
