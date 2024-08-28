-- show tables; select * from cosecha 
-- update empresa set parametros = JSON_OBJECT() where empresa_id = 5
-- describe movimiento
 -- insert into movimiento(fecha) values ('2024-01-01' ) select * from movimiento
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
SELECT l.id,l.fecha ,l.lugar, l.nave ,l.comentario, d.*,
    CASE
      WHEN d.unidad_de_total IN ('kilogramo (KG)', 'Litro (LTS)') THEN d.total_aplicado
      WHEN d.unidad_de_total = 'Mili-litro (ML)' THEN d.total_aplicado / 1000
      WHEN d.unidad_de_total = 'Mili-gramo (MG)' THEN d.total_aplicado / 1000
      ELSE NULL
    END AS total_kg_lt
FROM aplicacion l
CROSS JOIN JSON_TABLE(l.detalle, '$[*]' COLUMNS (
    insumo VARCHAR(255) PATH '$.insumo',
    total_aplicado float PATH '$.total_aplicado',
    unidad_de_total varchar(255) PATH '$.unidad_de_total'
)) d
-- where periodo_id = 3
),
vista_gasto as (
SELECT g.periodo_id,g.id,g.fecha,g.prov_empresa,g.prov_documento, d.* 
FROM gasto g 
CROSS JOIN JSON_TABLE(g.detalle, '$[*]' COLUMNS(
	unidad varchar(255) path '$.unidad',
    cantidad int path '$.cantidad',
	descripcion VARCHAR(255) PATH '$.descripcion',
    precio_unitario int path '$.precio_unitario',
    precio_total int path '$.precio_total',
    tipo varchar(255) path '$.tipo'
)) d
-- group by d.descripcion
order by g.fecha desc
)
,vista_cosecha as (
SELECT c.periodo_id,c.id,c.fecha,c.lugar,c.nave, d.* 
FROM cosecha c 
CROSS JOIN JSON_TABLE(c.detalle, '$[*]' COLUMNS(
	hortaliza varchar(255) path '$.hortaliza',
    calibre int path '$.calibre',
	unidad VARCHAR(255) PATH '$.unidad',
    cantidad int path '$.cantidad'
)) d
-- group by d.descripcion
order by g.fecha desc
)
/* ANALISIS EMBARQUE */
-- SELECT * FROM EMBARQUE
-- select * from vista_embarque where hortaliza != "Tomate Bola"
-- select distinct(hortaliza) from vista_embarque
-- 1. TOTAL DE GAMELAS PRODUCIDAS POR PERIODO,PARCELA Y NAVE.
--  select p.periodo_fiscal,v.periodo_id, v.parcela, sum(v.total) from vista_embarque v  inner join periodo p on v.periodo_id = p.periodo_id group by periodo_id ,parcela
-- select sum(json_extract(detalle_totales, "$[0].total_procesado")) from embarque where periodo_id = 7 order by fecha desc
 
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
-- select * from vista_aplicacion
-- 1. Calcular total de aplicaciones de insumos de medida KG o LT
--  select v.*, sum(total_kg_lt) from vista_aplicacion v where v.unidad_de_total in ('kilogramo (KG)' ,'Litro (LTS)') group by insumo 
-- select v.*, sum(total_kg_lt) from vista_aplicacion v  group by insumo 
-- select * from vista_aplicacion v where v.unidad_de_total in ("Mili-litro (ML)", "Mili-litro (ML)")
-- (TOOLS) Convertir las unidades ML, MG a KG , LTS
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
 -- select * from gasto where fecha > "2024-03-01" order by fecha asc
 
-- select * from vista_gasto
-- 1. LISTA DE GASTOS PRODUCTO AGRUPADO -> DESCRIPCION DE PRODUCTO, UNIDAD, SUMA(CANTIDAD), PRECIO_UNITARIO(? o promedio) ,SUMA(PRECIO_TOTAL) 
select fecha,descripcion , unidad, sum(cantidad), precio_unitario, sum(precio_total) from vista_gasto where tipo = 'fertilizante' group by descripcion
-- 1.1 BUSCAR UN GASTO EN LISTA DE GASTOS POR PRODUCTO AGRUPADOO (algunso repetidos por causa de espacios en blancos, solucion strip.)
-- select fecha,descripcion , unidad, sum(cantidad), precio_unitario, sum(precio_total) from vista_gasto where descripcion like '%natu%' group by descripcion
-- 1.2 BUSCAR TODOS LOS GASTOS POR PRODUCTO  
-- select fecha,descripcion , unidad, cantidad, precio_unitario, precio_total from vista_gasto where descripcion like '%liqui%'  -- group by descripcion
-- select  id, fecha, descripcion , cantidad,precio_unitario, SUM(cantidad) OVER (ORDER BY cantidad ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_cantidad  FROM vista_gasto where descripcion like '%%' GROUP BY id ;
-- 2.0 CALCULAR GASTO TOTAL X PERIODO U OTROS
-- select CONCAT('$', FORMAT(sum(total), 1)) as total  from gasto where periodo_id = 7
-- 2.1 CALCULAR GASTO TOTAL X PERIODO X tipo | incluye boletas.? revisar
-- select tipo,sum(precio_total),CONCAT('$', FORMAT(sum(precio_total), 1)) as neto , CONCAT('$', FORMAT(sum(precio_total)*1.19, 1)) as con_iva from vista_gasto where periodo_id = 7 group by tipo WITH ROLLUP
-- select * ,CONCAT('$', FORMAT(sum(precio_total*1.19), 1)) as bruto   from vista_gasto where prov_documento = "boleta" group by tipo with rollup

-- select SUM(cantidad) , descripcion , CONCAT('$', FORMAT(sum(precio_total), 1)) from vista_gasto where tipo = "FERTILIZANTE" group by DESCRIPCION
