
import csv

def formato2(texto):
    """ Da formato: 
    TOTAL NETO;1451261
$ TOTAL;1806941
10 % COMISION;145126
FLETE ARI-STGO;391200
FLETE STGO-ARI;0
TOTAL DESCUENTOS;536326
TOTAL A PAGAR;1270614

*ahi que agregar un doble espacio al final del .txt 
para que lea la cantidad exacta de 14 lineas*
"""
    with open(texto, 'r') as f:
        lines = f.readlines()
    # print(len(lines))

    text_list = []
    text = ''
    incr = 0
    j = 0  # cambio de fila
    for i in range(len(lines)):
        if incr < 3:  # 13 lineas
            if i % 2 == 0:
                if j == 0:  # Comienzo del armado
                    x = lines[i].strip()
                    # print(f'index comienzo: {str(i)} | x: {x}  | incr: {incr}')
                    text = x
                    j = 1
                else:

                    x = lines[i].strip().replace('$', '').replace('.', '')
                    # print(f'index cuerpo: {str(i)} | x: {x}  | incr: {incr}')
                    text = text + ';' + x
            incr += 1
        else:
            # print(text)
            # print('13 lineas leidas , volviendo a crear el texto')
            text_list.append(text)
            # print(f'index end: {str(i)} | x: {x}')
            j = 0
            incr = 0
            text = ''
    print(text_list)
    return text_list


def formato1(txt_file):
    """ Da formato: """
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    #print(len(lines))
    lista_text = []
    text = ''
    j = 0
    incr = 0
    for i in range(len(lines)):

        if incr < 13:  # 13 lineas
            if i % 2 == 0:
                if j == 0:  # Comienzo del armado
                    x = lines[i].strip()
                    #print(f'index comienzo: {str(i)} | x: {x}  | incr: {incr}')
                    text = x
                    j = 1
                else:

                    x = lines[i].strip().replace('$', '').replace('.', '')
                    #print(f'index cuerpo: {str(i)} | x: {x}  | incr: {incr}')
                    text = text + ';' + x
            incr += 1
        else:
            print(text)
            #print('13 lineas leidas , volviendo a crear el texto')
            x = lines[i].strip()
            #print(f'index end: {str(i)} | x: {x}')
            j = 0
            incr = 0
            text = ''
    return lista_text

def formato_combinado(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    lista1 = []
    lista2 = []
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        if i<3:
            texto = lines[i].split('\t')
            if i == 0:
                guia = texto[1]
            print('Seccion 0: ' , texto)
            lista1.append([texto[i] for i in range(2)])

        elif i<12:
            print(f'i:{i} | ',lines[i])
            texto = lines[i].split('\t')
            texto[1]= (texto[1].replace('$','').replace('.','')).strip()
            print('Seccion 1: ' ,texto)
            lista1.append([texto[i] for i in range(2)])
        elif i>=12 and len(lines[i].split('\t')) == 7:
            print(f'i:{i} | ',lines[i])
            texto = lines[i].split('\t')
            texto = [ (i.replace('$','').replace('.','')).strip() for i in texto]
            if texto[6] != '0' and texto[6] != '':
                print(f'len:6 | {texto[6]} | Seccion 2: ' ,texto)
                lista2.append(texto)
        else: print('extra')
    
    #modificaciones
    lista1.pop(1)
    lista1 = swapPositions(lista1, 2, 3)
    lista1.pop(8) #total - total descuentos
    lista1.pop(8) # abono mm
    print('lista1:' ,lista1)
    print('lista2:', lista2)
    
    # GUARDAR CSV
    # Nombre del archivo CSV que deseas crear
    nombre_archivo = r'C:\Users\super\Desktop\proyectos_python\app-flujo-caja\liquidaciones\2020\liquidacion_guia_'+guia+'.csv'
    with open(nombre_archivo, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        
        # Escribir los datos de la lista1 en el archivo CSV
        for lista in lista1:
            writer.writerow(lista)

        for lista in lista2:
            writer.writerow(lista)

    print(f'LIQUIDACION GUIA {guia}: -> csv creado')
    return 0

def swapPositions(list, pos1, pos2):

    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


if __name__ == '__main__':
    texto_tabla = "liquidaciones/libro1.txt"
    montos = 'liquidaciones/libro2.txt'
    #a = formato_combinado(texto_tabla)
    j = formato2(montos)
    x = swapPositions(j, 0, 1)
    for i in x:
        print(i)
    y = formato1(texto_tabla)
 