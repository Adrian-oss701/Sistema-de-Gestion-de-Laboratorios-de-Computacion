document.getElementById('formLogin').addEventListener('submit', async function(e) {
    e.preventDefault();

    const correo = document.getElementById('correo').value;
    const password = document.getElementById('password').value;

    const respuesta = await fetch(API_URL + '/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({correo, password})
    });

    const data = await respuesta.json();

    if (respuesta.ok) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('usuario', JSON.stringify(data.usuario));
        window.location.href = 'index.html';
    } else {
        document.getElementById('mensaje').innerHTML = `<div class="alert alert-danger">${data.mensaje}</div>`;
    }
});
