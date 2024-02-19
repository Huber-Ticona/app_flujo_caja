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
