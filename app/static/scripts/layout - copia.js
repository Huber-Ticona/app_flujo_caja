var array_json = [];

$("#open-sidebar").click(function () {
  console.log("activando_sidebar");
  $(".sidebar-wrapper").addClass("hide");
});
$("#close-sidebar").click(function () {
  console.log("desactivando_sidebar");
  $(".sidebar-wrapper").removeClass("hide");
});

$(".contenedor-link").on("click", ".link", function () {
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
    let total_procesado = Number($(this).find("td:nth-child(3) input").val());
    datos_procesados.push({
      hortaliza,
      total_terreno,
      total_procesado,
    });
  });
  console.log(datos_procesados);
  return datos_procesados;
}

$(".dashboard-contenido").on("click", "#enviar_datos", function () {
  let fecha = $("#datepicker").val();
  let observacion = $("#observacion").val();
  let totales = obtener_datos_totales();
  let data = {
    fecha: fecha,
    detalle: array_json,
    detalle_totales: totales,
    observacion: observacion,
  };
  console.log("data", data);
  data = JSON.stringify(data);
  console.log("data stringfy", data);

  $.ajax({
    type: "POST",
    url: "/parcela/embarque/registrar",
    contentType: "application/json; charset=utf-8",
    success: function (msg) {
      console.log(msg);
    },
    data: data,
  });
});
