verificarSesion();
let idEditarEquipo = null;

async function cargarLaboratoriosSelect() {
    const respuesta = await fetch(API_URL + '/laboratorios');
    const labs = await respuesta.json();
    const select = document.getElementById('id_laboratorio');
    select.innerHTML = '<option value="">Seleccione laboratorio</option>';
    labs.forEach(lab => {
        select.innerHTML += `<option value="${lab.id_laboratorio}">${lab.nombre}</option>`;
    });
}

async function cargarEquipos() {
    const respuesta = await fetch(API_URL + '/equipos');
    const datos = await respuesta.json();
    const tbody = document.getElementById('tablaEquipos');
    tbody.innerHTML = '';

    datos.forEach(eq => {
        tbody.innerHTML += `
            <tr>
                <td>${eq.id_equipo}</td>
                <td>${eq.codigo}</td>
                <td>${eq.descripcion}</td>
                <td>${eq.estado}</td>
                <td>${eq.laboratorio}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick='editarEquipo(${JSON.stringify(eq)})'>Editar</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarEquipo(${eq.id_equipo})">Eliminar</button>
                </td>
            </tr>`;
    });
}

document.getElementById('formEquipo').addEventListener('submit', async function(e) {
    e.preventDefault();

    const equipo = {
        codigo: document.getElementById('codigo').value,
        descripcion: document.getElementById('descripcion').value,
        estado: document.getElementById('estado').value,
        id_laboratorio: document.getElementById('id_laboratorio').value
    };

    const url = idEditarEquipo ? API_URL + '/equipos/' + idEditarEquipo : API_URL + '/equipos';
    const metodo = idEditarEquipo ? 'PUT' : 'POST';

    const respuesta = await fetch(url, {
        method: metodo,
        headers: headersJSON(),
        body: JSON.stringify(equipo)
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    idEditarEquipo = null;
    this.reset();
    cargarEquipos();
});

function editarEquipo(eq) {
    idEditarEquipo = eq.id_equipo;
    document.getElementById('codigo').value = eq.codigo;
    document.getElementById('descripcion').value = eq.descripcion;
    document.getElementById('estado').value = eq.estado;
    document.getElementById('id_laboratorio').value = eq.id_laboratorio;
}

async function eliminarEquipo(id) {
    if (!confirm('¿Está seguro de eliminar este equipo?')) return;

    const respuesta = await fetch(API_URL + '/equipos/' + id, {
        method: 'DELETE',
        headers: headersJSON()
    });

    const data = await respuesta.json();
    alert(data.mensaje);
    cargarEquipos();
}

cargarLaboratoriosSelect();
cargarEquipos();
