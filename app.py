# Area de trabajo
import pandas as pd
import os
import numpy as np
import streamlit as st
import re
import openpyxl


# st.set_page_config(page_title='Sale Dashboars',
#                    page_icon='',
#                    layout='wide')


# -----------------------------------------------------

def data_clean(df):

        list_null=[]
        for i in range(0,len(df)):
                if type(df[2][i]) != int :
                        list_null.append(i)
        df = df.drop(list_null,axis=0).reset_index(drop=True)#.drop([0],axis=0).reset_index(drop=True)
        df=df.rename(columns={ 0: 'CODIGO', 1: 'DESCRIPCION', 2: 'PRECIO'}).infer_objects()
        # df['PRECIO'][0]
        df['CODIGO'].str.strip()
        df['DESCRIPCION'].str.strip()

        equipo=[]
        marca=[]
        procesador= []
        ram=[]

        for e in df['DESCRIPCION']:
        #EQUIPO Y MARCA
                if (e.split(' ')[0])=='ALL':
                        equipo.append('ALL IN ONE')
                        marca.append(e.split(' ')[3]) 
                else:
                        equipo.append(e.split(' ')[0])
                        marca.append(e.split(' ')[1])
                #PROCESADOR
                if e.rfind('CORE I') > 0:
                        CORE = e.rfind('CORE I')
                        procesador.append(e[CORE:CORE+7])
                elif e.rfind('RYZEN') > 0:    
                        RYZEN = e.rfind('RYZEN')
                        procesador.append(e[RYZEN:RYZEN+7])
                elif e.rfind('CELERON') > 0:    
                        CELERON = e.rfind('CELERON')
                        procesador.append(e[CELERON:CELERON+7])
                elif e.rfind('PENTIUM') > 0:    
                        PENTIUM = e.rfind('PENTIUM')
                        procesador.append(e[PENTIUM:PENTIUM+14]) 
                elif e.rfind('AMD') > 0:    
                        AMD = e.rfind('AMD')
                        procesador.append(e[AMD:AMD+3])  
                else: procesador.append(None)
                #RAM
                if e.rfind('4GB RAM') > 0:
                        GB4 = e.rfind('4GB RAM')
                        ram.append(e[GB4:GB4+7])
                elif e.rfind('8GB RAM') > 0:    
                        GB8 = e.rfind('8GB RAM')
                        ram.append(e[GB8:GB8+7])
                elif e.rfind('12GB RAM') > 0:    
                        GB12 = e.rfind('12GB RAM')
                        ram.append(e[GB12:GB12+8])
                elif e.rfind('16GB RAM') > 0:    
                        GB16 = e.rfind('16GB RAM')
                        ram.append(e[GB16:GB16+8]) 
                elif e.rfind('32GB RAM') > 0:    
                        GB32 = e.rfind('32GB RAM')
                        ram.append(e[GB32:GB32+8])       
                else: ram.append(None)

        df['EQUIPO'] = equipo
        df['MARCA'] = marca
        df['PROCESADOR'] = procesador
        df['MEMORIA']=ram

        df = df[['CODIGO','EQUIPO','MARCA','PROCESADOR','MEMORIA','PRECIO','DESCRIPCION']]
        
        return df

# -----------------------------------------------------


def display_equipo(df):
        equipo_list=['All'] + list(df['EQUIPO'].unique())
        equipo_list= st.radio('Seleccionar Equipo:',equipo_list,horizontal=True)
        
        return equipo_list

def display_marca(df,equipo):
        if equipo == 'All' :
                marca_list=['All'] + list(df['MARCA'].unique())
        if equipo != 'All' :
                marca_list=['All'] + list(df[df['EQUIPO']==f'{equipo}']['MARCA'].unique())
        marca_list= st.selectbox('Seleccionar Marca:',marca_list)

        return marca_list

def display_proc(df,equipo,marca):
        if (equipo == 'All') and (marca=='All') :
                proc_list=['All'] + list(df['PROCESADOR'].unique())
        if (equipo == 'All') and (marca!='All') :
                proc_list=['All'] + list(df[df['MARCA']==f'{marca}']['PROCESADOR'].unique())
        if (equipo != 'All') and (marca=='All') :
                proc_list=['All'] + list(df[df['EQUIPO']==f'{equipo}']['PROCESADOR'].unique())
        if (equipo != 'All') and (marca!='All') :
                proc_list=['All'] + list(df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}')]['PROCESADOR'].unique())
        

        proc_list= st.selectbox('Seleccionar Procesador:',proc_list)

        return proc_list

def display_cod(df,equipo,marca,procesador):
        if (equipo == 'All') and (marca=='All') and (procesador=='All') :
                cod_list=['All'] + list(df['CODIGO'].unique())
        if (equipo == 'All') and (marca!='All') and (procesador=='All') :
                cod_list=['All'] + list(df[df['MARCA']==f'{marca}']['CODIGO'].unique())
        if (equipo != 'All') and (marca=='All') and (procesador=='All') :
                cod_list=['All'] + list(df[df['EQUIPO']==f'{equipo}']['CODIGO'].unique())
        if (equipo != 'All') and (marca!='All') and (procesador=='All') :
                cod_list=['All'] + list(df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}')]['CODIGO'].unique())
        if (equipo != 'All') and (marca!='All') and (procesador!='All') :
                cod_list=['All'] + list(df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}') & (df['PROCESADOR']==f'{procesador}')]['CODIGO'].unique())
        if (equipo == 'All') and (marca=='All') and (procesador!='All') :
                cod_list=['All'] + list(df[(df['PROCESADOR']==f'{procesador}')]['CODIGO'].unique())
        if (equipo == 'All') and (marca!='All') and (procesador!='All') :
                cod_list=['All'] + list(df[(df['PROCESADOR']==f'{procesador}') & (df['MARCA']==f'{marca}')]['CODIGO'].unique())
        if (equipo != 'All') and (marca=='All') and (procesador!='All') :
                cod_list=['All'] + list(df[(df['PROCESADOR']==f'{procesador}') & (df['EQUIPO']==f'{equipo}')]['CODIGO'].unique())

        cod_list= st.selectbox('Seleccionar Codigo:',cod_list)

        return cod_list

def display_tables(df,equipo,marca,codigo,procesador):

        if (equipo == 'All') & (marca=='All') & (codigo=='All') & (procesador=='All')  :
                tabla = df

        if (equipo != 'All') & (marca=='All') & (codigo=='All') & (procesador=='All') :
                tabla = df[df['EQUIPO']==f'{equipo}'].drop('EQUIPO',axis=1)
        if (equipo != 'All') & (marca!='All') & (codigo=='All') & (procesador=='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}') ].drop(['EQUIPO','MARCA'],axis=1)
        if (equipo != 'All') & (marca!='All') & (codigo!='All') & (procesador=='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}') & (df['CODIGO']==f'{codigo}') ].drop(['EQUIPO','MARCA','CODIGO'],axis=1)      
        if (equipo != 'All') & (marca!='All') & (codigo!='All') & (procesador!='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}') & (df['CODIGO']==f'{codigo}') & (df['PROCESADOR']==f'{procesador}') ].drop(['EQUIPO','MARCA','CODIGO','PROCESADOR'],axis=1)    
        if (equipo != 'All') & (marca=='All') & (codigo!='All') & (procesador=='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['CODIGO']==f'{codigo}')].drop(['EQUIPO','CODIGO'],axis=1) 
        if (equipo != 'All') & (marca=='All') & (codigo!='All') & (procesador!='All') :
                tabla = df[(df['CODIGO']==f'{codigo}') & (df['EQUIPO']==f'{equipo}') &(df['PROCESADOR']==f'{procesador}')].drop(['EQUIPO','CODIGO','PROCESADOR'],axis=1)        
        if (equipo != 'All') & (marca=='All') & (codigo=='All') & (procesador!='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['PROCESADOR']==f'{procesador}') ].drop(['EQUIPO','PROCESADOR'],axis=1) 
        if (equipo != 'All') & (marca!='All') & (codigo=='All') & (procesador!='All') :
                tabla = df[(df['EQUIPO']==f'{equipo}') & (df['MARCA']==f'{marca}') & (df['PROCESADOR']==f'{procesador}') ].drop(['MARCA','EQUIPO','PROCESADOR'],axis=1)     

        if (equipo == 'All') & (marca!='All') & (codigo=='All') & (procesador=='All') :
                tabla = df[ (df['MARCA']==f'{marca}') ].drop('MARCA',axis=1)        
        if (equipo == 'All') & (marca!='All') & (codigo!='All') & (procesador=='All') :
                tabla = df[(df['MARCA']==f'{marca}') & (df['CODIGO']==f'{codigo}') ].drop(['MARCA','CODIGO'],axis=1)      
        if (equipo == 'All') & (marca!='All') & (codigo!='All') & (procesador!='All') :
                tabla = df[(df['MARCA']==f'{marca}') & (df['CODIGO']==f'{codigo}') & (df['PROCESADOR']==f'{procesador}') ].drop(['MARCA','CODIGO','PROCESADOR'],axis=1)      
        if (equipo == 'All') & (marca!='All') & (codigo=='All') & (procesador!='All') :
                tabla = df[(df['MARCA']==f'{marca}')  & (df['PROCESADOR']==f'{procesador}') ].drop(['MARCA','PROCESADOR'],axis=1)   
 

        if (equipo == 'All') & (marca=='All') & (codigo!='All') & (procesador=='All') :
                tabla = df[(df['CODIGO']==f'{codigo}') ].drop('CODIGO',axis=1)       
        if (equipo == 'All') & (marca=='All') & (codigo!='All') & (procesador!='All') :
                tabla = df[(df['CODIGO']==f'{codigo}') & (df['PROCESADOR']==f'{procesador}') ].drop(['CODIGO','PROCESADOR'],axis=1)   

        if (equipo == 'All') & (marca=='All') & (codigo=='All') & (procesador!='All') :
                tabla = df[(df['PROCESADOR']==f'{procesador}') ].drop('PROCESADOR',axis=1)   

        tabla = tabla.sort_values('PRECIO', ascending=False).reset_index(drop=True)

        return tabla


def main():

        left_column, right_column = st.columns([1,1],gap="small")
        with left_column:  st.title('LAPTOPS')
        with right_column: 
                data_file = st.file_uploader("Upload File (format: xlsx)",type=['xlsx'])
        # if
        # st.button("Process")
        if data_file is not None:
                # file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
                # st.write(file_details)
                df = pd.read_excel(data_file,header=None,usecols =[0,1,2])
                df = data_clean(df)

                st.write('---')

                left_column, right_column = st.columns([1,1],gap="small")
                with left_column:
                        equipo = display_equipo(df)
                        marca = display_marca(df,equipo)

                with right_column:
                        procesador = display_proc(df,equipo,marca)
                        codigo = display_cod(df,equipo,marca,procesador)  
                
                
                st.dataframe(display_tables(df,equipo,marca,codigo,procesador),width=None, height=None,use_container_width=False)


 

if __name__=='__main__':
    main()





