PER_PREFIJO = (
    ("Sr.",     "Sr."),
    ("Sra.",    "Sra."),
    ("Ing.",    "Ing."),
    ("Lic.",    "Lic."),
)

PER_FORMACION = (
    ("ESTUDIANTE",  "ESTUDIANTE"),
    ("INGENIERO",   "INGENIERO"),
    ("LICENCIADO",  "LICENCIADO"),
    ("TÉCNICO",     "TÉCNICO"),
)

PER_DEPARTAMENTO = (
    ("PRODUCCIÓN",      "PRODUCCIÓN"),
    ("MANTENIMIENTO",   "MANTENIMIENTO"),
    ("LOGÍSTICA",       "LOGÍSTICA"),
)

PER_AREA = (
    ("LABORATORIO",     "LABORATORIO"),
    ("PRODUCCIÓN",      "PRODUCCIÓN"),
    ("BOBINADO",        "BOBINADO"),
    ("MANTENIMIENTO",   "MANTENIMIENTO"),
    ("LOGÍSTICA",       "LOGÍSTICA"),
    ("ALMACÉN",         "ALMACÉN"),
)

PER_PUESTO = (
    ("ANALISTA",    "ANALISTA"),
    ("ALMACENERO",  "ALMACENERO"),
    ("JEFE",        "JEFE"),
    ("SUPERVISOR",  "SUPERVISOR"),
)

PER_TIPO = (
    ("OPERARIO",    "OPERARIO"),
    ("EMPLEADO",    "EMPLEADO"),
)

PROPIEDAD_CHOICES = (
    ("FISICA",      "FISICA"),
    ("MECANICA",    "MECANICA"),
    ("VISUAL",      "VISUAL"),
    ("OTRO",        "OTRO"),
)

CONTENIDO_CHOICES = (
    ("ACTIVIDAD",       "ACTIVIDAD"),
    ("CONSIDERACIÓN",   "CONSIDERACIÓN"),
)

PRODUCTO_GAMA_CHOICES = (
    ("AUTOMOTOR",               "AUTOMOTOR"),
    ("CALZADO",                 "CALZADO"),
    ("CARPETERIA",              "CARPETERIA"),
    ("CONFECCIONES",            "CONFECCIONES"),
    ("FORROS Y EMPAQUE",        "FORROS Y EMPAQUE"),
    ("HOGAR E INSTITUCIONAL",   "HOGAR E INSTITUCIONAL"),
    ("INDUSTRIAL",              "INDUSTRIAL"),
    ("MARROQUINERIA",           "MARROQUINERIA"),
)

PRODUCTO_LINEA_CHOICES =(
    ("CORTINAS",                "CORTINAS"),
    ("CUERO SINTETICO",         "CUERO SINTETICO"),
    ("DOBLE FAZ",               "DOBLE FAZ"),
    ("ENCUADERNACIONES",        "ENCUADERNACIONES"),
    ("FILMS FLEXIBLES",         "FILMS FLEXIBLES"),
    ("FILMS RIGIDOS",           "FILMS RIGIDOS"),
    ("FILMS SEMIRIGIDOS",       "FILMS SEMIRIGIDOS"),
    ("GEOSINTETICOS",           "GEOSINTETICOS"),
    ("LAMINAS ESPUMADAS",       "LAMINAS ESPUMADAS"),
    ("LAMINAS MULTICAPAS",      "LAMINAS MULTICAPAS"),
    ("LONAS",                   "LONAS"),
    ("MANTELES",                "MANTELES"),
    ("PISOS",                   "PISOS"),
    ("PLANTILLAS ESPUMADAS",    "PLANTILLAS ESPUMADAS"),
    ("TAPICERIAS",              "TAPICERIAS"),
    ("TEXTILES PLASTIFICADOS",  "TEXTILES PLASTIFICADOS"),
)

PRODUCTO_SERIE_CHOICES = (
    ("", 		""),
    ("C10000", 	"C10000"),
    ("C20000", 	"C20000"),
    ("C30000", 	"C30000"),
    ("C40000", 	"C40000"),
    ("C50000", 	"C50000"),
    ("C60000", 	"C60000"),
    ("C70000", 	"C70000"),
    ("C80000", 	"C80000"),
    ("C90000", 	"C90000"),
    ("E13000", 	"E13000"),
    ("E20000", 	"E20000"),
    ("E30000", 	"E30000"),
    ("E40000", 	"E40000"),
    ("E50000", 	"E50000"),
    ("E60000", 	"E60000"),
    ("T1000", 	"T1000"),
)

PRODUCTO_PRG_CHOICES = (
    ("DIRECTOS",                "DIRECTOS"),
    ("ESTAMPADOS",              "ESTAMPADOS"),
    ("LAMINADOS",               "LAMINADOS"),
    ("LONAS",                   "LONAS"),
    ("PLASTIFICADOS",           "PLASTIFICADOS"),
    ("PLASTIFICADOS ADHESIVO",  "PLASTIFICADOS ADHESIVO"),
    ("SPREADING",               "SPREADING"),
    ("OTROS",                   "OTROS"),
)

FORMULACION_CAT_CHOICES = (
    ("FOR", "Formulación"),
    ("PIG", "Pigmentación"),
)

TOLERANCIA_CHOICES = (
    ("-",       "-"),
    ("mín.",    "mín."),
    ("máx.",    "máx."),
    ("5%",      "5%"),
    ("8%",      "8%"),
    ("10%",     "10%"),
)

INFORMACION_CHOICES = (
    ("DESCRIPCION",    	"DESCRIPCIÓN"),
    ("CARACTERISTICA", 	"CARACTERÍSTICA"),
    ("RECOMENDACION", 	"RECOMENDACIÓN"),
    ("CONDICION",     	"CONDICIÓN"),
)

CALIFICATIVO_CHOICES = (
    ("APROBADO",    "APROBADO"),
    ("DESAPROBADO", "DESAPROBADO"),
)

ESTADO_CHOICES = (
    ("Anulado",     "Anulado"),
    ("Emitido",     "Emitido"),
    ("Finalizado",  "Finalizado"),
    ("Proceso",     "Proceso"),
)

UNIDAD_CHOICES = (
    ("m",	"metros"),
    ("kg",  "kilogramos"),
)

COLORES = [
    "#d88c9a",
    "#f2d0a9",
    "#f1e3d3",
    "#99c1b9",
    "#8e7dbe",
    "#ffcab1",
    "#69a2b0",
    "#659157",
    "#a1c084",
    "#e05263",
    "#74d3ae",
    "#678d58",
    "#a6c48a",
    "#f6e7cb",
    "#dd9787",
]

REQ_CHOICES = (
    ("Diseño y Desarrollo",	"Diseño y Desarrollo"),
    ("Desarrollo de color", "Desarrollo de color"),
    ("Actualización", 		"Actualización"),
    ("Evaluación", 			"Evaluación"),
)

REQ_SOL_CHOICES = (
    ("Patricia Cipriano",	"Patty"),
    ("Wilkis Lavan", 		"Wilkis"),
    ("Carlos Cabrera", 		"Carlos"),
    ("José Garriazo", 		"Pepe"),
)

REQ_MEDIO_CHOICES = (
    ("Correo", 		"Correo"),
    ("Llamada", 	"Llamada"),
    ("Pedido", 		"Pedido"),
    ("Reunión", 	"Reunión"),
    ("Whatsapp", 	"Whatsapp"),
)

TIPO_DATO = (
    ("TXT", "Texto"),
    ("INT", "Número Entero"),
    ("SEL", "Selección de Opciones"),
    ("BOO", "Sí/No"),
    )