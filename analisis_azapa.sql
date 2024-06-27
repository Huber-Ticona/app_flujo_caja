-- show tables;
-- use test_app_flujo
-- use app_flujo_caja
-- truncate alembic_version
-- select @@version 
with vista_embarque as (
SELECT e.periodo_id,e.fecha, d.*
FROM embarque e
CROSS JOIN JSON_TABLE(e.detalle, '$[*]' COLUMNS (
    nave VARCHAR(255) PATH '$.nave',
    total INT PATH '$.total',
    parcela VARCHAR(255) PATH '$.parcela',
    hortaliza VARCHAR(255) PATH '$.hortaliza'
)) d
-- where periodo_id = 5
ORDER BY e.fecha
),
 vista_liquidacion as (
SELECT l.periodo_id,l.liquidacion_id ,l.fecha, d.*
FROM liquidacion l
CROSS JOIN JSON_TABLE(l.detalle, '$[*]' COLUMNS (
    producto VARCHAR(255) PATH '$.producto',
    cantidad INT PATH '$.cantidad',
    precio_venta VARCHAR(255) PATH '$.precio_venta',
    neto VARCHAR(255) PATH '$.neto',
    precio VARCHAR(255) PATH '$.precio',
    total VARCHAR(255) PATH '$.total'
)) d
-- where periodo_id = 3
),
vista_aplicacion as (
SELECT l.id,l.fecha ,l.lugar, l.nave ,l.comentario, d.*
FROM aplicacion l
CROSS JOIN JSON_TABLE(l.detalle, '$[*]' COLUMNS (
    insumo VARCHAR(255) PATH '$.insumo',
    total_aplicado float PATH '$.total_aplicado',
    unidad_de_total varchar(255) PATH '$.unidad_de_total'
)) d
-- where periodo_id = 3
),
vista_gasto as (
SELECT g.fecha, d.* 
FROM gasto g 
CROSS JOIN JSON_TABLE(g.detalle, '$[*]' COLUMNS(
	unidad varchar(255) path '$.unidad',
    cantidad int path '$.cantidad',
	descripcion VARCHAR(255) PATH '$.descripcion',
    precio_unitario int path '$.precio_unitario',
    precio_total int path '$.precio_total'
)) d
)
/* ANALISIS EMBARQUE */
-- SELECT * FROM EMBARQUE
-- 1. TOTAL DE GAMELAS PRODUCIDAS POR PERIODO,PARCELA Y NAVE.
 select p.periodo_fiscal,v.periodo_id, v.parcela, sum(v.total) from vista_embarque v  inner join periodo p on v.periodo_id = p.periodo_id group by periodo_id ,parcela
-- select sum(json_extract(detalle_totales, "$[0].total_procesado")) from embarque order by fecha desc
 
/* ANALISIS LIQUIDACIONES  */ 
-- select * from vista_liquidacion

-- 1. Total ventas por periodo(año)
-- select periodo_id, CONCAT('$', FORMAT(sum(total_venta), 2)) as total_venta, CONCAT('$', FORMAT(sum(total_pago), 2)) as total_pago from liquidacion group by periodo_id
-- 2. LISTAR DETALLES X PRODUCTO ESPECIFICO
 -- select LIQUIDACION_ID,producto,cantidad,neto,PRECIO,TOTAL from vista_liquidacion where producto = 'TOMATE CALIBRE 8' and periodo_id = 5
-- 3. RESUMEN PERIODO -> PRODUCTO,CANTIDAD , TOTAL
-- select periodo_id,producto,sum(cantidad) ,CONCAT('$', FORMAT(sum(total), 1)) as total from vista_liquidacion group by producto

-- (TOOLS)
-- (UPDATE permite usar json_set, json_replace y json_remove , SELECT no lo permite y * o ** tampoco)
-- SELECT liquidacion_id, JSON_SET(detalle , '$[0].producto' , 'test') AS detalle_modificado FROM liquidacion WHERE liquidacion_id = 59 
-- SELECT liquidacion_id, JSON_REPLACE(detalle, '$[*].producto', 'test') AS detalle_modificado FROM liquidacion WHERE liquidacion_id = 59
-- select * from liquidacion where json_extract(detalle,'$.producto') = 'TOMATE CALIBRE 75'
-- SELECT * FROM liquidacion WHERE JSON_CONTAINS(detalle, '{"producto": "TOMATE CALIBRE 75"}');
-- select * from liquidacion
-- UPDATE liquidacion SET detalle = JSON_REPLACE(detalle, '$[*].producto', 'TOMATE CALIBRE 7.5') WHERE detalle->"$[*].producto" = 'TOMATE CALIBRE 75';


/* ANALISIS APLICACION */

-- select * from aplicacion
-- select * from vista_aplicacion v where v.unidad_de_total in ("Mili-litro (ML)", "Mili-litro (ML)")
-- 1. Convertir las unidades ML, MG a KG , LTS
/* select v.* ,
case
	when v.unidad_de_total IN  ('kilogramo (KG)' ,'Litro (LTS)') then (v.total_aplicado)
    when v.unidad_de_total = 'Mili-litro (ML)' then (v.total_aplicado/1000)
    when v.unidad_de_total = 'Mili-gramo (MG)' then (v.total_aplicado/1000)
end as total_final,
case 
	when v.unidad_de_total = 'Mili-litro (ML)' then 'kilogramo (KG)'
    when v.unidad_de_total = 'Mili-gramo (MG)' then 'Litro (LTS)'
    ELSE v.unidad_de_total
end as unidad_final from vista_aplicacion v  */

/* ANALISIS GASTO */
-- select * from vista_gasto
-- select * from gasto
-- 1. LISTA DE GASTOS PRODUCTO AGRUPADO -> DESCRIPCION DE PRODUCTO, UNIDAD, SUMA(CANTIDAD), PRECIO_UNITARIO(? o promedio) ,SUMA(PRECIO_TOTAL) 
-- select fecha,descripcion , unidad, sum(cantidad), precio_unitario, sum(precio_total) from vista_gasto group by descripcion
-- 1.1 BUSCAR UN GASTO EN LISTA DE GASTOS POR PRODUCTO AGRUPADOO (algunso repetidos por causa de espacios en blancos, solucion strip.)
-- select fecha,descripcion , unidad, sum(cantidad), precio_unitario, sum(precio_total) from vista_gasto where descripcion like '%natu%' group by descripcion
-- 2. BUSCAR TODOS LOS GASTOS POR PRODUCTO  
-- select fecha,descripcion , unidad, cantidad, precio_unitario, precio_total from vista_gasto where descripcion like '%natu%' -- group by descripcion

-- 2. CALCULAR GASTO TOTAL X PERIODO U OTROS
-- select CONCAT('$', FORMAT(sum(total), 1)) as total  from gasto where periodo_id = 7
-- 3. LISTAR GASTOS POR TIPO DE GASTO AGRUPADO
-- select v.tipo, sum(total) ,CONCAT('$', FORMAT(sum(total), 1)) as total  from gasto v group by v.tipo


