import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Leer datos
url = "https://docs.google.com/spreadsheets/d/1goK-ZvnFnxwX-ohOFI39MDh00y5r8_xC5-wNP-11Sjk/export?format=csv&gid=1884402125"
df = pd.read_csv(url)

# DataFrames preparados para los gráficos
tipo_tx_df = df['tipo_tx'].value_counts().reset_index()
tipo_tx_df.columns = ['tipo_tx', 'count']   # 🔹 renombramos columnas

diagnostico_df = df['diagnostico'].value_counts().reset_index()
diagnostico_df.columns = ['diagnostico', 'count']

estado_tx_df = df['estado_tx'].value_counts().reset_index()
estado_tx_df.columns = ['estado_tx', 'count']

# Crear app
app = Dash(__name__)
app.title = "Dashboard de Casos Atendidos"

app.layout = html.Div([
    html.H1("Dashboard de Casos Atendidos", style={'textAlign': 'center'}),

    # Gráfico de barras por tipo_tx
    dcc.Graph(
        figure=px.bar(
            tipo_tx_df,
            x='tipo_tx', y='count',
            labels={'tipo_tx': 'Tipo de Trasplante', 'count': 'Cantidad'},
            title="Cantidad por Tipo de Trasplante"
        )
    ),

    # Gráfico de torta por diagnóstico
    dcc.Graph(
        figure=px.pie(
            diagnostico_df,
            names='diagnostico', values='count',
            title="Porcentaje de Diagnóstico sobre el total de casos"
        ).update_traces(textinfo='percent+label')
    ),

    # Gráfico de barras por estado_tx
    dcc.Graph(
        figure=px.bar(
            estado_tx_df,
            x='estado_tx', y='count',
            labels={'estado_tx': 'Estado del Tratamiento', 'count': 'Cantidad'},
            title="Cantidad por Estado del Tratamiento"
        )
    )
])

if __name__ == "__main__":
    app.run(debug=True)
