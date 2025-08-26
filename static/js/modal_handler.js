; (function () {
    // --- Constantes y Variables del Modal ---
    const modalElement = document.getElementById("modal");
    const dialogElement = document.getElementById("dialog"); // Contenedor del contenido dentro del modal
    const spinnerElement = document.getElementById("spinner-container");
    let modalInstance = null;
    let triggeringElement = null;

    // --- Inicialización del Modal ---
    if (modalElement && dialogElement) {
        try {
            modalInstance = new bootstrap.Modal(modalElement);
            console.log("Modal Bootstrap inicializado para #modal.");
        } catch (e) {
            console.error("Error al inicializar Bootstrap Modal:", e);
            modalElement = null;
        }
    } else {
        console.error("Elemento #modal o #dialog no encontrado. Las funciones de modal no funcionarán correctamente.");
        return;
    }

    if (!modalInstance) {
        console.error("Instancia de Modal no creada, no se añadirán listeners.");
        return;
    }

    // --- HTMX Event Listeners (Usando document.body.addEventListener) ---
    // Escuchamos en 'body' y filtramos DENTRO del listener si el evento
    // es relevante para nuestro modal (#dialog).

    // ANTES de la petición HTMX relacionada con el modal
    document.body.addEventListener("htmx:beforeRequest", (evt) => {
        // Verificar si modalElement todavía existe en el DOM (importante en SPAs o cargas dinámicas)
        if (!document.body.contains(modalElement)) return;

        // Obtener detalles del evento HTMX
        const targetElement = evt.detail.target;
        const initiatingElement = evt.detail.elt; // Elemento que disparó la petición

        // Comprobar si el target o el iniciador están relacionados con nuestro #dialog
        const isDialogTarget = targetElement && targetElement.id === 'dialog';
        const isTargetInsideDialog = targetElement && targetElement.closest('#dialog'); //  <-- ESTO CUBRIRÁ #id_unidad_options
        const isTriggerInsideDialog = initiatingElement && initiatingElement.closest('#dialog'); // <-- ESTO CUBRIRÁ EL SELECT #id_metodo

        // Solo actuar si la petición afecta al diálogo del modal
        if (isDialogTarget || isTargetInsideDialog || isTriggerInsideDialog) {            console.log("htmx:beforeRequest (addEventListener en body) para #dialog o dentro. Mostrando spinner.");
            const modalHeader = modalElement.querySelector("#modal-header");
            const modalBody = modalElement.querySelector("#modal-body");
            const modalSpinner = modalElement.querySelector("#modal-spinner");
            const modalFooter = modalElement.querySelector("#modal-footer");

            if (modalHeader) {
                modalHeader.classList.add("d-none");
            }
            if (modalBody) {
                modalBody.classList.add("d-none");
            }
            if (modalSpinner) {
                modalSpinner.classList.remove("d-none"); // Muestra spinner
            }
            if (modalFooter) {
                modalFooter.style.display = "none"; // Oculta footer durante la carga
            }
        }
    });

    // DESPUÉS de la petición HTMX relacionada con el modal
    document.body.addEventListener("htmx:afterRequest", (evt) => {
        if (!document.body.contains(modalElement)) return;

        const xhr = evt.detail.xhr;
        const targetElement = evt.detail.target;
        const initiatingElement = evt.detail.elt;

        const isDialogTarget = targetElement && targetElement.id === 'dialog';
        const isTargetInsideDialog = targetElement && targetElement.closest('#dialog'); // <-- ESTO CUBRIRÁ #id_unidad_options
        const isTriggerInsideDialog = initiatingElement && initiatingElement.closest('#dialog'); // <-- ESTO CUBRIRÁ EL SELECT #id_metodo

        // Solo actuar si la petición afectó al diálogo del modal
        if (isDialogTarget || isTargetInsideDialog || isTriggerInsideDialog) {
            console.log(`htmx:afterRequest (addEventListener en body) procesando lógica modal (target: ${targetElement?.id}, inside: ${!!isTargetInsideDialog})`);

            // Restaurar estado visual (spinner, footer) siempre que la petición se relacione con el modal
            // const modalFooter = modalElement.querySelector(".modal-footer");
            // if (spinnerElement) spinnerElement.classList.add("d-none");
            // if (modalFooter) modalFooter.style.display = ""; // Restaura display

            // --- Chequeo de Autenticación/Autorización (401/403) ---
            if (xhr.status === 403 || xhr.status === 401) {
                console.warn(`Login requerido detectado (${xhr.status}). Redirigiendo...`);
                const currentPage = window.location.pathname + window.location.search;
                const loginBaseUrl = typeof LOGIN_URL !== 'undefined' ? LOGIN_URL : '/login/'; // Asume LOGIN_URL global o usa default
                const separator = loginBaseUrl.includes('?') ? '&' : '?';
                const loginRedirectUrl = loginBaseUrl + separator + 'next=' + encodeURIComponent(currentPage);
                window.location.href = loginRedirectUrl;
                return; // Salir para evitar más procesamiento
            }

            // --- Chequeo de otros errores ---
            if (!evt.detail.successful) {
                // Si hubo un error (distinto de 401/403), el contenido del error
                // probablemente ya fue insertado por HTMX si la petición tenía como target #dialog.
                // No cerramos el modal automáticamente, permitimos que el usuario vea el error.
                console.error(`Error ${xhr.status} ${xhr.statusText} en petición HTMX relacionada con el modal.`);
                // Podrías añadir lógica aquí para mostrar un mensaje de error genérico si lo prefieres.
                // Ejemplo: const modalTitle = modalElement.querySelector(".modal-title");
                // if (modalTitle) modalTitle.innerHTML = "Error al procesar";
                return; // Salir lógica modal exitosa
            }

            // --- Procesamiento Exitoso ---
            // Si la petición fue exitosa Y el target era el dialog Y no fue una respuesta 'sin contenido' (204) o error de validación (422)
            // aseguramos que el modal esté visible.
            if (isDialogTarget && xhr.status !== 204 && xhr.status !== 422) {
                console.log("Contenido cargado/actualizado en #dialog vía HTMX, asegurando visibilidad modal.");
                modalInstance.show();
            }
            // Si la petición vino de dentro del diálogo (isInsideDialog) y fue exitosa,
            // HTMX ya actualizó la parte correspondiente DENTRO del diálogo.
            // No necesitamos hacer nada más con el estado del modal aquí.
        }
    });

    // --- Aquí inicializamos Choices.js DESPUÉS de que HTMX hace el swap ---
    document.body.addEventListener("htmx:afterSwap", (evt) => {
        if (evt.detail.target.id === "dialog") {
            console.log("Inicializando Choices.js en selects dentro del modal...");
            const selects = evt.detail.target.querySelectorAll("select");
            selects.forEach((select) => {
                if (!select.dataset.choicesInitialized) {
                    new Choices(select, {
                        removeItemButton: true,
                        searchEnabled: true,
                        shouldSort: false,
                        placeholder: true,
                        placeholderValue: "Selecciona una opción",
                        noResultsText: "No se encontraron resultados",
                        noChoicesText: "No hay opciones disponibles",
                        itemSelectText: "Presiona para seleccionar",
                    });
                    select.dataset.choicesInitialized = "true";
                }
            });
        }
    });

    // ANTES del intercambio (Swap) - Prevenir swap vacío para #dialog
    document.body.addEventListener("htmx:beforeSwap", (evt) => {
        if (!document.body.contains(modalElement)) return;

        // Verificar si el target del swap es nuestro #dialog
        if (evt.detail.target.id === "dialog") {
            // Verificar si la respuesta está vacía (podría ser null, undefined o string vacío)
            if (!evt.detail.xhr.response) {
                console.warn("HTMX beforeSwap (addEventListener en body): Respuesta vacía para #dialog, cancelando swap y ocultando modal.");
                modalInstance.hide(); // Ocultar el modal
                evt.detail.shouldSwap = false; // Cancelar el swap
            }
        }
    });

    document.body.addEventListener("htmx:trigger", (evt) => {
        // --- Log para depurar ---
        console.log("Evento htmx:trigger recibido:", evt);
        console.log("Detalle del evento:", evt.detail);
        // ------------------------

        // Lógica para closeModal (solo si modal existe)
        if (evt.detail.name === "closeModal") {
            const modalElement = document.getElementById("modal"); // Busca el modal aquí
            const modalInstance = modalElement ? bootstrap.Modal.getInstance(modalElement) : null; // Obtén instancia si existe
            if (modalElement && modalInstance && modalElement.classList.contains('show')) {
                console.log("Trigger 'closeModal' detectado. Cerrando modal.");
                modalInstance.hide();
            }
        }
    });

    // --- Manejo de Eventos Nativos de Bootstrap Modal (Se mantienen igual) ---
    // Estos listeners SÍ deben estar directamente en modalElement porque
    // son específicos de Bootstrap y de ESE elemento modal.

    if (modalElement && modalInstance) { // Re-chequeo por si acaso
        modalElement.addEventListener('show.bs.modal', function (event) {
            triggeringElement = event.relatedTarget; // Elemento que hizo clic para abrir
            console.log("Modal show.bs.modal - Triggered by:", triggeringElement);
        });

        modalElement.addEventListener('shown.bs.modal', function () {
            console.log("Modal shown.bs.modal - Setting focus.");
            // Intenta enfocar el primer elemento con 'autofocus' dentro del modal
            const elementWithAutofocus = modalElement.querySelector('[autofocus]');
            if (elementWithAutofocus) {
                elementWithAutofocus.focus();
            } else {
                // Si no, enfoca el primer elemento enfocable estándar
                const firstFocusable = modalElement.querySelector(
                    'button, [href], input:not([type=hidden]):not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
                );
                if (firstFocusable) {
                    firstFocusable.focus();
                }
            }
        });

        modalElement.addEventListener('hide.bs.modal', function (event) {
            console.log("Modal hide.bs.modal - Attempting to return focus.");
            // Devolver foco al elemento que abrió el modal, si aún existe y es visible
            if (triggeringElement) {
                try {
                    // Comprobar si el elemento sigue en el DOM y es visible
                    if (document.body.contains(triggeringElement) && triggeringElement.offsetParent !== null) {
                        triggeringElement.focus();
                    } else {
                        console.log("Triggering element no longer visible or focusable.");
                        triggeringElement = null; // No se puede enfocar, olvidar referencia
                    }
                } catch (e) {
                    console.warn("Error returning focus:", e);
                    triggeringElement = null; // Algo falló, olvidar referencia
                }
            }
        });

        modalElement.addEventListener('hidden.bs.modal', function () {
            console.log("Modal hidden.bs.modal - Clearing #dialog content and resetting trigger.");
            if (dialogElement) {
                // Limpiar el contenido del diálogo para la próxima vez que se abra
                dialogElement.innerHTML = '<div class="text-center p-5"><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Cargando...</div>'; // O simplemente ""
            }
            // Limpiar título también podría ser buena idea
            const modalTitle = modalElement.querySelector(".modal-title");
            if (modalTitle) {
                modalTitle.innerHTML = "Modal"; // Título por defecto
            }
            // Resetear referencia al elemento que lo abrió
            triggeringElement = null;
        });
    } // Fin listeners Bootstrap

})(); // Fin del IIFE