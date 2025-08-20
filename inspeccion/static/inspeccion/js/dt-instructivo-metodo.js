// Función para inicializar DataTable
function initializeDataTable() {
    const tableElement = $('#dataTable'); // Selector de tu tabla
    if ($.fn.DataTable.isDataTable(tableElement)) {
        return;
    }

	let path = "/inspeccion/instructivo_metodo"
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
			{ searchable: false, targets: [2, 3, 5] },
			{ orderable: false, targets: [-1] },
		],
		columns: [
			{ data: 'instructivo__id' },
			{ data: 'metodo__id' },
			{
				data: "critico",
				render: function(data) {
					return data === true ? '&#9745;' : '&#9744;';
				}
			},
			{
				data: "requerido",
				render: function(data) {
					return data === true ? '&#9745;' : '&#9744;';
				}
			},
			{
				data: "estado",
				render: function(data) {
					return data === true ? '&#9745;' : '&#9744;';
				}
			},
			{
				data: "id",
                className: "dt-actions-cell", // <--- CONFIRMA ESTA LÍNEA
                render: function (data, type, row) { // 'row' te da acceso a otros datos si necesitas
                    const editarUrl = `${path}/editar/${data}/`;
                    return `<div class='btn-group actions-container d-flex justify-content-end'>
                                <button 
                                    type='button' 
                                    class='btn btn-sm btn-outline-primary action-button'
                                    hx-get='${editarUrl}'
                                    hx-target='#dialog'
                                    hx-swap='innerHTML'
                                    title='Editar ${row.nombre || ''}'>
                                    <i class='bi bi-pencil-square'></i>
                                </button>
                            </div>`;
                }
			},
		],
	};
    tableElement.DataTable(getDefaultDataTablesConfig(SpecificConfig));
}

// Inicializar DataTable al cargar la página
$(document).ready(function () {
	initializeDataTable();
});