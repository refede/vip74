/**
 * Crea y devuelve un objeto de configuración de DataTables con opciones comunes
 * y las específicas proporcionadas.
 *
 * @param {object} specificConfig - Objeto con la configuración específica de la tabla
 *                                 (obligatorio: ajax, columns).
 * @returns {object} - Objeto de configuración completo para $.DataTable().
 */
function getDefaultDataTablesConfig(specificConfig) {

    // --- Validación básica ---
    if (!specificConfig || typeof specificConfig !== 'object') {
        console.error("getDefaultDataTablesConfig: Se requiere un objeto specificConfig.");
        return {}; // Devuelve objeto vacío para evitar error mayor
    }
    if (!specificConfig.ajax || !specificConfig.columns) {
        console.error("getDefaultDataTablesConfig: specificConfig debe incluir 'ajax' y 'columns'.");
        return {};
    }

    // --- Opciones Comunes por Defecto ---
    const commonConfig = {
        deferRender: true,
        responsive: true,
        // --- Callback Común para procesar HTMX ---
        drawCallback: function (settings) {
            const tableNode = this.api().table().node();
            // Procesar HTMX después de cada dibujo
            setTimeout(() => {
                htmx.process(tableNode);
            }, 0);
        },
        // --- Callback Común para Autofocus en Búsqueda ---
        initComplete: function (settings, json) {
            try {
                const tableWrapper = $(this.api().table().container());
                const searchInput = tableWrapper.find('.dt-search input[type="search"], .dataTables_filter input[type="search"]').first();
                if (searchInput.length > 0) {
                    searchInput.focus();
                } else {
                    // No es un error crítico, solo advertencia si no se encuentra
                    // console.warn("DataTables search input not found on initComplete.");
                }
            } catch (e) {
                console.error("Error setting focus on search input:", e);
            }
        },
        // // --- Idioma Común ---
        // language: {
        //     url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json', // O tu URL de idioma preferida
        //     search: "_INPUT_",
        //     searchPlaceholder: "Buscar en tabla..."
        // },
        // --- DOM por defecto (puedes sobrescribirlo en specificConfig si es necesario) ---
        // dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rt<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
    };

    // --- Fusionar Configuraciones ---
    // Las opciones en specificConfig sobrescribirán las comunes si tienen la misma clave.
    // Usamos Object.assign para crear un nuevo objeto combinado.
    const finalConfig = Object.assign({}, commonConfig, specificConfig);

    return finalConfig;
}

// Puedes añadir más funciones de utilidad aquí si lo necesitas