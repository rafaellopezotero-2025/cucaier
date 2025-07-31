import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output

# =====================
# Cargar datos
# =====================
url = "https://docs.google.com/spreadsheets/d/1goK-ZvnFnxwX-ohOFI39MDh00y5r8_xC5-wNP-11Sjk/export?format=csv&gid=1884402125"
df = pd.read_csv(url)

# DataFrame único de médicos (con opción TODOS)
medicos = sorted(df['medico_ref'].dropna().unique())
medicos.insert(0, "TODOS")   # opción extra
medicos_df = pd.DataFrame({'medico_ref': medicos})

# DataFrame para el gráfico de torta (diagnóstico)
diagnostico_df = df['diagnostico'].value_counts().reset_index()
diagnostico_df.columns = ['diagnostico', 'count']

# =====================
# Crear app
# =====================
app = Dash(__name__)
app.title = "Dashboard de Casos Atendidos"

app.layout = html.Div([
    html.H1("Dashboard de Casos Atendidos", style={'textAlign': 'center', 'color': '#d35400', 'fontFamily': 'Arial'}),

    html.Div([
        # Columna izquierda (gráficos)
        html.Div([
            dcc.Graph(id="grafico_tipo_tx"),
            dcc.Graph(id="grafico_estado_tx"),

            # Gráfico de torta
            dcc.Graph(
                id="grafico_diagnostico",
                figure=px.pie(
                    diagnostico_df,
                    names='diagnostico', values='count',
                    color_discrete_sequence=px.colors.sequential.OrRd,
                    title="Porcentaje de Diagnóstico sobre el total de casos"
                ).update_traces(textinfo='percent+label')
            )
        ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Columna derecha (tabla de médicos)
        html.Div([
            dash_table.DataTable(
                id='tabla_medicos',
                columns=[{"name": "Médicos", "id": "medico_ref"}],
                data=medicos_df.to_dict('records'),
                row_selectable='single',  # solo uno a la vez
                selected_rows=[0],        # por defecto "TODOS"
                style_table={'width': '100%'},
                style_cell={'textAlign': 'left', 'fontFamily': 'Arial', 'padding': '8px', 'fontSize': '16px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f5b041', 'color': 'black'},
                style_data_conditional=[
                    {'if': {'state': 'selected'}, 'backgroundColor': '#f39c12', 'color': 'white'}
                ]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'paddingLeft': '20px'})
    ], style={'margin': '20px'})
])

# =====================
# Callbacks de interacción
# =====================
@app.callback(
    Output('grafico_tipo_tx', 'figure'),
    Output('grafico_estado_tx', 'figure'),
    Input('tabla_medicos', 'selected_rows')
)
def actualizar_graficos(fila_seleccionada):
    # Si no hay médico seleccionado, usar todos
    if not fila_seleccionada:
        filtro_df = df
    else:
        medico = medicos_df.iloc[fila_seleccionada[0]]['medico_ref']
        if medico == "TODOS":
            filtro_df = df
        else:
            filtro_df = df[df['medico_ref'] == medico]

    # Gráfico tipo_tx
    tipo_tx_df = filtro_df['tipo_tx'].value_counts().reset_index()
    tipo_tx_df.columns = ['tipo_tx', 'count']
    fig_tipo_tx = px.bar(tipo_tx_df, x='tipo_tx', y='count',
                         labels={'tipo_tx': 'Tipo de Tratamiento', 'count': 'Cantidad'},
                         title="Cantidad por Tipo de Tratamiento",
                         color='tipo_tx',
                         color_discrete_sequence=px.colors.sequential.OrRd)
    fig_tipo_tx.update_traces(width=0.4, texttemplate='%{y}', textposition='outside')
    fig_tipo_tx.update_layout(height=300, title_font_color='#d35400', title_font_size=20)

    # Gráfico estado_tx
    estado_tx_df = filtro_df['estado_tx'].value_counts().reset_index()
    estado_tx_df.columns = ['estado_tx', 'count']
    fig_estado_tx = px.bar(estado_tx_df, x='estado_tx', y='count',
                           labels={'estado_tx': 'Estado del Tratamiento', 'count': 'Cantidad'},
                           title="Cantidad por Estado del Tratamiento",
                           color='estado_tx',
                           color_discrete_sequence=px.colors.sequential.OrRd)
    fig_estado_tx.update_traces(width=0.4, texttemplate='%{y}', textposition='outside')
    fig_estado_tx.update_layout(height=300, title_font_color='#d35400', title_font_size=20)

    return fig_tipo_tx, fig_estado_tx


if __name__ == "__main__":
    app.run(debug=True)
