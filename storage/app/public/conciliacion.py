#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from os.path import exists
import xlsxwriter
import pandas as pd
import sys
import re
pd.options.mode.chained_assignment = None  # default='warn'

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

periodo_mes = ""

def ingresos_egresos_sigep(general_sigep_dataframe, colsInicial, tipo):
    global periodo_mes
    values = general_sigep_dataframe[colsInicial[2]] == tipo
    values = general_sigep_dataframe[values]
    mon = pd.DatetimeIndex(values[colsInicial[3]])
    values['Periodo'] = mon.month
    periodo_mes = meses[int(mon.month[0])]
    cols = values.columns.tolist()
    cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
    values = values[cols]
    ref = values[cols[0]].astype('int64')
    values.update(ref)
    values['Formula'] = 0
    values['Diferencia'] = 0
    values['Observaciones'] = 0
    values['valida'] = 0
    
    return values

def fomulaSSValida(original, file, cols):
    for index0, row0 in file.iterrows():
        sumaSS = 0
        salud = 0
        value = original[cols[0]] == row0[cols[0]]
        value = original[value]
        suma = value[cols[1]].sum()
        for index1, row1 in file.iterrows():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            if(row0[cols[0]] == row1[cols[0]]):
                sumaSS = sumaSS + abs(row1[cols[1]])
        salud = round(sumaSS * porcentaje_salud,1)
        file.loc[index0, 'SS'] = salud
        diferenciaSigepSapSeguridadSocial = abs(row0['Formula']) - (suma + int(round(sumaSS * porcentaje_salud)))
        if(diferenciaSigepSapSeguridadSocial == -1) | (diferenciaSigepSapSeguridadSocial == 1):
            file.loc[index0, 'valida'] = 0
            value['valida'] = 0
        else:
            file.loc[index0, 'valida'] = diferenciaSigepSapSeguridadSocial
            value['valida'] = diferenciaSigepSapSeguridadSocial
        original.update(value)

def valorFormulaDiferencia(fileOne, fileTwo):
    colC = fileOne.columns.tolist()
    colT = fileTwo.columns.tolist()
    for index, row in fileOne.iterrows():
        value = (fileTwo[colT[0]] == row[colC[0]]) & (fileTwo[colT[6]] == row[colC[6]])
        value = fileTwo[value]
        suma = value[colT[1]].sum()
        fileOne.loc[index,'Formula'] = suma
        dif = row[colC[1]] - abs(suma)
        fileOne.loc[index,'Diferencia'] = dif
        #Suma iguales valores del archivo base
        value = (fileOne[colC[0]] == row[colC[0]]) & (fileOne[colC[6]] == row[colC[6]])
        value = fileOne[value]
        value = value[colC[1]].sum()
        fileOne.loc[index, 'valida'] = abs(suma) - abs(value)

def style(item, row, col, worksheet, cont, format, seguridad, posgrados, posgradosPagos, enPos, negRecaudos, date, normal_valor):
    recaudo_positivo = workbook.add_format({'fg_color':'#FFE699'})
    recaudo_positivo_money = workbook.add_format({'fg_color':'#FFE699', 'num_format': '#,##0'})
    recaudo_positivo_date = workbook.add_format({'fg_color':'#FFE699', 'num_format': 'mm/dd/yyyy'})
    if(item == 1):
        if(float(row[col[1]])) > 0:
            worksheet.set_row(cont,None, recaudo_positivo)
            worksheet.write(cont, 1,  row[col[1]], recaudo_positivo_money)
            worksheet.write(cont, len(col)-4, '=SUMIFS(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,@Recaudos_SAP!G:G)', recaudo_positivo_money)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), recaudo_positivo_money)
            worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), recaudo_positivo_date)
            worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), recaudo_positivo_date)
        else:
            negRecaudos.append('B'+str(cont+1))
            worksheet.write(cont, 1,  row[col[1]], format)
            worksheet.write(cont, len(col)-4, '=SUMIFS(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,@Recaudos_SAP!G:G)', format)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), format)
            worksheet.write(cont, 4, row[col[4]], normal_valor)
            worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), date)
            worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), date)
        
        if(enPos == True):
            if(str(row[col[0]]).lower()[0:4] == '4200'):
                valueP = 0
                if(row[col[0]] in posgrados):
                    valueP = posgrados[row[col[0]]]
                    valueP = valueP + ['B'+str(cont+1)]
                    posgrados[row[col[0]]] = valueP
                    if(float(row[col[1]])) > 0:
                        worksheet.write(cont, len(col)-3, '', recaudo_positivo.set_num_format('#,##0'))
                    else:
                        worksheet.write(cont, len(col)-3, '', format)
    elif(item == 2):
        worksheet.write(cont, 11, '=SUMIFS(Recaudos_SAP!B:B,Recaudos_SAP!A:A,Ingresos_SIGEP!A'+str(cont+1)+',Recaudos_SAP!G:G,@Ingresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-ABS(L'+str(cont+1)+')', format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]].split()[0], '%Y-%m-%d'), date)
    elif(item == 3):
        worksheet.write(cont, len(col)-5, '=SUMIFS(Egresos_SIGEP!B:B,Egresos_SIGEP!A:A,Pagos_SAP!A'+str(cont+1)+',Egresos_SIGEP!G:G,@Pagos_SAP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, len(col)-4, '=B'+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(cont+1), format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), date)
        worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), date)
        value = 0
        if(str(row[col[12]]).lower()[0:8] == 'docentes') & (str(row[col[4]]).lower()[0:3] == 'men') & ((str(row[col[4]]).lower().strip()[-1] == '1') | (str(row[col[4]]).lower().strip()[-1] == '3')):
            if not seguridad.empty:
                value = seguridad[row[col[0]]]
                value = value + ['B'+str(cont+1)]
                seguridad[row[col[0]]] = value
        
        if(enPos == True):
            if(str(row[col[0]]).lower()[0:4] == '4200'):
                valuePP = 0
                if(row[col[0]] in posgradosPagos):
                    valuePP = posgradosPagos[row[col[0]]]
                    valuePP = valuePP + ['B'+str(cont+1)]
                    posgradosPagos[row[col[0]]] = valuePP
    elif(item == 4):
        worksheet.write(cont, 11, '=SUMIFS(Pagos_SAP!B:B,Pagos_SAP!A:A,Egresos_SIGEP!A'+str(cont+1)+',Pagos_SAP!G:G,@Egresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-L'+str(cont+1), format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]].split()[0], '%Y-%m-%d'), date)

def totalesSheets(worksheet, shapes, format, item, total, negRecaudos, col, enPos):
    moneyTotalSap = workbook.add_format({'num_format': '#,##', 'fg_color':'#ffff00'})
    if(item == 2) | (item == 4):
        worksheet.write(shapes, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, 11, '=SUM(L2:L'+str(shapes)+')', format)
        worksheet.write(shapes, 12, '=SUM(M2:M'+str(shapes)+')', format)
    elif(item == 3):
        worksheet.write(shapes, 1, total[1], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-5, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-5)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-4, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-4)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-3, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-3)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-3)+str(shapes)+')', format)
    elif(item == 1):
        worksheet.write(shapes, 1, total[2], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=('+('+'.join(negRecaudos))+')', format)
        if(enPos == True):
            worksheet.write(shapes, len(col)-8, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-7, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-7)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-6, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-6)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-6)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-5, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-5)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-4, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-4)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-3, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-3)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-3)+str(shapes)+')', format)

def verificaDataFrameVacio(worksheet, conciliar, fila, col, dato, tag):
    if(conciliar.empty):
        worksheet.write(fila, col, 0, tag)
    else:
        worksheet.write(fila, col, dato, tag)

def uneBancolombia(pago, egreso, colp, cole, rPago, rEgreso):
    sumP = rPago[colp[1]].sum()
    sumE = rEgreso[cole[1]].sum()
    if(sumP == sumE):
        rPago['valida'] = 0
        rEgreso['valida'] = 0
        pago.update(rPago)
        egreso.update(rEgreso)

path = sys.argv[2]+"conciliacion/"
porcentaje_salud = round(float(sys.argv[4]),5)
porcentaje_ingresos = round(float(sys.argv[5]),4)

general_sigep_dataframe = pd.DataFrame()
pagos_sap_dataframe = pd.DataFrame()
recaudos_sap_dataframe = pd.DataFrame()

ingresos_sigep_dataframe = pd.DataFrame()
egresos_sigep_dataframe = pd.DataFrame()

general_sigep = 'general_sigep_'+str(sys.argv[1])+'_'+sys.argv[3]+'.xlsx'
if exists(path + general_sigep):
    general_sigep_dataframe = pd.read_excel(path + general_sigep)

pagos_sap = 'pagos_sap_'+str(sys.argv[1])+'_'+sys.argv[3]+'.xlsx'
if exists(path + pagos_sap):
    pagos_sap_dataframe = pd.read_excel(path + pagos_sap).astype(str)

recaudos_sap = 'recaudos_sap_'+str(sys.argv[1])+'_'+sys.argv[3]+'.xlsx'
if exists(path + recaudos_sap):
    recaudos_sap_dataframe = pd.read_excel(path + recaudos_sap).astype(str)

colsInicial = general_sigep_dataframe.columns.tolist()
pagosSap = pagos_sap_dataframe
recaudosSap = recaudos_sap_dataframe
stringSigep = general_sigep_dataframe[colsInicial[9]].apply(lambda s: type(s) == str)
stringSigep = general_sigep_dataframe[stringSigep]
general_sigep_dataframe.loc[stringSigep.index.tolist(),colsInicial[9]] = 0
general_sigep_dataframe = general_sigep_dataframe.astype(str)

#generalSigep
ingresos_sigep_dataframe = ingresos_egresos_sigep(general_sigep_dataframe, colsInicial, 'Ingreso')
egresos_sigep_dataframe = ingresos_egresos_sigep(general_sigep_dataframe, colsInicial, 'Egreso')

#Habilita Posgrados
enablePos = False
if(str(sys.argv[1]) == '21920005'):
    enablePos = True

''' TITULOS SIGEP '''
titulosSigep=['Número de Soporte','Valor','Proyecto','Codigo','Tipo','Fecha','Periodo','Referencia','Nit/Cédula','Observación','Tipo de Soporte',' Formula','Diferencia','Observaciones','valida']

totaDetSap = {1:'', 2:''}

''' SE CREA EL ARCHIVO DE EXCEL'''
writer = pd.ExcelWriter(sys.argv[2]+'files_out/Centro_de_Costos_'+str(sys.argv[1])+'_'+sys.argv[3]+'.xlsx', 
                        engine='xlsxwriter', 
                        options={'nan_inf_to_errors': True})

sheets = {1:'Recaudos_SAP',2:'Ingresos_SIGEP',3:'Pagos_SAP',4:'Egresos_SIGEP'}

#Se crea conciliacion de recaudos
pd.DataFrame().to_excel(writer, sheet_name='Conciliación', index=False)

''' ESTILOS '''
workbook = writer.book
merge_center = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter'})
merge_format = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#acb9ca'})
merge_bold = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter'})
merge_bold_color = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#ededed'})

cell_size = 12.5
bold = workbook.add_format({'bold': 1})
bold_money = workbook.add_format({'bold': 1, 'num_format': '#,##0'})
money = workbook.add_format({'num_format': '#,##0'})
title = workbook.add_format({'fg_color': '#C6E0B4'})
titleConciliacion = workbook.add_format({'bold': 1, 'fg_color': '#FCE4D6'})
date = workbook.add_format({'num_format': 'mm/dd/yyyy'})

''' Conciliacion '''
worksheet = writer.sheets['Conciliación']
worksheet.set_column('A:E', cell_size, None)
worksheet.merge_range('A1:E2', periodo_mes.upper() + ' - CONCILIACIÓN CENTRO DE COSTOS '+str(sys.argv[1]), merge_format)

cont = 5
cont_recaudos_ingresos = 0
pV = 1

#ESTILO DE RECAUDOS - INGRESOS- PAGOS - EGRESOS
dataFrames = {1: pd.DataFrame(), 2: pd.DataFrame(), 3: pd.DataFrame(), 4: pd.DataFrame()}

pagosValidar = pd.DataFrame()
shapeSIGEP = []
shapeSAP = []

if not ingresos_sigep_dataframe.empty:
    colsInicialN = ingresos_sigep_dataframe.columns.tolist()
    ingresos_sigep_dataframe[colsInicialN[0]] = ingresos_sigep_dataframe[colsInicialN[0]].astype(float)
    ingresos_sigep_dataframe[colsInicialN[1]] = ingresos_sigep_dataframe[colsInicialN[1]].astype(float)

    #recaudosSap
    cols = recaudosSap.columns.tolist()
    cols = [cols[6]] + [cols[5]] + cols[0:5] + cols[7:]
    totaDetSap[2] = float(recaudosSap.loc[recaudosSap.shape[0]-1,cols[1]])
    recaudosSap = recaudosSap[cols]
    recaudosSap = recaudosSap[:-1]
    #Posgrados
    if(enablePos == True):
        recaudosSap['Total Ingresos'] = 0
        recaudosSap['% Ingreso Sigep_'+str(porcentaje_ingresos*100)+'%'] = 0
        recaudosSap['Pendiente registrar en proyecto ingresos_'+str(100-(porcentaje_ingresos*100))+'%'] = 0
        recaudosSap['Deducciones'] = 0
    recaudosSap['Formula'] = 0
    recaudosSap['Diferencia'] = 0
    recaudosSap['Observaciones'] = 0
    recaudosSap['valida'] = 0
    recaudosSap[cols[0]] = recaudosSap[cols[0]].astype(float)
    recaudosSap[cols[1]] = recaudosSap[cols[1]].astype(float)
    recaudosSap[cols[6]] = recaudosSap[cols[6]].astype(float)
    recaudosSap[cols[6]] = recaudosSap[cols[6]].astype(int)

    #Formula y diferencia
    valorFormulaDiferencia(ingresos_sigep_dataframe, recaudosSap)
    valorFormulaDiferencia(recaudosSap, ingresos_sigep_dataframe)

    #Calculos CC 21920005 POSGRADOS
    ccPosgrados = dict()
    ccPosgradosPagos = dict()
    if(enablePos == True):
        principal = -1

        colI = ingresos_sigep_dataframe.columns.tolist()
        ccPSigep = ingresos_sigep_dataframe.apply(lambda s: str(s[colI[0]]).lower()[0:4] == '4200', axis=1)
        ccPSigep = ingresos_sigep_dataframe[ccPSigep]
        ccPSigepD = ccPSigep[ccPSigep[colI[0]].duplicated() == True]
        if(~ccPSigepD.empty):
            if(ccPSigepD.shape[0] == 1):
                principal = ccPSigepD.iloc[0][colI[0]]
        ingresoPosPrin = ccPSigep[colI[0]] == principal
        ingresoPosPrin = ccPSigep[ingresoPosPrin]

        cols = recaudosSap.columns.tolist()
        ccPosgradosC = recaudosSap.apply(lambda s: str(s[cols[0]]).lower()[0:4] == '4200', axis=1)
        ccPosgradosC = recaudosSap[ccPosgradosC]

        ccPosgradosF = ccPosgradosC[[cols[0]] + [cols[1]]]
        ccPosgradosF = ccPosgradosF.groupby([cols[0]]).sum()
        ccPosgradosF = ccPosgradosF.reset_index()
        ccPosgrados = dict.fromkeys(ccPosgradosF[cols[0]], [])
        ccPosgradosPagos = dict.fromkeys(ccPosgradosF[cols[0]], [])

        valueProyeIngre = 0
        for item in ccPosgrados:
            valueR = ccPosgradosC[cols[0]] == item
            valueI = ingresos_sigep_dataframe[colI[0]] == item
            valueR = ccPosgradosC[valueR]
            valueI = ingresos_sigep_dataframe[valueI]
            valueT = abs(valueR[cols[1]]).sum()
            sumaR = valueT*porcentaje_ingresos
            valueProyeIngre += (valueT - sumaR)
            sumaI = int(abs(valueI[colI[1]]).sum())
            if(int(sumaR) == sumaI):
                valueR['valida'] = 0
                valueI['valida'] = 0
                recaudosSap.update(valueR)
                ingresos_sigep_dataframe.update(valueI)

        numero_documento_base = 0
        sumatoria_documento_base = 0

        for index, row in ingresoPosPrin.iterrows():
            updRecaudo = ccPosgradosC[cols[0]] == row[colI[0]]
            updRecaudo = ccPosgradosC[updRecaudo]
            if(updRecaudo.empty == False):
                valueT = abs(updRecaudo[cols[1]]).sum()
                sumaR = int(round(valueT*porcentaje_ingresos))
                if(sumaR == int(float(row[colI[1]]))):
                    updRecaudo['valida'] = 0
                    ingresoPosPrin.loc[index,'valida'] = 0
                    ingresos_sigep_dataframe.update(ingresoPosPrin)
                    recaudosSap.update(updRecaudo)

                if int(row[colI[1]]) == int(valueProyeIngre):
                    numero_documento_base = row[colI[0]]
                    sumatoria_documento_base = sumaR
                    ingresoPosPrin.loc[index,'valida'] = 0
                    ingresos_sigep_dataframe.update(ingresoPosPrin)

        if(numero_documento_base != 0 and sumatoria_documento_base != 0):
            ingreso_documento_base = ingresoPosPrin[colI[0]] == numero_documento_base
            ingreso_documento_base = ingresoPosPrin[ingreso_documento_base]
            for index, row in ingreso_documento_base.iterrows():
                if(int(row[colI[1]]) == sumatoria_documento_base):
                    updRecaudo = ccPosgradosC[cols[0]] == numero_documento_base
                    updRecaudo = ccPosgradosC[updRecaudo]
                    updRecaudo['valida'] = 0
                    recaudosSap.update(updRecaudo)
                    ingreso_documento_base.loc[index,'valida'] = 0
                    ingresos_sigep_dataframe.update(ingreso_documento_base)

    colRS = recaudosSap.columns.tolist()
    recaudosSap = recaudosSap.sort_values(by=[colRS[0]])

    ingresos_sigep_dataframe.columns = titulosSigep

    cols = recaudosSap.columns.tolist()
    ingreso = ingresos_sigep_dataframe

    recaudos = recaudosSap

    positivosRecaudos = recaudos.apply(lambda s: float(s[cols[1]]) > 0, axis=1)
    positivosRecaudos = recaudos[positivosRecaudos]

    recaudosValidar = recaudos.apply(lambda s: (s['valida'] != 0) & (float(s[cols[1]]) <= 0), axis=1)
    recaudosValidar = recaudos[recaudosValidar]
    cols = recaudosValidar.columns.tolist()
    recaudosValidar = recaudosValidar[[cols[0]]+ [cols[1]]]
    recaudosValidar = recaudosValidar.groupby([cols[0]]).sum()
    recaudosValidar = recaudosValidar.reset_index()

    ingresosValidar = ingreso.apply(lambda s: (s['valida'] != 0), axis=1)
    ingresosValidar = ingreso[ingresosValidar]
    colsI = ingresosValidar.columns.tolist()
    ingresosValidar = ingresosValidar[[colsI[0]]+ [colsI[1]]]
    ingresosValidar = ingresosValidar.groupby([colsI[0]]).sum()
    ingresosValidar = ingresosValidar.reset_index()

    recaudosV = recaudos.drop(columns='valida')
    recaudosV.to_excel(writer, index=False, sheet_name=sheets[1])

    colE = ingreso.columns.tolist()
    ingresoV = ingreso.drop(columns='valida')
    ingresoVAjuste = ingresoV[colE[0]].apply(lambda s: s == 0)
    ingresoVAjuste = ingresoV[ingresoVAjuste]
    ingresoAjuste = stringSigep[colsInicial[2]] == 'Ingreso'
    ingresoAjuste = stringSigep[ingresoAjuste]
    ingresoVAjuste.loc[:,colE[0]] = ingresoAjuste[colsInicial[9]]
    ingresoV.update(ingresoVAjuste)
    ingresoV.to_excel(writer, index=False, sheet_name=sheets[2])

    cols = positivosRecaudos.columns.tolist()
    shapePositivos = positivosRecaudos.shape

    for index, row in positivosRecaudos.iterrows():
        worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), 'Menos ingreso '+str(int(row[cols[0]]))+' (en positivo no se registra)', merge_center)
        worksheet.write(cont, 3, row[cols[1]], money)
        cont = cont + 1

    cols = recaudosValidar.columns.tolist()
    shapeRecaudosV = recaudosValidar.shape
    cont = shapePositivos[0] + 5
    for index, row in recaudosValidar.iterrows():
        worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
        worksheet.write(cont, 4, abs(row[cols[1]]), money)
        cont = cont + 1

    if(positivosRecaudos.empty):
        inicial = 6
    else:
        inicial = 5

    cols = ingresosValidar.columns.tolist()
    shapeIngresoV = ingresosValidar.shape
    cont = shapePositivos[0] + shapeRecaudosV[0] + 5
    for index, row in ingresosValidar.iterrows():
        worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
        if(row[cols[0]] == 0):
            worksheet.write(cont, 0, 'Ajustes', merge_center)
        worksheet.write(cont, 4, abs(row[cols[1]]), money)
        cont = cont + 1

    cont_recaudos_ingresos = shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]

    worksheet.write(cont_recaudos_ingresos+6, 3, '=D5-SUM(D6:D'+str(shapePositivos[0]+inicial)+')', money)
    worksheet.write(cont_recaudos_ingresos+6, 4, '=SUM(E5:E'+str(shapePositivos[0]+shapeRecaudosV[0]+5)+')-SUM(E'+str(shapePositivos[0]+shapeRecaudosV[0]+6)+':E'+str(cont_recaudos_ingresos+inicial)+')', money)
    worksheet.write(cont_recaudos_ingresos+7, 4, '=D'+str(cont_recaudos_ingresos+7)+'-E'+str(cont_recaudos_ingresos+7), bold_money)

    dataFrames[1] = recaudos
    dataFrames[2] = ingreso

if not egresos_sigep_dataframe.empty:
    colsInicialN = egresos_sigep_dataframe.columns.tolist()
    egresos_sigep_dataframe[colsInicialN[0]] = egresos_sigep_dataframe[colsInicialN[0]].astype(float)
    egresos_sigep_dataframe[colsInicialN[1]] = egresos_sigep_dataframe[colsInicialN[1]].astype(float)

    #pagosSap
    cols = pagosSap.columns.tolist()
    cols = [cols[7]] + [cols[5]] + cols[0:5]+ [cols[6]] + cols[8:]
    totaDetSap[1] = float(pagosSap.loc[pagosSap.shape[0]-1,cols[1]])
    pagosSap = pagosSap[cols]
    pagosSap = pagosSap[:-1]
    pagosSap['Formula'] = 0
    pagosSap['Diferencia'] = 0
    pagosSap['SS'] = 0
    pagosSap['Observaciones'] = 0
    pagosSap['valida'] = 0

    #pagosSap
    cols = pagosSap.columns.tolist()
    nanValues = pagosSap.apply(lambda s: str(s[cols[0]]).lower() == 'nan', axis=1)
    newPagosSap = pagosSap[nanValues]
    for index, row in newPagosSap.iterrows():
        val = row[cols[4]]
        if(val[0:2] == '81') | (val[0:5] == '1000'):
            newPagosSap.loc[index,cols[0]] = float(row[cols[4]])
        else:
            newPagosSap.loc[index,cols[0]] = float(row[cols[2]])
    pagosSap.update(newPagosSap)
    pagosSap[cols[0]] = pagosSap[cols[0]].astype(float)
    pagosSap[cols[1]] = pagosSap[cols[1]].astype(float)
    pagosSap[cols[6]] = pagosSap[cols[6]].astype(float)


    colGeneralSigep = egresos_sigep_dataframe.columns.tolist()
    # Se filtra por cobrad porque estan escribiendo cobrado o cobrada
    generalSigepSinSSCobrada = egresos_sigep_dataframe.apply(lambda s: str(s[colGeneralSigep[9]]).lower()[0:9] != 'ss cobrad', axis=1)
    generalSigepSinSSCobrada = egresos_sigep_dataframe[generalSigepSinSSCobrada]
    if(generalSigepSinSSCobrada.empty == True):
        generalSigepSinSSCobrada = egresos_sigep_dataframe
        
    valorFormulaDiferencia(generalSigepSinSSCobrada, pagosSap)
    valorFormulaDiferencia(pagosSap, generalSigepSinSSCobrada)
    egresos_sigep_dataframe.update(generalSigepSinSSCobrada)

    if(enablePos == True):
        cols = pagosSap.columns.tolist()
        #5300 no aparecio
        pagosPosSap = pagosSap.apply(lambda s: (str(s[cols[4]]).lower()[0:4] == '4200') | (str(s[cols[4]]).lower()[0:4] == '5300'), axis=1)
        pagosPosSapD = pagosSap[pagosPosSap]
        for index, row in pagosPosSapD.iterrows():
            pagosPosSapD.loc[index,cols[0]] = int(row[cols[4]])
        pagosSap.update(pagosPosSapD)

        pagosPosSap = pagosSap.apply(lambda s: str(s[cols[4]]).lower()[0:4] == '4200', axis=1)
        pagosPosSap = pagosSap[pagosPosSap]
        totalPosgradosPagos = abs(pagosPosSap[cols[1]]).sum()
        prinEgre = egresos_sigep_dataframe[colI[0]] == principal
        prinEgre = egresos_sigep_dataframe[prinEgre]
        if(~prinEgre.empty):
            if(prinEgre.shape[0] == 1):
                if(prinEgre.iloc[0][colI[1]] == totalPosgradosPagos):
                    pagosPosSap['valida'] = 0
                    prinEgre['valida'] = 0
                    egresos_sigep_dataframe.update(prinEgre)
                    pagosSap.update(pagosPosSap)


        cols = pagosSap.columns.tolist()
        pagosSap = pagosSap.sort_values(by=[cols[0]])


    colP = pagosSap.columns.tolist()
    colE = egresos_sigep_dataframe.columns.tolist()

    #UNE EPM PAGOS - EGRESOS
    uneEpm = 'une epm telecomunicaciones'
    uneEpmP = pagosSap.apply(lambda s: uneEpm in str(s[colP[17]]).lower(), axis=1)
    uneEpmP = pagosSap[uneEpmP]
    if(uneEpmP.empty == False):
        uneEpmE = egresos_sigep_dataframe.apply(lambda s: uneEpm in str(s[colE[8]]).lower(), axis=1)
        uneEpmE = egresos_sigep_dataframe[uneEpmE]
        uneBancolombia(pagosSap, egresos_sigep_dataframe, colP, colE, uneEpmP, uneEpmE)

    #BANCOLOMBIA PAGOS - EGRESOS
    bancolombiaP = pagosSap.apply(lambda s: 'bancolombia s.a.' in str(s[colP[17]]).lower(), axis=1)
    bancolombiaP = pagosSap[bancolombiaP]
    if(bancolombiaP.empty == False):
        bancolombiaE = egresos_sigep_dataframe.apply(lambda s: 'gastos bancarios' in str(s[colE[9]]).lower(), axis=1)
        bancolombiaE = egresos_sigep_dataframe[bancolombiaE]
        uneBancolombia(pagosSap, egresos_sigep_dataframe, colP, colE, bancolombiaP, bancolombiaE)

    #APORTES POR DED CONV
    cols = pagosSap.columns.tolist()
    aportesPDC = pagosSap.apply(lambda s: str(s[cols[12]]).lower() == 'aportes por ded conv', axis=1)
    aportesPDC = pagosSap[aportesPDC]
    if(aportesPDC.empty == False):
        aportesPDCValue = aportesPDC.iloc[0][cols[4]]
        aportes_egresos = egresos_sigep_dataframe[colE[0]] == int(float(aportesPDCValue))
        aportes_egresos = egresos_sigep_dataframe[aportes_egresos]
        if(aportes_egresos.empty == False):
            aportesPDCSum = aportesPDC[cols[1]].sum()
            if(int(aportesPDCSum) == int(float(aportes_egresos.iloc[0][colE[1]]))):
                aportes_egresos['valida'] = 0
                aportesPDC['valida'] = 0
                egresos_sigep_dataframe.update(aportes_egresos)
                pagosSap.update(aportesPDC)

    #Calculo seguridad
    # MEN022022-3-1 or MEN022022-3-3, termina en 1 o 3
    cols = pagosSap.columns.tolist()
    salario = pagosSap.apply(lambda s: (str(s[cols[12]]).lower()[0:8] == 'docentes') & (str(s[cols[4]]).lower()[0:3] == 'men') & ((str(s[cols[4]]).lower().strip()[-1] == '1') | (str(s[cols[4]]).lower().strip()[-1] == '3')), axis=1)
    newPagosSap = pagosSap[salario]
    salarioEps = newPagosSap[[cols[0]] + [cols[1]]]
    salarioEps = salarioEps.groupby([cols[0]]).sum()
    salarioEps = salarioEps.reset_index()
    salarioEps = dict.fromkeys(salarioEps[cols[0]], [])

    fomulaSSValida(pagosSap, newPagosSap, cols)
    pagosSap.update(newPagosSap)

    colE = egresos_sigep_dataframe.columns.tolist()
    for item in salarioEps:
        pago = pagosSap[cols[0]] == item
        pago = pagosSap[pago]
        egreso = egresos_sigep_dataframe[colE[0]] == item
        egreso = egresos_sigep_dataframe[egreso]
        if(pago.shape[0] == 1):
            unsoloMEN = pago.apply(lambda s: (str(s[cols[12]]).lower()[0:8] == 'docentes') & (str(s[cols[4]]).lower()[0:3] == 'men') & ((str(s[cols[4]]).lower().strip()[-1] == '1') | (str(s[cols[4]]).lower().strip()[-1] == '3')), axis=1)
            unsoloMEN = pago[unsoloMEN]
            if(unsoloMEN.empty == False):
                if(unsoloMEN.iloc[0][cols[1]] == egreso.iloc[0][colE[1]]):
                    pago['valida'] = 0
                    egreso['valida'] = 0
                    pagosSap.update(pago)

        suma = abs(pago['valida']).sum()
        egreso['valida'] = suma
        egresos_sigep_dataframe.update(egreso)

    #GIROS
    regex_all_giros_zims = r'zims\s[0-9]+.*'
    regex_index_giros_zims = r'zims\s[0-9]+$'
    giros = pagosSap.apply(lambda x: len(re.findall(regex_all_giros_zims, str(x[cols[4]]).lower())) != 0, axis=1)
    giros = pagosSap[giros]
    if(giros.empty == False):
        giros_index = giros.apply(lambda x: len(re.findall(regex_index_giros_zims, str(x[cols[4]]).lower())) != 0, axis=1)
        giros_index = giros[giros_index]
        for index, giros_row in giros_index.iterrows():

            giros_sigep = egresos_sigep_dataframe[colE[0]] == giros_row[cols[0]]
            giros_sigep = egresos_sigep_dataframe[giros_sigep]
            giros_sigep_total = abs(giros_sigep[colE[1]]).sum()

            giros_retefuente = giros.apply(lambda x: len(re.findall(re.escape(str(giros_row[cols[4]]).lower())+r'\s[a-z]+', str(x[cols[4]]).lower())) != 0, axis=1)
            giros_retefuente = giros[giros_retefuente]

            giros_retefuente_valor = 0
            if(giros_retefuente.empty == False):
                giros_retefuente_valor = abs(giros_retefuente[cols[1]]).sum()

            giros_sap_total = giros_retefuente_valor + giros_row[cols[1]]

            if(int(giros_sigep_total) == giros_sap_total):
                giros_retefuente['valida'] = 0
                giros_index.loc[index,'valida'] = 0
                giros_sigep['valida'] = 0
                pagosSap.update(giros_retefuente)
                pagosSap.update(giros_index)
                egresos_sigep_dataframe.update(giros_sigep)

    #seguridad
    colP = pagosSap.columns.tolist()
    colR = egresos_sigep_dataframe.columns.tolist()
    ssSap = pagosSap.apply(lambda s: str(s[colP[4]]).lower()[0:6] == 'automn', axis=1)
    ssSigep = egresos_sigep_dataframe.apply(lambda s: str(s[colR[9]]).lower()[0:2] == 'ss', axis=1)
    ssSap = pagosSap[ssSap]
    ssSigep = egresos_sigep_dataframe[ssSigep]

    egresos_sigep_dataframe.columns = titulosSigep

    ssSigep.columns = titulosSigep

    egreso = egresos_sigep_dataframe
    seguridadSap = ssSap
    seguridadSigep = ssSigep
    pagos = pagosSap

    pagosValidar = pagos.apply(lambda s: (s['valida'] != 0) & (str(s[cols[4]]).lower()[0:6] != 'automn'), axis=1)
    pagosValidar = pagos[pagosValidar]
    cols = pagosValidar.columns.tolist()
    pagosValidar = pagosValidar[[cols[0]]+ [cols[1]]]
    pagosValidar = pagosValidar.groupby([cols[0]]).sum()
    pagosValidar = pagosValidar.reset_index()

    colE = egreso.columns.tolist()
    egresoValidar = egreso.apply(lambda s: (s['valida'] != 0) & (str(s[colE[9]]).lower()[0:2] != 'ss'), axis=1)
    egresoValidar = egreso[egresoValidar]
    cols = egresoValidar.columns.tolist()
    egresoValidar = egresoValidar[[cols[0]]+ [cols[1]]]
    egresoValidar = egresoValidar.groupby([cols[0]]).sum()
    egresoValidar = egresoValidar.reset_index()

    pagosV = pagos.drop(columns='valida')
    pagosV.to_excel(writer, index=False, sheet_name=sheets[3])

    egresoV = egreso.drop(columns='valida')
    egresoVAjuste = egresoV[colE[0]].apply(lambda s: s == 0)
    egresoVAjuste = egresoV[egresoVAjuste]
    egresoAjuste = stringSigep[colsInicial[2]] == 'Egreso'
    egresoAjuste = stringSigep[egresoAjuste]
    egresoVAjuste.loc[:,colE[0]] = egresoAjuste[colsInicial[9]]
    egresoV.update(egresoVAjuste)
    egresoV.to_excel(writer, index=False, sheet_name=sheets[4])

    ''' HOJA DE SEGURIDAD SOCIAL SS '''
    cols = seguridadSap.columns.tolist()
    cols = [cols[0]] + [cols[1]] + cols[4:7] + [cols[9]] + cols[20:22]
    seguridadSap = seguridadSap[cols]
    shapeSAP = seguridadSap.shape
    seguridadSap.to_excel(writer, sheet_name='SS', startrow=1, header=True, index=False)

    if(seguridadSap.empty):
        ssSS = 2
    else:
        ssSS = 3

    worksheet_ss = writer.sheets['SS']
    worksheet_ss.write(shapeSAP[0]+2, 1, '=SUM(B'+str(ssSS)+':B'+str(shapeSAP[0]+2)+')', bold_money)
    worksheet_ss.write(0, 0, 'SS SAP', bold)
    worksheet_ss.set_column('A:AB', cell_size, None)
    worksheet_ss.set_column('B:B', None, money)

    contSS = 2
    for index, row in seguridadSap.iterrows():
        worksheet_ss.write(contSS, 3, datetime.strptime(row[cols[3]], '%Y-%m-%d').date(), date)
        contSS += 1 

    cols = seguridadSigep.columns.tolist()
    seguridadSigep = seguridadSigep[cols[0:11]]
    shapeSIGEP = seguridadSigep.shape

    seguridadSigep.to_excel(writer, sheet_name='SS', startrow=shapeSAP[0]+5, header=True, index=False)

    contSS = contSS + 4
    for index, row in seguridadSigep.iterrows():
        worksheet_ss.write(contSS, 5, datetime.strptime(row[cols[5]].split()[0], '%Y-%m-%d'), date)
        
        contSS += 1 

    if(seguridadSigep.empty):
        ssSI = 6
    else:
        ssSI = 7
    worksheet_ss = writer.sheets['SS']
    worksheet_ss.write(shapeSAP[0]+shapeSIGEP[0]+6, 1, '=SUM(B'+str(shapeSAP[0]+ssSI)+':B'+str(shapeSAP[0]+shapeSIGEP[0]+6)+')', bold_money)
    worksheet_ss.write(shapeSAP[0]+4, 0, 'SS SIGEP', bold)

    worksheet_ss.write(shapeSAP[0]+shapeSIGEP[0]+8, 0, 'SAP')
    verificaDataFrameVacio(worksheet_ss, seguridadSap, shapeSAP[0]+shapeSIGEP[0]+8, 1, '=B'+str(shapeSAP[0]+3), money)
    worksheet_ss.write(shapeSAP[0]+shapeSIGEP[0]+9, 0, 'SIGEP')
    verificaDataFrameVacio(worksheet_ss, seguridadSigep, shapeSAP[0]+shapeSIGEP[0]+9, 1, '=B'+str(shapeSAP[0]+shapeSIGEP[0]+7), money)
    worksheet_ss.write(shapeSAP[0]+shapeSIGEP[0]+10, 0, 'Diferencia')
    worksheet_ss.write(shapeSAP[0]+shapeSIGEP[0]+10, 1, '=B'+str(shapeSAP[0]+shapeSIGEP[0]+9)+'-B'+str(shapeSAP[0]+shapeSIGEP[0]+10), bold_money)

    cols = pagosValidar.columns.tolist()

    if(pagosValidar.empty):
        pV = 1
    else:
        cont = cont_recaudos_ingresos+12
        sumatoriaNegativosPagosSap = pagosValidar[cols[1]].sum()
        worksheet.write(cont, 3, sumatoriaNegativosPagosSap, money)
        pV = 0

    cols = egresoValidar.columns.tolist()
    shapeEgresoV = egresoValidar.shape
    cont = cont_recaudos_ingresos+13
    for index, row in egresoValidar.iterrows():
        worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
        if(row[cols[0]] == 0):
            worksheet.write(cont, 0, 'Ajustes', merge_center)
        worksheet.write(cont, 4, abs(row[cols[1]]), money)
        cont = cont + 1

    if(pagosValidar.empty):
        worksheet.write(cont+1, 3, '=D'+str(cont_recaudos_ingresos+11), money)
    else:
        worksheet.write(cont+1, 3, '=D'+str(cont_recaudos_ingresos+11)+'-D'+str(cont_recaudos_ingresos+13), money)

    dataFrames[3] = pagos
    dataFrames[4] = egreso

if egresos_sigep_dataframe.empty:
    cont = 11

#Ingresos
worksheet.merge_range('A4:C4', 'Ingresos', merge_bold_color)
worksheet.write(3, 3, 'SAP', merge_bold_color)
worksheet.write(3, 4, 'SIGEP', merge_bold_color)
worksheet.merge_range('A5:C5', 'Notas', merge_center)
worksheet.merge_range('A'+str(cont_recaudos_ingresos+7)+':C'+str(cont_recaudos_ingresos+7), 'Total', merge_bold)
worksheet.merge_range('A'+str(cont_recaudos_ingresos+8)+':C'+str(cont_recaudos_ingresos+8), 'Diferencias', merge_bold)

#Egresos
worksheet.merge_range('A'+str(cont_recaudos_ingresos+10)+':C'+str(cont_recaudos_ingresos+10), 'Egresos', merge_bold_color)
worksheet.write(cont_recaudos_ingresos+9, 3, 'SAP', merge_bold_color)
worksheet.write(cont_recaudos_ingresos+9, 4, 'SIGEP', merge_bold_color)
worksheet.merge_range('A'+str(cont_recaudos_ingresos+11)+':C'+str(cont_recaudos_ingresos+11), 'Notas', merge_center)
worksheet.merge_range('A'+str(cont+2)+':C'+str(cont+2), 'Total', merge_bold)
if not egresos_sigep_dataframe.empty:
    worksheet.write(cont+1, 4, '=SUM(E'+str(cont_recaudos_ingresos+11)+':E'+str(cont_recaudos_ingresos+12)+')-SUM(E'+str(cont_recaudos_ingresos+13)+':E'+str(cont+pV)+')', money)
worksheet.merge_range('A'+str(cont+3)+':C'+str(cont+3), 'Diferencias', merge_bold)
worksheet.write(cont+2, 4, '=D'+str(cont+2)+'-E'+str(cont+2), bold_money)

for item in sheets:
    if sheets[item] in writer.sheets:
        if(item % 2) != 0:

            worksheet = writer.sheets[sheets[item]]
            if(item == 1):
                if(enablePos == True):
                    worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2), cell_size, None)
                    worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2)+'1')
                else:
                    worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2), cell_size, None)
                    worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2)+'1')
            else:
                worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2), cell_size, None)
                worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2)+'1')
            worksheet.set_column('C:D', None, None, {'hidden': True})
            worksheet.set_column('H:L', None, None, {'hidden': True})
            worksheet.set_column('N:Q', None, None, {'hidden': True})
            worksheet.set_column('S:T', None, None, {'hidden': True})
            worksheet.set_column('U:U', None, None, {'hidden': True})
            
        elif(item % 2) == 0:
            worksheet = writer.sheets[sheets[item]]
            worksheet.set_column('A:N', cell_size, None)
            worksheet.autofilter('A1:N1')

correct_info = workbook.add_format({'fg_color': '#C6E0B4'})
correct_info_money = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '#,##0'})
ss_info = workbook.add_format({'fg_color': '#FFFF00'})
ss_info_money = workbook.add_format({'fg_color': '#FFFF00', 'num_format': '#,##0'})
wrong_info = workbook.add_format({'fg_color': '#F8CBAD'})
wrong_info_money = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '#,##0'})
correct_info_date = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': 'mm/dd/yyyy'})
ss_info_date = workbook.add_format({'fg_color': '#FFFF00', 'num_format': 'mm/dd/yyyy'})
wrong_info_date = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': 'mm/dd/yyyy'})
deducciones_color = workbook.add_format({'fg_color': '#bdd7ee', 'num_format': '#,##0'})
correct_normal_format = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '###'})
wrong_normal_format = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '###'})

totales = {1: 0, 2: 0, 3: 0, 4: 0}

if not ingresos_sigep_dataframe.empty:
    salarioEps = pd.DataFrame()

if ingresos_sigep_dataframe.empty:
    ccPosgrados = pd.DataFrame()
    ccPosgradosPagos = pd.DataFrame()
    posNegRecaudos = pd.DataFrame()

for item in dataFrames:
    if sheets[item] in writer.sheets:
        posNegRecaudos = []
        worksheet = writer.sheets[sheets[item]]
        shapes = dataFrames[item].shape
        shapes = shapes[0] + 2
        totales[item] = shapes
        col = dataFrames[item].columns.tolist()
        cont = 1
        for index, row in dataFrames[item].iterrows():
            if (float(row['valida']) == 0):
                worksheet.set_row(cont,None, correct_info)
                style(item, row, col, worksheet, cont, correct_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, correct_info_date, correct_normal_format)
            else:
                worksheet.set_row(cont,None, wrong_info)
                style(item, row, col, worksheet, cont, wrong_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, wrong_info_date, wrong_normal_format)

            if (str(row[col[4]]).lower()[0:6] == 'automn') | (str(row[col[9]]).lower()[0:2] == 'ss'):
                worksheet.set_row(cont,None, ss_info)
                style(item, row, col, worksheet, cont, ss_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, ss_info_date, None)
            cont = cont + 1
        if(dataFrames[item].empty):
            shapes = 3
        totalesSheets(worksheet, shapes-1, money, item, totaDetSap, posNegRecaudos, col, enablePos)
        worksheet.set_row(0, 30, title)

# Formato en excel para calculo de salud en pagos sap
if not dataFrames[3].empty:
    col = dataFrames[3].columns.tolist()
    worksheet = writer.sheets[sheets[3]]
    salud = workbook.add_format({'num_format': '#,##0'})
    cont = 1
    for index, row in dataFrames[3].iterrows():
        if (str(row[col[12]]).lower()[0:8] == 'docentes') & (str(row[col[4]]).lower()[0:3] == 'men')  & ((str(row[col[4]]).lower().strip()[-1] == '1') | (str(row[col[4]]).lower().strip()[-1] == '3')):
            if not salarioEps.empty:
                value = salarioEps[row[col[0]]]
                if (float(row['valida']) == 0):
                    worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*'+str(porcentaje_salud*100)+'%', correct_info_money)  
                else:
                    worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*'+str(porcentaje_salud*100)+'%', wrong_info_money)  
    cont = cont + 1

# Formato en excel para calculo de porcentajes en recaudos sap
if(enablePos == True):
    if not dataFrames[1].empty:
        col = dataFrames[1].columns.tolist()
        worksheet = writer.sheets[sheets[1]]
        formato = workbook.add_format({'num_format': '#,##0'})
        cont = 1
        rowCont = 0
        anterior = 0
        for index, row in dataFrames[1].iterrows():
            if(str(row[col[0]]).lower()[0:4] == '4200'):
                if(row[col[0]] != anterior):
                    rowCont = 1
                else:
                    worksheet.write(cont, len(col)-5, 0, deducciones_color)
                    rowCont = 0

                if(rowCont == 1):
                    valueCCP = ccPosgrados[row[col[0]]]
                    if (float(row['valida']) == 0):
                        worksheet.write(cont, len(col)-8, '=abs('+('+'.join(valueCCP))+')', correct_info_money)
                        worksheet.write(cont, len(col)-7, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+')*'+str(porcentaje_ingresos*100)+'%', correct_info_money)   
                        worksheet.write(cont, len(col)-6, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(cont+1)+')', correct_info_money)
                    else:
                        worksheet.write(cont, len(col)-8, '=abs('+('+'.join(valueCCP))+')', wrong_info_money)
                        worksheet.write(cont, len(col)-7, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+')*'+str(porcentaje_ingresos*100)+'%', wrong_info_money)   
                        worksheet.write(cont, len(col)-6, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(cont+1)+')', wrong_info_money)
                    rowCont = 0

                    valueCCPP = ('=Pagos_SAP!'+ccPosgradosPagos[row[col[0]]][0]) if(ccPosgradosPagos[row[col[0]]][:] != []) else 0
                    worksheet.write(cont, len(col)-5, valueCCPP, deducciones_color)
                anterior = row[col[0]]
            cont = cont + 1
        
# TOTALES EN CONCILIACION
worksheet = writer.sheets['Conciliación']

shape_sigep_size = 0
if len(shapeSIGEP) != 0:
    shape_sigep_size = shapeSIGEP[0]
shape_sap_size = 0
if len(shapeSAP) != 0:
    shape_sap_size = shapeSAP[0]

if not egresos_sigep_dataframe.empty:
    worksheet.merge_range('A'+str(cont_recaudos_ingresos+12)+':C'+str(cont_recaudos_ingresos+12), 'Más SS Social Cobrada de Mas al CC', merge_center)
    worksheet.write(cont_recaudos_ingresos+11, 4, '=SS!B'+str(shape_sap_size + shape_sigep_size + 11), money)

if(not pagosValidar.empty):
    worksheet.merge_range('A'+str(cont_recaudos_ingresos+13)+':C'+str(cont_recaudos_ingresos+13), 'Valores negativos SAP, no se registra en SIGEP', merge_center)

if not dataFrames[1].empty:
    verificaDataFrameVacio(worksheet, dataFrames[1], 4, 3, '=abs(Recaudos_SAP!B'+str(totales[1])+')', money)

verificaDataFrameVacio(worksheet, ingresos_sigep_dataframe, 4, 4, '=Ingresos_SIGEP!B'+str(totales[2]), money)
if not dataFrames[3].empty:
    verificaDataFrameVacio(worksheet, dataFrames[3], cont_recaudos_ingresos+10, 3, '=Pagos_SAP!B'+str(totales[3]+1), money)

verificaDataFrameVacio(worksheet, egresos_sigep_dataframe, cont_recaudos_ingresos+10, 4, '=Egresos_SIGEP!B'+str(totales[4]), money)


# Close the Pandas Excel writer and output the Excel file.
writer.save()
