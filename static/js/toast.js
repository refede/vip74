; (function () {
    const toastElement = document.getElementById("toast")
    const toastBody = document.getElementById("toast-body")
    const toast = new bootstrap.Toast(toastElement, { delay: 4000 })

    const toastAlertaElement = document.getElementById("toast-alerta")
    const toastAlertaBody = document.getElementById("toast-alerta-body")
    const toastAlerta = new bootstrap.Toast(toastAlertaElement, { autohide: false })

    htmx.on("showMessage", (e) => {
        toastBody.innerText = e.detail.value
        toast.show()
    })

    htmx.on("showErrores", (e) => {
        toastAlertaBody.innerText = e.detail.value
        toastAlerta.show()
    })

})()
