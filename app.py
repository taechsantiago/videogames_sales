import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import objects_interface as oi
import objects_data as od
import pandas as pd

from dash.dependencies import Output,Input,State


app = dash.Dash(__name__)

df = od.return_data()

df_publisher = pd.DataFrame(df.groupby(['Publisher']).agg({'Publisher':'unique'}).apply(lambda x:x['Publisher'][0],axis =1),columns= ['Publisher'])
options_dropdown_publisher = [{'label':id_1,'value':id_2} for id_1,id_2 in zip(df_publisher.index,df_publisher.Publisher)]

df1 = df.groupby('Platform', as_index = True).agg({'Global_Sales':'sum'})
df2 = df.groupby('Genre', as_index = True).agg({'Global_Sales':'sum'})
df3 = df.groupby('Rank', as_index = True).agg({'Name':'sum','NA_Sales':'sum','EU_Sales':'sum','JP_Sales':'sum','Other_Sales':'sum'}).iloc[:10]
header = oi.return_header()

main = oi.return_main(df1,df2,df3,options_dropdown_publisher)
app.layout = html.Div([header, main])



#Actualización de la gráfica 
@app.callback(Output(component_id = 'graph_updating_publisher_1', component_property = 'children'),
				[Input(component_id = 'wid_select_publisher_1', component_property = 'value')])
def update_trace(publisher_select):
	print(publisher_select)
	df_sample = df[df.Publisher == publisher_select]
	global_sales_by_specific_platform = df_sample.groupby('Year', as_index = True).agg({'Global_Sales':'sum'})
	graph = dcc.Graph(figure = od.return_scatter_plot(global_sales_by_specific_platform))
	return(html.Div([graph], id = 'graph_cases_content'))


@app.callback(Output(component_id = 'graph_updating_publisher_2', component_property = 'children'),
				[Input(component_id = 'wid_select_publisher_2', component_property = 'value')])
def update_trace(publisher_select):
	print(publisher_select)
	df_sample = df[df.Publisher == publisher_select]
	global_sales_by_specific_publisher = df_sample.groupby('Genre', as_index = True).agg({'Global_Sales':'sum'})
	graph = dcc.Graph(figure = od.return_pie_plot(global_sales_by_specific_publisher))
	return(html.Div([graph], id = 'graph_cases_content'))

if __name__ == "__main__":
    app.run_server(debug=True)