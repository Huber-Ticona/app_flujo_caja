var array_json = [];

$(".contenedor-link").on("click", ".link", function () {
    console.log("cambiando opcion");
    var optionUrl = $(this).data("url"); // obtener la url de la opción seleccionada
    $.ajax({
        url: optionUrl,
        method: "POST",
        success: function (data) {
            // actualizar la segunda columna con el contenido devuelto por la petición
            $(".dashboard-contenido").html(data);
        },
    });
});

$(".dashboard-contenido").on("click", "#datepicker", function () {
    console.log("abriendo pickerdate");
    $("#datepicker").datepicker();
});
$(".dashboard-contenido").on("click", ".add-detalle", function () {
    console.log("añadiendo detalle");
    parcela = $("#input-parcela").val();
    nave = $("#input-nave").val();
    hortaliza = $("#input-hortaliza").val();
    total = $("#input-total").val();

    console.log("parcela: ", parcela);
    console.log("nave: ", nave);
    console.log("total: ", total);

    if (total != "") {
        // crear nuevo objeto JSON
        const nuevoJSON = {
            parcela: parcela,
            nave: nave,
            hortaliza: hortaliza,
            total: parseInt(total),
        };
        // agregar objeto al array
        array_json.push(nuevoJSON);
        actualizar_tabla_embarque();
        actualizar_tabla_2();
    } else {
        alert("ingrese total de gamelas");
    }
});

function actualizar_tabla_embarque() {
    var tabla = $(".body-tabla-embarque");
    tabla.empty(); // Limpia la tabla antes de actualizarla

    // Crea las filas y celdas de la tabla
    for (var i = 0; i < array_json.length; i++) {
        var fila = $("<tr>");
        var parcela = $("<td>").text(array_json[i].parcela);
        var nave = $("<td>").text(array_json[i].nave);
        var hortaliza = $("<td>").text(array_json[i].hortaliza);
        var total = $("<td>").text(array_json[i].total);
        var accion = $("<td>");
        var boton = $("<button>").text("Eliminar");

        // Agrega el evento click al botón para eliminar la fila y el elemento del array JSON
        boton.click(
            (function (index) {
                return function () {
                    array_json.splice(index, 1);
                    actualizar_tabla_embarque(); // Actualiza la tabla después de eliminar la fila
                    actualizar_tabla_2();
                };
            })(i)
        );

        accion.append(boton);
        fila.append(parcela, nave, hortaliza, total, accion);
        tabla.append(fila);
    }
    console.log("array_json: ", array_json);
}

function actualizar_tabla_2() {
    $("#tabla2 tbody").empty();
    let hortalizas = {};
    let dato = array_json;
    // Iteramos sobre el array y agregamos los totales de cada hortaliza al objeto 'hortalizas'
    dato.forEach((dato) => {
        if (!hortalizas[dato.hortaliza]) {
            hortalizas[dato.hortaliza] = dato.total;
        } else {
            hortalizas[dato.hortaliza] += dato.total;
        }
    });
    console.log("hortalizas: ", hortalizas);
    // Creamos las filas de la tabla dinámicamente
    let tbody = $("#tabla2 tbody");
    for (let hortaliza in hortalizas) {
        let fila = $("<tr>");
        $("<td>").text(hortaliza).appendTo(fila);
        $("<td>").text(hortalizas[hortaliza]).appendTo(fila);
        let input = $("<input>")
            .attr("type", "number")
            .val(hortalizas[hortaliza].total_procesado)
            .appendTo($("<td>").appendTo(fila));
        fila.appendTo(tbody);
    }
}

function obtener_datos_totales() {
    let datos_procesados = [];
    $("#tabla2 tbody tr").each(function () {
        let hortaliza = $(this).find("td:first-child").text();
        let total_terreno = Number($(this).find("td:nth-child(2)").text());
        let total_procesado = Number(
            $(this).find("td:nth-child(3) input").val()
        );
        datos_procesados.push({
            hortaliza,
            total_terreno,
            total_procesado,
        });
    });
    console.log(datos_procesados);
    return datos_procesados;
}
// REGISTRAR EMBARQUE
$(".dashboard-contenido").on("click", "#enviar_datos", function () {
    let fecha = $("#datepicker").val();
    let observacion = $("#observacion").val();
    let totales = obtener_datos_totales();

    let extra = {
        observacion: observacion,
    };

    let data = {
        fecha: fecha,
        detalle: array_json,
        detalle_totales: totales,
        extra: JSON.stringify(extra),
    };

    console.log("data", data);
    data = JSON.stringify(data);
    console.log("data stringfy", data);

    $.ajax({
        type: "POST",
        url: "/embarque/registrar",
        contentType: "application/json; charset=utf-8",
        success: function (res) {
            if (res.exito) {
                console.log(res.msg);
                $(".dashboard-contenido").empty();
                array_json = [];
                toastr.success(res.msg, res.title, { timeOut: 3000 });
            } else {
                console.log(res.msg);
                toastr.error(res.msg, res.title, { timeOut: 3000 });
            }
        },
        data: data,
    });
});

// FUNCIONES PARA COMPONENTES LIQUIDACION
var array_json_liquidacion = [];
var datos_csv = [];

// Cargar CSV
$(".dashboard-contenido").on("click", "#enviar_csv", function (event) {
    console.log("enviando csv ...");
    event.preventDefault();
    var archivo_csv = $("#csv-file")[0].files[0];
    var formData = new FormData();
    formData.append("csv-file", archivo_csv);
    $.ajax({
        url: "/subir_csv",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (res) {
            // maneja la respuesta del servidor  `res`
            if (res.exito) {
                console.log(res.msg);
                datos_csv = res.datos;
                array_json_liquidacion = res.tabla;
                console.log("-------- array json ------ ", res.tabla);
                console.log("-------- datos csv ------ ", res.datos);

                toastr.success(res.msg, res.title, { timeOut: 3000 });
            } else {
                console.log(res.msg);
                toastr.error(res.msg, res.title, { timeOut: 3000 });
            }
        },
    });
});
// RELLENAR DATOS LIQUIDACION DESDE CSV.
$(".dashboard-contenido").on("click", "#rellenar_datos", function () {
    console.log("Rellenando datos");
    console.log("datos_csv", datos_csv);

    for (var i = 0; i < array_json_liquidacion.length; i++) {
        let item = array_json_liquidacion[i];
        crear_fila_liquidacion(item);
    }
    if (datos_csv.length > 0) {
        // [ nro_guia ,fecha ,total_neto_guia, total_venta, comision,flete_ari_stgo ,flete_stgo_ari,TOTAL DESCUENTOS, TOTAL A PAGAR ] ]
        $("#nro_guia").val(datos_csv[0]);
        // Convertir la fecha al formato yyyy-MM-dd
        let fecha_formateada =
            "20" + datos_csv[1].split("-").reverse().join("-");
        // Asignar la fecha formateada al input
        $("#fecha").val(fecha_formateada);
        $("#total_neto_guia").val(datos_csv[2]);
        $("#total_venta").val(datos_csv[3]);
        $("#comision").val(datos_csv[4]);
        $("#flete_ari_stgo").val(datos_csv[5]);
        $("#flete_stgo_ari").val(datos_csv[6]);
        $("#total_descuento").val(datos_csv[7]);
        $("#total_pago").val(datos_csv[8]);
        $("#total_bulto").val(datos_csv[9]);
        $("#desc_x_bulto").val(datos_csv[10]);
    }
});

// Agregar fila.
$(".dashboard-contenido").on("click", "#btn-add-item", function () {
    console.log("Añadiendo fila -...");
    let data = {
        cantidad: "0",
        iva_guia: "0",
        neto: "0",
        precio: "0",
        precio_venta: "0",
        producto: "TOMATE CALIBRE ",
        total: "0",
        p_guia: "0",
        total_neto: "0",
        desc_aplicado: "0",
    };
    crear_fila_liquidacion(data);
});

// Crear fila tabla liquidacion.
function crear_fila_liquidacion(dato) {
    var tabla_liquidacion = $(".body-tabla-liquidacion");
    var numeroDeFilas = tabla_liquidacion.find("tr").length;

    console.log("Número de filas en la tabla: " + numeroDeFilas);

    var i = numeroDeFilas;
    var tabla_liquidacion = $(".body-tabla-liquidacion");

    var fila = $("<tr>");

    var productoInput = $("<input>")
        .attr("type", "text")
        .val(dato.producto)
        .addClass("input-text-table-liquidacion producto-lq");
    var cantidadInput = $("<input>")
        .attr("type", "number")
        .val(dato.cantidad)
        .addClass("input-table-liquidacion cantidad-lq");
    var precioVentaInput = $("<input>")
        .attr("type", "number")
        .val(dato.precio_venta)
        .addClass("input-table-liquidacion precioventa-lq");
    var netoInput = $("<input>")
        .attr("type", "number")
        .val(dato.neto)
        .addClass("input-table-liquidacion neto-lq");
    var ivaGuiaInput = $("<input>")
        .attr("type", "number")
        .val(dato.iva_guia)
        .addClass("input-table-liquidacion ivaguia-lq");
    var precioInput = $("<input>")
        .attr("type", "number")
        .val(dato.precio)
        .addClass("input-table-liquidacion precio-lq");
    var totalInput = $("<input>")
        .attr("type", "number")
        .val(dato.total)
        .addClass("input-table-liquidacion total-lq");
    var p_guia_input = $("<input>")
        .attr("type", "number")
        .val(dato.p_guia)
        .addClass("input-table-liquidacion p_guia-lq");
    var total_neto_input = $("<input>")
        .attr("type", "number")
        .val(dato.total_neto)
        .addClass("input-table-liquidacion total_neto-lq");
    var desc_aplicado_input = $("<input>")
        .attr("type", "number")
        .val(dato.desc_aplicado)
        .addClass("input-table-liquidacion desc_aplicado-lq");
    var boton = $("<button>")
        .text("Eliminar")
        .addClass("btn-remover-fila-liquidacion");

    fila.append(
        $("<td>").append(productoInput),
        $("<td>").append(cantidadInput),
        $("<td>").append(precioVentaInput),
        $("<td>").append(netoInput),
        $("<td>").append(ivaGuiaInput),
        $("<td>").append(precioInput),
        $("<td>").append(totalInput),
        $("<td>").append(p_guia_input),
        $("<td>").append(total_neto_input),
        $("<td>").append(desc_aplicado_input),
        $("<td>").append(boton)
    );

    tabla_liquidacion.append(fila);
}
// Funcion para obtener el Array de JSON de la tabla liquidaciones.
function obtenerDatosDeTablaLiquidacion() {
    var datos = []; // Aquí almacenaremos los objetos JSON

    // Itera sobre las filas de la tabla
    $(".body-tabla-liquidacion tr").each(function () {
        var fila = $(this);
        var producto = fila.find(".producto-lq").val();
        var cantidad = fila.find(".cantidad-lq").val();
        var precioVenta = fila.find(".precioventa-lq").val();
        var neto = fila.find(".neto-lq").val();
        var ivaGuia = fila.find(".ivaguia-lq").val();
        var precio = fila.find(".precio-lq").val();
        var total = fila.find(".total-lq").val();
        var p_guia = fila.find(".p_guia-lq").val();
        var total_neto = fila.find(".total_neto-lq").val();
        var desc_aplicado = fila.find(".desc_aplicado-lq").val();

        // Crea un objeto JSON con los valores de la fila
        var filaJSON = {
            producto: producto,
            cantidad: cantidad,
            precio_venta: precioVenta,
            neto: neto,
            iva_guia: ivaGuia,
            precio: precio,
            total: total,
            p_guia: p_guia,
            total_neto: total_neto,
            desc_aplicado: desc_aplicado,
        };

        // Agrega el objeto JSON al array
        datos.push(filaJSON);
    });
    console.log("DETALLE: ", datos);
    return datos;
}
$(".dashboard-contenido").on(
    "click",
    ".btn-remover-fila-liquidacion",
    function () {
        // Encuentra el elemento padre <tr> de este botón y elimínalo
        console.log("eliminando fila liqidacion.");
        $(this).closest("tr").remove();
    }
);
// REGISTRAR DATOS LIQUIDACION
$(".dashboard-contenido").on("click", "#registrar_liquidacion", function () {
    let liquidacion_id = $(this).data("liquidacion_id");
    let url = "";
    let mode = "registro";
    if (typeof liquidacion_id === "undefined") {
        // La variable es undefined
        console.log("La variable es undefined. MODO REGISTRO");
        url = "/liquidacion/registrar";
    } else {
        // La variable tiene un valor
        console.log("La variable no es undefined. MODO UPDATE");
        url = "/liquidacion/actualizar/" + liquidacion_id.toString();
        mode = "update";
    }

    console.log("LIQUIDACION ID: ", liquidacion_id);
    console.log("------- INICIANDO " + mode + " liquidacion ------- ");
    let fecha = $("#fecha").val();
    let detalle = obtenerDatosDeTablaLiquidacion();
    let detalles_extras = {
        total_neto_guia: parseInt($("#total_neto_guia").val()),
        comision: parseInt($("#comision").val()),
        flete_ari_stgo: parseInt($("#flete_ari_stgo").val()),
        flete_stgo_ari: parseInt($("#flete_stgo_ari").val()),
        nro_guia: $("#nro_guia").val(),
        vendedor: $("#input-vendedor").val(),
        comentario: $("#input-comentario").val(),
        total_bulto: parseInt($("#total_bulto").val()),
        desc_x_bulto: parseInt($("#desc_x_bulto").val()),
    };

    console.log("detalles extras", detalles_extras);
    let total_venta = parseInt($("#total_venta").val());
    let total_descuento = parseInt($("#total_descuento").val());
    let total_pago = parseInt($("#total_pago").val());

    let data = JSON.stringify({
        fecha: fecha,
        detalle: detalle,
        detalles_extras: detalles_extras,
        total_venta: total_venta,
        total_descuento: total_descuento,
        total_pago: total_pago,
    });
    console.log("DATOS LIQUIDACION", data);
    console.log(fecha);
    console.log(total_venta);
    console.log(total_descuento);
    console.log(total_pago);

    if (
        fecha == "" ||
        isNaN(total_venta) ||
        isNaN(total_descuento) ||
        isNaN(total_pago)
    ) {
        console.log("RELLENE TODOS LOS DATOS..");
        alert("RELLENE TODOS LOS DATOS.");
    } else {
        console.log("------- " + mode + " LIQUIDACION ... ----------");

        $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json; charset=utf-8",
            data: data,
            success: function (res) {
                if (res.exito) {
                    console.log(res.msg);
                    $(".dashboard-contenido").empty();
                    array_json_liquidacion = [];
                    toastr.success(res.msg, res.title, { timeOut: 3000 });
                } else {
                    console.log(res.msg);
                    toastr.error(res.msg, res.title, { timeOut: 3000 });
                }
            },
        });
    }
});

//
$(".dashboard-contenido").on("click", ".btn-mod-lq", function () {
    let id = $(this).data("id");
    console.log("modificar liquidacion id: ", id);
    $(".dashboard-contenido").html("<hi1>hola</hi1>");
    url = "/liquidacion/actualizar/" + id.toString();
    $.ajax({
        url: url,
        method: "GET",
        success: function (data) {
            // actualizar la segunda columna con el contenido devuelto por la petición
            $(".dashboard-contenido").html(data);
        },
    });
});
