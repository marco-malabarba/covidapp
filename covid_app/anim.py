import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime 
import numpy as np
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import os
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px  # (version 4.7.0)
from urllib.request import urlopen
import plotly.tools as tls


def printRt(x):
	if type(x)==str:
		return x
	else:
		return	str("{:.3f}".format(x))

def print_intero(x):
	if type(x)==str:
		return x
	else:
		return str('{:,}'.format(x).replace(',', '\''))

def print_frazione(x):
	if type(x)==str:
		return x
	else:
		return str("{:.1f}".format(x))

def print_variaz(x):
	if type(x)==str:
		return x
	else:
		return str('{:+,}'.format(int(x)).replace(',', '\''))
		
		
def print_variaz_perc(x):
	if type(x)==str:
		return x
	else:
		return str('{0:+.2f}'.format(x))


#with urlopen("https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson") as response:
	#regioni = json.load(response)
	
	
#https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson
	
with open('files/regioni.json') as json_file:
    regioni = json.load(json_file)
with open('files/province.json') as json_file:
    province = json.load(json_file)    


abitanti_italia=[60244639,10103969,5865544,5785861,4968410, 4907704, 4467118, 4341375, 4008296, 3722729, 1924701, 1630474, 1543127, 1518400, 1305770, 1211357, 880285, 556934, 302265, 125501, 1074819]  #fonte: https://www.tuttitalia.it/regioni/popolazione/

#abitanti_italia=[60244639,10103969,1074819]

app = dash.Dash(__name__)
pd.options.mode.chained_assignment = None

df=pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
dff=pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")


for i in range(len(df["data"])):
	index=((df["data"])[i]).find("T")
	(df["data"])[i]=((df["data"])[i])[0:index]


today=datetime.date.today()
data_in=np.datetime64('2020-02-24')

date=[]
while data_in<today:
	date.append(data_in)
	data_in+=np.timedelta64(1,'D')

for i in range(len(date)):
	date[i]=str(date[i])
valori=np.arange(0,len(date))

regioni_array=["Italia","Lombardia","Lazio","Campania","Sicilia","Veneto","Emilia-Romagna","Piemonte", "Puglia", "Toscana", "Calabria", "Sardegna", "Liguria", "Marche", "Abruzzo", "Friuli Venezia Giulia", "Umbria", "Basilicata", "Molise", "Valle d'Aosta", "Trentino-Alto Adige" ] 

#regioni_array=["Italia","Lombardia","Trentino-Alto Adige"]

valori_reg=np.arange(0,len(regioni_array))

totale=[]

for j in range(len(regioni_array)):
	ricoverati_con_sintomi=[]
	terapia_intensiva=[]
	totale_ospedalizzati=[]
	isolamento_domiciliare=[]
	totale_positivi=[]
	variazione_totale_positivi=[]
	nuovi_positivi=[]
	dimessi_guariti=[]
	deceduti=[]
	casi_da_sospetto_diagnostico=[]
	casi_da_screening=[]
	totale_casi=[]
	tamponi=[]
	casi_testati=[]

	if (j!=0 and j!=len(regioni_array)-1):
		parziale1=df[df.denominazione_regione==regioni_array[j]]
		
	if (j==0):
		parziale1=df.copy()
		
	if (j==len(regioni_array)-1):
		parziale1=df.loc[(df['denominazione_regione'] == 'P.A. Trento') | (df['denominazione_regione'] == 'P.A. Bolzano')]
		
		
	for i in range(len(date)):

		parziale=parziale1[parziale1.data==date[i]]
		ricoverati_con_sintomi.append(parziale['ricoverati_con_sintomi'].sum())
		terapia_intensiva.append(parziale['terapia_intensiva'].sum())
		totale_ospedalizzati.append(parziale['totale_ospedalizzati'].sum())
		isolamento_domiciliare.append(parziale['isolamento_domiciliare'].sum())
		totale_positivi.append(parziale['totale_positivi'].sum())
		variazione_totale_positivi.append(parziale['variazione_totale_positivi'].sum())
		nuovi_positivi.append(parziale['nuovi_positivi'].sum())
		dimessi_guariti.append(parziale['dimessi_guariti'].sum())
		deceduti.append(parziale['deceduti'].sum())
		casi_da_sospetto_diagnostico.append(parziale['casi_da_sospetto_diagnostico'].sum())
		casi_da_screening.append(parziale['casi_da_screening'].sum())
		totale_casi.append(parziale['totale_casi'].sum())
		tamponi.append(parziale['tamponi'].sum())
		casi_testati.append(parziale['casi_testati'].sum())
		

	variazione_morti=np.zeros(len(totale_positivi))
	for i in range(1,len(variazione_morti)):
		variazione_morti[i]=deceduti[i]-deceduti[i-1]

	

	tot={'Indici':valori,'Data':date,'Ricoverati con sintomi':ricoverati_con_sintomi,'Terapia intensiva':terapia_intensiva, 'Ospedalizzati':totale_ospedalizzati, 'Isolamento Domiciliare': isolamento_domiciliare, 'Attualmente positivi':totale_positivi, 'Variazione attualmente positivi': variazione_totale_positivi, 'Positivi giornalieri': nuovi_positivi, 'Guariti': dimessi_guariti, 'Deceduti':deceduti, 'casi_da_sospetto_diagnostico': casi_da_sospetto_diagnostico, 'casi_da_screening':casi_da_screening, 'Totale casi':totale_casi, 'Tamponi':tamponi, 'Casi testati':casi_testati, 'Deceduti giornalieri':variazione_morti}

	tot = pd.DataFrame(tot)
	totale.append(tot) 




app.layout = html.Div(className='row', children=[

    html.H1(id='titolo', style={'text-align': 'center','margin':30}),
    html.Div(children=[
    dcc.Dropdown(id="seleziona giorno",
                 options=[

                 {"label": date[i], "value": valori[i]} for i in range(len(date))],
                 multi=False,
                 value=valori[len(valori)-1], searchable=False,
                 style={'width': "50%",'display': 'inline-block','text-align': 'left'},
                 ),
    dcc.Dropdown(id="seleziona regione",
                 options=[

                 {"label": regioni_array[i], "value": valori_reg[i]} for i in range(len(regioni_array))],
                 multi=False,
                 value=valori_reg[0], searchable=False,
                 style={'width': "50%",'display': 'inline-block','text-align': 'center'},
                 ),
    ]),
    html.Div(children=[
    html.Div(id='output_container', children=[], style={'width': "50%",'display': 'inline-block','text-align': 'left'},),
    html.Div(id='output_regione', children=[],style={'width': "50%",'display': 'inline-block','text-align': 'center'},),
    ]),
    html.Div(children=[
    dcc.Markdown(id='markyy',style={"height" : "100%","width":"45%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
    dcc.Graph(id='mappa', figure={},style={"height" : "100%", "width":"45%",'display': 'inline-block',}),

    ]),
    

    
    #html.Br(),
    html.Div(children=[
    dcc.Graph(id='contagi',figure={},style={"height" : "100%",  "width":"60%",'display': 'inline-block',}),
    dcc.Markdown(id='trasm' ,style={ "height" : "100%","width":"35%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
   ]),
   
   html.Div(children=[
    dcc.Graph(id='t_i',figure={},style={"height" : "100%",  "width":"60%",'display': 'inline-block',}),
    dcc.Markdown(id='ter_int' ,style={ "height" : "100%","width":"35%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
   ]),
   
   html.Div(children=[
    dcc.Graph(id='osp',figure={},style={"height" : "100%",  "width":"60%",'display': 'inline-block',}),
    dcc.Markdown(id='osped' ,style={ "height" : "100%","width":"35%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
   ]),
   
   html.Div(children=[
    dcc.Graph(id='var_pos',figure={},style={"height" : "100%",  "width":"60%",'display': 'inline-block',}),
    dcc.Markdown(id='variaz_pos' ,style={ "height" : "100%","width":"35%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
   ]),
   
   html.Div(children=[
    dcc.Graph(id='morti',figure={},style={"height" : "100%",  "width":"60%",'display': 'inline-block',}),
    dcc.Markdown(id='mort' ,style={ "height" : "100%","width":"35%",'display': 'inline-block','verticalAlign': 'top','text-align': 'center',"color":"black"}),
   ]),
   
  dcc.Markdown("## Grafici riepilogativi" ,style={ "height" : "100%","width":"100%",'verticalAlign': 'center','text-align': 'center',"color":"black"}),
  
  html.Div(children=[
    dcc.Graph(id='totale_casi',figure={},style={"height" : "100%",  "width":"50%",'display': 'inline-block',}),
    dcc.Graph (id='totale_morti',figure={},style={"height" : "100%",  "width":"50%",'display': 'inline-block',}),
   ]),
   
   html.Div(children=[
    dcc.Graph(id='totale_guariti',figure={},style={"height" : "100%",  "width":"50%",'display': 'inline-block',}),
    dcc.Graph (id='totale_tamponi',figure={},style={"height" : "100%",  "width":"50%",'display': 'inline-block',}),
   ]),
  
  
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    Output(component_id='titolo', component_property='children'),
    Output(component_id='output_container', component_property='children'),
    Output(component_id='output_regione', component_property='children'),
    Output(component_id='markyy', component_property='children'),
    Output(component_id='mappa', component_property='figure'),
    Output(component_id='contagi', component_property='figure'),
    Output(component_id='trasm', component_property='children'),
    Output(component_id='t_i', component_property='figure'),
    Output(component_id='ter_int', component_property='children'), 
    Output(component_id='osp', component_property='figure'),   
    Output(component_id='osped', component_property='children'),
    Output(component_id='var_pos', component_property='figure'),
    Output(component_id='variaz_pos', component_property='children'),       
    Output(component_id='morti', component_property='figure'),
    Output(component_id='mort', component_property='children'),
    Output(component_id='totale_casi', component_property='figure'),
    Output(component_id='totale_morti', component_property='figure'),
    Output(component_id='totale_guariti', component_property='figure'),
    Output(component_id='totale_tamponi', component_property='figure'),
    Input(component_id='seleziona giorno', component_property='value'),
    Input(component_id='seleziona regione', component_property='value'),
)
def update_graph(option_slctd,reg_slctd):

	intero=int(option_slctd)
	data_str=date[intero]   
	container = "Il giorno selezionato è: {}".format(data_str)
	
	intero_2=int(reg_slctd)
	regione_sel="La regione selezionata è: {}".format(regioni_array[intero_2])
	
	titolo="Covid-19 "+regioni_array[intero_2]
	if (intero_2==0):
		dati=df[df.data==data_str]
		i1=dati[dati["denominazione_regione"]=="P.A. Bolzano"].index[0]
		i2=dati[dati["denominazione_regione"]=="P.A. Trento"].index[0]
		val1=int(dati.loc[i1].at['totale_positivi'])
		val2=int(dati.loc[i2].at['totale_positivi'])
		dati=dati.append({'data' : data_str , 'denominazione_regione' : 'Trentino-Alto Adige','totale_positivi':val1+val2}, ignore_index=True)
		
		fig1 = px.choropleth_mapbox(
        	data_frame=dati,
        	geojson=regioni,
        	locations='denominazione_regione',
        	color='totale_positivi',
        	featureidkey="properties.reg_name",
        	mapbox_style="carto-positron",
        	color_continuous_scale=px.colors.sequential.YlOrRd,
        	labels={'totale_positivi': 'Attualmente positivi','denominazione_regione': 'Regione'},
        	center = {"lat": (max(dati["lat"])+min(dati["lat"]))/2, "lon": (max(dati["long"])+min(dati["long"]))/2},zoom=3.7,opacity=0.9,title='<b>Distribuzione attualmente positivi</b>',
    	)
    	
	if (intero_2==len(regioni_array)-1):
		datii=dff.loc[(dff['denominazione_provincia'] == "Bolzano") | (dff['denominazione_provincia'] == "Trento")]
		dati=datii.loc[datii['data'].str.contains(data_str)]
		
		fig1 = px.choropleth_mapbox(
        	data_frame=dati,
        	geojson=province,
        	locations='denominazione_provincia',
        	color='totale_casi',
        	featureidkey="properties.prov_name",
        	mapbox_style="carto-positron",
        	color_continuous_scale=px.colors.sequential.YlOrRd,
        	labels={'totale_casi': 'Totale casi','denominazione_provincia': 'Provincia'},
        	center = {"lat": (max(dati["lat"])+min(dati["lat"]))/2, "lon": (max(dati["long"])+min(dati["long"]))/2},zoom=5.9,opacity=0.9, title='<b>Distribuzione casi totali</b>',
    	)
	
	if (intero_2!=0 and intero_2!=len(regioni_array)-1):
		dati=dff.loc[(dff['data'].str.contains(data_str)) & (dff['denominazione_regione'] == regioni_array[intero_2])]
		fig1 = px.choropleth_mapbox(
        	data_frame=dati,
        	geojson=province,
        	locations='denominazione_provincia',
        	color='totale_casi',
        	featureidkey="properties.prov_name",
        	mapbox_style="carto-positron",
        	color_continuous_scale=px.colors.sequential.YlOrRd,
        	labels={'totale_casi': 'Totale casi','denominazione_provincia': 'Provincia'},
        	center = {"lat": (max(dati["lat"])+min(dati["lat"]))/2, "lon": (max(dati["long"])+min(dati["long"]))/2},zoom=5.9,opacity=0.9, title='<b>Distribuzione casi totali</b>',
    	)
	
	
	
	
	fig1.update_layout(
    #height=400,
    title=dict(
        #text='<b>Distribuzione attualmente positivi</b>',
        x=0.5,
        #y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)


    	
    	
    	
	totale_cut=totale[intero_2].copy()
	totale_cut= totale_cut[totale_cut.Indici <= intero]
    	
	fig2 = px.line(
        data_frame=totale_cut,
        x="Data",y="Positivi giornalieri",color_discrete_sequence=["orange"]
       
    )
  
  
	markdown='\n\t'+'\n'+"### ATTUALMENTE POSITIVI: "+str('{:,}'.format(totale_cut["Attualmente positivi"][intero]).replace(',', '\''))+'\n' + "#### CASI TOTALI: "+str('{:,}'.format(totale_cut["Totale casi"][intero]).replace(',', '\'')) +'\n'+ "#### GUARITI: "+ str('{:,}'.format(totale_cut["Guariti"][intero]).replace(',', '\''))+'\n'+ "#### DECEDUTI: "+str('{:,}'.format(totale_cut["Deceduti"][intero]).replace(',', '\''))
	
	
	var_0_7=0
	var_0_14=0
	c_0_7=0
	c_7_14=0
	c_0_14=0
	c_14_28=0
	m_7=0
	m_14=0
	i=0
	
	
	
	if intero<7:
		c_0_7="N/D"
		m_7="N/D"
		var_0_7="N/D"
		c_0_14="N/D"
		m_14="N/D"
		var_0_14="N/D"
		c_7_14="N/D"
		c_14_28="N/D"
		
		Rt_2w="N/D"
		Rt_1w="N/D"
		frac_7="N/D"
		frac_14="N/D"
		frac_m7="N/D"
		frac_m14="N/D"
		var_per_7="N/D"
		var_per_14="N/D"
		
		ti_7="N/D"
		ti_14="N/D"
		osp_7="N/D"
		osp_14="N/D"
		
	else: 
	
	
		
		while (i<7):
			c_0_7+=totale[intero_2]["Positivi giornalieri"][intero-i]
			m_7+=totale[intero_2]["Deceduti giornalieri"][intero-i]
			var_0_7+=totale[intero_2]["Variazione attualmente positivi"][intero-i]
			c_0_14+=totale[intero_2]["Positivi giornalieri"][intero-i]
			var_0_14+=totale[intero_2]["Variazione attualmente positivi"][intero-i]
			m_14+=totale[intero_2]["Deceduti giornalieri"][intero-i]
			i+=1
			
		frac_7=(c_0_7/abitanti_italia[intero_2]*100000)
		frac_m7=(m_7/abitanti_italia[intero_2]*100000)
		var_per_7=(totale[intero_2]["Attualmente positivi"][intero]/totale[intero_2]["Attualmente positivi"][intero-7])*100-100
		ti_7=totale[intero_2]["Terapia intensiva"][intero]/totale[intero_2]["Terapia intensiva"][intero-7]*100-100
		osp_7=totale[intero_2]["Ospedalizzati"][intero]/totale[intero_2]["Ospedalizzati"][intero-7]*100-100
		
	if intero<14:

		c_0_14="N/D"
		m_14="N/D"
		var_0_14="N/D"
		c_7_14="N/D"
		c_14_28="N/D"
		
		Rt_2w="N/D"
		Rt_1w="N/D"
		frac_14="N/D"
		frac_m14="N/D"
		var_per_14="N/D"
		
		ti_14="N/D"
		osp_14="N/D"
			
	else:
		while (i<14):
			c_0_14+=totale[intero_2]["Positivi giornalieri"][intero-i]
			var_0_14+=totale[intero_2]["Variazione attualmente positivi"][intero-i]
			m_14+=totale[intero_2]["Deceduti giornalieri"][intero-i]
			c_7_14+=totale[intero_2]["Positivi giornalieri"][intero-i]
			i+=1
			
		Rt_1w=c_0_7/c_7_14
		frac_14=(c_0_14/abitanti_italia[intero_2]*100000)
		frac_m14=m_14/abitanti_italia[intero_2]*100000
		var_per_14=(totale[intero_2]["Attualmente positivi"][intero]/totale[intero_2]["Attualmente positivi"][intero-14])*100-100
		ti_14=totale[intero_2]["Terapia intensiva"][intero]/totale[intero_2]["Terapia intensiva"][intero-14]*100-100
		osp_14=totale[intero_2]["Ospedalizzati"][intero]/totale[intero_2]["Ospedalizzati"][intero-14]*100-100
		
		
	if intero<28:
		Rt_2w="N/D"
		c_14_28="N/D"
	
	else:
		while (i<28):
			c_14_28+=totale[intero_2]["Positivi giornalieri"][intero-i]
			i+=1
		
		Rt_2w=c_0_14/c_14_28

	


	
	
	
	
	
	
	trasm="### R (2 weeks) = " + printRt(Rt_2w) + '\n' + "### R (1 week) = " + printRt(Rt_1w) +'\n'+'\n'+ '\n' +"#### Contagiati ultima settimana: "+ print_intero(c_0_7) + " ("+print_frazione(frac_7)+" contagiati per 100k abitanti)" + '\n' +"#### Contagiati ultime due settimane: "+ print_intero(c_0_14) + " ("+print_frazione(frac_14)+" contagiati per 100k abitanti)"

	mort="### Mortalità = "+str("{:.2f}".format(totale[intero_2]["Deceduti"][intero]/totale[intero_2]["Totale casi"][intero]*100))+"%"+'\n'+"#### Deceduti ultima settimana: "+print_intero(m_7) + " ("+print_frazione(frac_m7)+" deceduti per 100k abitanti)"+'\n'+"#### Deceduti ultime due settimane: "+ print_intero(m_14) + " ("+print_frazione(frac_m14)+" deceduti per 100k abitanti)"

	ter_int="### Percentuali positivi in terapia intensiva: " + str("{:.2f}".format(totale[intero_2]["Terapia intensiva"][intero]/totale[intero_2]["Attualmente positivi"][intero]*100))+"%"+'\n'+"#### Variazione numero pazienti in terapia intensiva nell'ultima settimana: "+print_variaz_perc(ti_7)+"%" +'\n'+"#### Variazione numero pazienti in terapia intensiva nelle ultime due settimane: "+print_variaz_perc(ti_14)+"%" 

	osped="### Percentuali positivi ospedalizzati: " + str("{:.2f}".format(totale[intero_2]["Ospedalizzati"][intero]/totale[intero_2]["Attualmente positivi"][intero]*100))+"%"+'\n'+"#### Variazione numero pazienti ospedalizzati nell'ultima settimana: "+print_variaz_perc(osp_7) +"%" +'\n'+"#### Variazione numero pazienti ospedalizzati nelle ultime due settimane: "+print_variaz_perc(osp_14) +"%" 


	variaz_pos="#### Variazione attualmente positivi nell'ultima settimana: " + print_variaz(var_0_7)+" ("+print_variaz_perc(var_per_7)+"%)"+'\n'"#### Variazione degli attualmente positivi nelle ultime due settimane: " + print_variaz(var_0_14) +" ("+print_variaz_perc(var_per_14)+"%)"
	

		

	fig2.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento positivi giornalieri</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)

	figti = px.line(
        data_frame=totale_cut,
        x="Data",y="Terapia intensiva",color_discrete_sequence=["brown"]
       
    )
  
  
	figti.update_layout(
    height=400,
    title=dict(
        text='<b>Pazienti in terapia intensiva</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)
	fosp = px.line(
        data_frame=totale_cut,
        x="Data",y="Ospedalizzati",color_discrete_sequence=["purple"]
       
    )
  
  
	fosp.update_layout(
    height=400,
    title=dict(
        text='<b>Pazienti ospedalizzati</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)
	figvarpos = px.line(
        data_frame=totale_cut,
        x="Data",y="Attualmente positivi",color_discrete_sequence=["magenta"]
       
    )
  
  
	figvarpos.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento attualmente positivi</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)

	fig3 = px.line(
        data_frame=totale_cut,
        x="Data",y="Deceduti giornalieri",color_discrete_sequence=["gray"]
       
    )
    
	fig3.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento deceduti giornalieri</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
)
    
	fig_totalecasi = px.line(
        data_frame=totale_cut,
        x="Data",y="Totale casi", color_discrete_sequence=["red"]
       
    )
    
	fig_totalecasi.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento totale casi registrati</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
)
    
	fig_totalemorti = px.line(
        data_frame=totale_cut,
        x="Data",y="Deceduti",color_discrete_sequence=["black"]
       
    )
    
	fig_totalemorti.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento deceduti</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
)
	fig_totaleguariti = px.line(
        data_frame=totale_cut,
        x="Data",y="Guariti",color_discrete_sequence=["green"],
       
    )
    
	fig_totaleguariti.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento guariti</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),
)

	fig_totaletamponi = px.line(
        data_frame=totale_cut,
        x="Data",y="Tamponi"
       
    )
    
	fig_totaletamponi.update_layout(
    height=400,
    title=dict(
        text='<b>Andamento tamponi totali effettuati</b>',
        x=0.5,
        y=0.95,
        font=dict(
            family="Arial",
            size=20,
            color='black'
        )
    ),

)
   
	return titolo,container, regione_sel, markdown, fig1,fig2, trasm, figti, ter_int, fosp, osped, figvarpos, variaz_pos, fig3, mort, fig_totalecasi, fig_totalemorti, fig_totaleguariti, fig_totaletamponi
	
	

if __name__ == '__main__':
    app.run_server(debug=True)






