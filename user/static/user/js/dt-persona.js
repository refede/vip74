// Función para inicializar DataTable
function initializeDataTable() {
    const tableElement = $('#dataTable'); // Selector de tu tabla
    if ($.fn.DataTable.isDataTable(tableElement)) {
        return;
    }

    let path = "/user/persona"
    const SpecificConfig = {
        ajax: {
            url: `${path}/data/`,
            dataSrc: 'data'
        },
        lengthMenu: [20, 50, 75, { label: 'All', value: -1 }],
        pageLength: 20,
        order: [
            [0, 'asc']
        ],
        columnDefs: [
            { searchable: false, targets: [-1] },
            { orderable: false, targets: [-1] },
        ],
        columns: [
            { data: 'id' },//0
            { data: 'nombre' },//1
            { data: 'paterno' },//2
            {
                data: "estado",
                render: function (data) {
                    return data === true ? '&#9745;' : '&#9744;';
                }
            },//3
            {
                data: 'nacimiento', render: function (data, type) {
                    if (type === 'display' || type === 'filter') {
                        return moment(data).format('DD/MM');
                    }
                    return data;
                }
            },//4
            {
                data: 'ingreso', render: function (data, type) {
                    if (type === 'display' || type === 'filter') {
                        return moment(data).format('DD/MM/YYYY');
                    }
                    return data;
                }
            },//5
            {
                data: "id",
                className: "dt-actions-cell", // <--- CONFIRMA ESTA LÍNEA
                render: function (data, type, row) { // 'row' te da acceso a otros datos si necesitas
                    const editUrl = `${path}/editar/${data}/`;
                    return `<div class='btn-group actions-container d-flex justify-content-end'>
                                <button 
                                    class='btn btn-sm btn-outline-primary action-button'
                                    hx-get='${editUrl}'
                                    hx-target='#dialog'
                                    hx-swap='innerHTML'
                                    title='Editar ${row.nombre || ''}'>
                                    <i class='bi bi-pencil-square'></i>
                                </button>
                            </div>`;
                }
            },//6
        ],
    };
    tableElement.DataTable(getDefaultDataTablesConfig(SpecificConfig));
}

// Inicializar DataTable al cargar la página
$(document).ready(function () {
    initializeDataTable();
});