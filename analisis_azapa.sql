-- select sum(json_extract(detalle_totales, "$[0].total_procesado")) from embarque order by fecha desc
-- select * from periodo

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
)
-- ANALISIS EMBARQUE 
-- 1. TOTAL DE GAMELAS PRODUCIDAS POR PERIODO,PARCELA Y NAVE.
-- select p.periodo_fiscal,v.periodo_id, v.parcela, sum(v.total) from vista_embarque v  inner join periodo p on v.periodo_id = p.periodo_id
-- group by periodo_id ,parcela
 

-- ANALISIS LIQUIDACIONES 
-- select * from vista_liquidacion

-- 1. Total ventas por periodo(año)
-- select periodo_id, CONCAT('$', FORMAT(sum(total_venta), 2)) as total_venta, CONCAT('$', FORMAT(sum(total_pago), 2)) as total_pago from liquidacion group by periodo_id
-- 2. LISTAR DETALLES X PRODUCTO ESPECIFICO
-- select LIQUIDACION_ID,producto,cantidad,neto,PRECIO,TOTAL from vista_liquidacion where producto = 'ROJO I'
-- 3. RESUMEN PERIODO -> PRODUCTO,CANTIDAD , TOTAL
 -- select periodo_id,producto,sum(cantidad) ,CONCAT('$', FORMAT(sum(total), 1)) as total from vista_liquidacion group by producto
-- select * from liquidacion where json_extract(detalle,'$.producto') = 'TOMATE CALIBRE 75'
-- SELECT * FROM liquidacion WHERE JSON_CONTAINS(detalle, '{"producto": "TOMATE CALIBRE 75"}');
-- select * from liquidacion
UPDATE liquidacion SET detalle = JSON_REPLACE(detalle, '$[*].producto', 'TOMATE CALIBRE 7.5') WHERE detalle->"$[*].producto" = 'TOMATE CALIBRE 75';
