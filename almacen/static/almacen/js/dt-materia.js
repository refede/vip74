// Función para inicializar DataTable
function initializeDataTable() {
    const tableElement = $('#dataTable'); // Selector de tu tabla
    if ($.fn.DataTable.isDataTable(tableElement)) {
        return;
    }

    let path = "/almacen/materia"
    const SpecificConfig = {
		ajax: {
			url: `${path}/data/`,
			dataSrc: 'data'
		},
		dom: 'Pfrtip', // Incluye 'P' para SearchPanes
		searchPanes: {
			viewTotal: true,
			initCollapsed: true,
			preSelect: [
				{
					rows: ['activo'],
					column: 7
				}
			]
		},
		destroy: true,
		lengthMenu: [15, 50, 75, { label: 'All', value: -1 }],
		pageLength: 15,
		order: [[0, 'asc']],
		columnDefs: [
			{ searchPanes: { show: true }, targets: [2, 8] },
			{ searchPanes: { show: false }, targets: [0, 1, 3, 4, 5, 6, 7, 9, 10] },
			{ searchable: false, targets: [4, 5, 6, 7, 9, 10] },
			{ orderable: false, targets: [-1] },
            // { visible: false, targets: [2, 10] },
		],
		columns: [
			{ data: 'id' },//0
			{ data: 'nombre' },//01
			{ data: 'categoria__nombre' },//02
			{ data: 'tipo' },//03
			{ data: "espesor",      render: $.fn.dataTable.render.number(',', '.', 3, '') },//04
			{ data: "peso lineal",  render: $.fn.dataTable.render.number(',', '.', 1, '') },//05
			{ data: "ancho",        render: $.fn.dataTable.render.number(',', '.', 2, '') },//06
			{ data: "costo",        render: $.fn.dataTable.render.number(',', '.', 2, '') },//07
			// { data: 'tipo' },
			// { data: 'pasadas' },
			// { data: 'factor' },
			{
				data: "estado",
				render: function (data, type) {
					if (type === 'display') {
						return data === true ? '&#9745;' : '&#9744;';
					} else if (type === 'filter') {
						return data === true ? 'activo' : 'inactivo';
					} else if (type === 'sort') {
						return data ? 1 : 0;
					}
					return data.toString();
				}
			},//8
			{
				data: 'date_updated', render: function (data, type) {
					if (type === 'display' || type === 'filter') {
						return moment(data).format('DD/MM/YYYY');
					}
					return data;
				}
			},//9
			{
				data: "id",
                className: "dt-actions-cell", // <--- CONFIRMA ESTA LÍNEA
                render: function (data, type, row) { // 'row' te da acceso a otros datos si necesitas
                    const editarUrl = `${path}/editar/${data}/`;
                    const clonarUrl = `${path}/clonar/${data}/`;
                    const desactivarUrl = `${path}/desactivar/${data}/`;
                    return `<div class='btn-group actions-container d-flex justify-content-end'>
                                <button 
                                    type='button' 
                                    class='btn btn-sm btn-outline-primary action-button'
                                    hx-get='${editarUrl}'
                                    hx-target='#dialog'
                                    hx-swap='innerHTML'
                                    title='Editar ${row.id || ''}'>
                                    <i class='bi bi-pencil-square'></i>
                                </button>
                                <button 
                                    type='button' 
                                    class='btn btn-sm btn-outline-info action-button'
                                    hx-get='${clonarUrl}'
                                    hx-target='#dialog'
                                    hx-swap='innerHTML'
                                    title='Clonar ${row.id || ''}'>
                                    <i class='bi bi-copy'></i>
                                </button>
                                <button 
                                    type='button' 
                                    class='btn btn-sm btn-outline-danger action-button'
                                    hx-get='${desactivarUrl}'
                                    hx-target='#dialog'
                                    hx-swap='innerHTML'
                                    title='Desactivar ${row.id || ''}'>
                                    <i class='bi bi-x-lg'></i>
                                </button>
                            </div>`;
				}
			}//10
		],
	};
    tableElement.DataTable(getDefaultDataTablesConfig(SpecificConfig));
}

// Inicializar DataTable al cargar la página
$(document).ready(function () {
	initializeDataTable();
});
