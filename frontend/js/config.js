const API_URL = 'http://127.0.0.1:5000';

function obtenerToken() {
    return localStorage.getItem('token');
}

function headersJSON() {
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + obtenerToken()
    };
}

function verificarSesion() {
    if (!obtenerToken()) {
        window.location.href = 'login.html';
    }
}

function cerrarSesion() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    window.location.href = 'login.html';
}
