; (function ($) { // Pasa jQuery como $ para asegurar compatibilidad
    'use strict';

    // --- DataTables Responsive HTMX Setup Function ---
    function setupResponsiveHtmxProcessing(tableQuery) {
        // Asegurarse de que es un objeto jQuery y tiene el método DataTable
        if (!tableQuery || !tableQuery.DataTable) {
            console.error("setupResponsiveHtmxProcessing: tableQuery inválido o no es un objeto jQuery con DataTable.");
            return;
        }

        try {
            const table = tableQuery.DataTable();

            // Verificar si el plugin Responsive está activo en esta tabla
            const isResponsive = table.settings()[0].oInit.responsive || table.settings()[0].responsive; // Comprobar config inicial

            if (isResponsive) {
                const tableId = tableQuery.attr('id') || 'Unknown Table';
                console.log(`Configurando listener 'responsive-display.htmx' para HTMX en tabla responsive: ${tableId}`);

                // Usar .off().on() para evitar duplicados si se llama múltiples veces
                table.off('responsive-display.htmx').on('responsive-display.htmx', function (e, datatable, row, showHide, update) {
                    // 'row' es un objeto de la API de DT para la fila afectada
                    // 'showHide' es true si se muestra el detalle, false si se oculta

                    if (showHide) {
                        // El detalle se acaba de mostrar
                        const childRowElement = row.child(); // Obtiene el elemento jQuery/DOM de la fila hija
                        if (childRowElement && childRowElement.length > 0 && childRowElement[0]) {
                            console.log("Responsive detail shown, processing HTMX for child row:", childRowElement[0]);
                            htmx.process(childRowElement[0]); // ¡Procesa HTMX en el contenido de la fila hija!
                        } else {
                            console.log("Responsive detail shown, but child row element not found or empty.");
                        }
                    }
                });

                // Forzar un redibujo inicial puede ayudar a detectar filas con hijos inmediatamente
                // table.responsive.recalc(); // Descomentar si es necesario

            } else {
                const tableId = tableQuery.attr('id') || 'Unknown Table';
                console.log(`Plugin Responsive no detectado o inactivo para la tabla: ${tableId}. No se añade listener 'responsive-display'.`);
            }
        } catch (e) {
            console.error("Error configurando DataTables Responsive HTMX:", e);
        }

    } // Fin de setupResponsiveHtmxProcessing

    // --- Inicialización de la Tabla Principal y Configuración Responsive ---
    $(document).ready(function () {
        const mainTableQuery = $('#dataTable'); // Tu tabla principal

        if (mainTableQuery.length === 0) {
            console.warn("#dataTable no encontrado en el DOM en document.ready.");
            return; // Salir si la tabla no existe
        }

        // Intentar configurar inmediatamente si ya es un DataTable al cargar el script
        if ($.fn.DataTable.isDataTable(mainTableQuery)) {
            console.log("#dataTable ya inicializado, configurando responsive HTMX.");
            setupResponsiveHtmxProcessing(mainTableQuery);
        } else {
            // Si no, esperar al evento de inicialización 'init.dt'
            console.log("#dataTable no inicializado aún, esperando evento 'init.dt'.");
            mainTableQuery.one('init.dt', function () { // Usar .one() para que se ejecute solo una vez por tabla
                console.log("Evento 'init.dt' recibido para #dataTable, configurando responsive HTMX.");
                // Usar $(this) para referirse a la tabla que disparó el evento
                setupResponsiveHtmxProcessing($(this));
            });
        }

        // Podrías tener aquí la inicialización de DataTables si no se hace en otro lugar:
        // if (!$.fn.DataTable.isDataTable(mainTableQuery)) {
        //     mainTableQuery.DataTable({
        //         responsive: true,
        //         // ... otras opciones de DataTables ...
        //         initComplete: function(settings, json) {
        //             console.log("DataTables initComplete for #dataTable.");
        //             // La configuración responsive ya se haría con el evento 'init.dt'
        //             // pero puedes poner otra lógica post-inicialización aquí.
        //         }
        //     });
        // }

    }); // Fin document.ready

    // --- Listener HTMX Global para Recarga de DataTable en 204 ---
    document.addEventListener("htmx:afterRequest", function (evt) {
        const xhr = evt.detail.xhr;

        // Si cualquier petición HTMX exitosa devuelve 204 No Content
        if (xhr.status === 204) {
            console.log("htmx:afterRequest(204) detectado. Intentando recargar #dataTable.");
            const mainTableQuery = $('#dataTable');

            // Verificar si DataTable está inicializado en #dataTable
            if ($.fn.DataTable.isDataTable(mainTableQuery)) {
                let table = mainTableQuery.DataTable();
                console.log("Recargando DataTable...");
                try {
                    // Comprobar si SearchPanes está activo y tiene el método (buena práctica)
                    if (table.searchPanes && typeof table.searchPanes.rebuildPane === 'function') {
                        // Recargar datos y LUEGO reconstruir paneles
                        table.ajax.reload(() => {
                            try {
                                // Intentar reconstruir los paneles solo si existen
                                if (table.searchPanes.container()) {
                                    table.searchPanes.rebuildPane(undefined, true); // true para mantener selección
                                    console.log("DataTable SearchPanes reconstruido después de 204.");
                                } else {
                                    console.log("SearchPanes container no encontrado, omitiendo reconstrucción.");
                                }
                            } catch (e) {
                                console.error("Error reconstruyendo SearchPanes:", e);
                            }
                        }, false); // false = no resetea paginación
                    } else {
                        // Recarga normal si SearchPanes no está activo o no se necesita reconstruir
                        table.ajax.reload(null, false);
                    }
                } catch (e) {
                    console.error("Error durante la recarga de DataTable:", e);
                }
            } else {
                console.warn("htmx:afterRequest(204), pero #dataTable no encontrado o no inicializado como DataTable.");
            }
        }
        // Nota: Este listener NO maneja la lógica específica del modal,
        // eso se hace en modal_handler.js
    });

})(jQuery); // Fin del IIFE para datatables_htmx_init.js