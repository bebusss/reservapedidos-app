document.addEventListener("DOMContentLoaded", () => {
    const pedidoForm = document.getElementById("pedidoForm");
    const reservaForm = document.getElementById("reservaForm");

    if (pedidoForm) {
        pedidoForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const data = {
                UsuarioID: document.getElementById("usuarioID").value,
                Estado: document.getElementById("estado").value,
                Total: document.getElementById("total").value,
            };
            await submitForm('/user/pedidos', data);
        });
    }

    if (reservaForm) {
        reservaForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const data = {
                UsuarioID: document.getElementById("usuarioID").value,
                FechaReserva: document.getElementById("fechaReserva").value,
                HoraReserva: document.getElementById("horaReserva").value,
                NumeroPersonas: document.getElementById("numeroPersonas").value,
                Estado: document.getElementById("estado").value,
            };
            await submitForm('/user/reservas', data);
        });
    }

    async function submitForm(url, data) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            alert(result.message || "Operación exitosa");
        } catch (error) {
            console.error("Error:", error);
            alert("Hubo un error al enviar el formulario.");
        }
    }
});
