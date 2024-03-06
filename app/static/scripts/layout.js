/* COMPONENT SIDEBAR */
var open_sidebar = false;
$("#menu").on("click", function () {
    console.log("abriendo main sidebar");
    $(".main-sidebar").addClass("active");
    $(".fondo_oscuro").addClass("sidebar-open");
});

$("#menu-btn").on("click", function () {
    if (open_sidebar) {
        open_sidebar = false;
        console.log("cerrando sidebar");
        $(".sidebar").removeClass("active");
        $(".fondo_oscuro").removeClass("sidebar-open");
    } else {
        open_sidebar = true;
        console.log("open sidebar");
        $(".sidebar").addClass("active");
        $(".fondo_oscuro").addClass("sidebar-open");
    }
});

$(".fondo_oscuro").click(function () {
    open_sidebar = false;
    $(".sidebar").removeClass("active");
    $(".main-sidebar").removeClass("active");
    $(".fondo_oscuro").removeClass("sidebar-open");
});
/* END SIDEBAR */

/* CONTROL ACTIVE CLASS ON MAIN_SIDEBAR */
$(".main_sidebar").on("click", ".custom-item", function (event) {
    /* console.log("item seleccionado: ", $(this));
    console.log("text: ", $(this).html());
 */
    $(this).addClass("active").siblings().removeClass("active");
});

/* htmx.on("eliminar_registro", (e) => {
    const toastElement = document.getElementById("toast");
    const toastBody = document.getElementById("toast-body");
    const toast = new bootstrap.Toast(toastElement, { delay: 2000 });

    console.log("evento: eliminar_registro");
    console.log("detail: ", e.detail);
    toastBody.innerText = e.detail.msg;
    console.log("ID recibido: ", e.detail.id);
    // Encuentra la fila con el mismo ID y la elimina
    $("#cuerpo-tabla")
        .find("tr#" + e.detail.id)
        .remove();
    $("#toast").addClass(e.detail.class);
    toast.show();
}); */

/* overflow-y: scroll;
scrollbar-color: red  #3b3b42 ;
scrollbar-width: auto; */
