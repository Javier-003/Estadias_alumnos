const btnDelete = document.querySelectorAll('.btn-delete');

if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        // <-- Agrega paréntesis aquí
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Estás seguro de eliminar el registro?')) {
                e.preventDefault();
            }
        });
    });
}