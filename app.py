import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import numpy as np  
import joblib

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
])


model = joblib.load("model.pkl")

# # Define custom CSS styles
# app.css.append_css({
#     'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
# })

# Define the layout of the app
app.layout = html.Div(
    style={
        'font-family': 'Arial, sans-serif',
        'backgroundColor': '#f4f4f4',
        'padding': '50px',
        'text-align': 'center'
    },
    children=[
        html.Div(
            [
                html.H1(
                    "Real Estate Price Prediction",
                    style={
                        'color': '#007BFF',
                        'font-size': '36px',
                        'margin-bottom': '20px'
                    }
                ),

                html.Div(
                    [
                        dcc.Input(
                            id='house_age',
                            type='number',
                            placeholder='House Age (age)',
                            style={
                                'margin': '10px',
                                'padding': '15px',
                                'width': '250px',
                                'border-radius': '5px',
                                'border': '2px solid #007BFF',
                                'font-size': '16px'
                            }
                        ),
                        
                        
                        dcc.Input(
                            id='distance_to_mrt',
                            type='number',
                            placeholder='Distance to MRT Station (meters)',
                            style={
                                'margin': '10px',
                                'padding': '15px',
                                'width': '250px',
                                'border-radius': '5px',
                                'border': '2px solid #007BFF',
                                'font-size': '16px'
                            }
                        ),
                        dcc.Input(
                            id='num_convenience_stores',
                            type='number',
                            placeholder='Number of Convenience Stores',
                            style={
                                'margin': '10px',
                                'padding': '15px',
                                'width': '250px',
                                'border-radius': '5px',
                                'border': '2px solid #007BFF',
                                'font-size': '16px'
                            }
                        ),
                        dcc.Input(
                            id='latitude',
                            type='number',
                            placeholder='Latitude',
                            style={
                                'margin': '10px',
                                'padding': '15px',
                                'width': '250px',
                                'border-radius': '5px',
                                'border': '2px solid #007BFF',
                                'font-size': '16px'
                            }
                        ),
                        dcc.Input(
                            id='longitude',
                            type='number',
                            placeholder='Longitude',
                            style={
                                'margin': '10px',
                                'padding': '15px',
                                'width': '250px',
                                'border-radius': '5px',
                                'border': '2px solid #007BFF',
                                'font-size': '16px'
                            }
                        ),
                        html.Button(
                            'Predict Price',
                            id='predict_button',
                            n_clicks=0,
                            style={
                                'margin': '10px',
                                'padding': '15px 30px',
                                'background-color': '#007BFF',
                                'color': 'white',
                                'border': 'none',
                                'border-radius': '5px',
                                'font-size': '18px',
                                'cursor': 'pointer',
                                'transition': 'background-color 0.3s'
                            }
                        ),
                    ],
                    style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap'}
                ),
                
                html.Div(
                    id='prediction_output',
                    style={
                        'text-align': 'center',
                        'font-size': '20px',
                        'margin-top': '20px',
                        'padding': '15px',
                        'border': '2px solid #007BFF',
                        'border-radius': '5px',
                        'background-color': '#e7f3ff',
                        'color': '#007BFF'
                    }
                )
            ],
            style={
                'width': '60%',
                'margin': '0 auto',
                'background-color': 'white',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 10px rgba(0,0,0,0.1)'
            }
        )
    ]
)

# Define callback to update output
@app.callback(
    Output('prediction_output', 'children'),
    [Input('predict_button', 'n_clicks')],
    [State('house_age', 'value'), 
    State('distance_to_mrt', 'value'), 
    State('num_convenience_stores', 'value'),
    State('latitude', 'value'),
    State('longitude', 'value')]
)
def update_output(n_clicks, house_age, distance_to_mrt, num_convenience_stores, latitude, longitude):
    if n_clicks > 0 and all(v is not None for v in [house_age, distance_to_mrt, num_convenience_stores, latitude, longitude]):
        # Prepare the feature vector
        features = pd.DataFrame([[house_age, distance_to_mrt, num_convenience_stores, latitude, longitude]], 
                                columns=['House age', 'Distance to the nearest MRT station', 'Number of convenience stores', 'Latitude', 'Longitude'])
        try:
            # Predict
            prediction = model.predict(features)[0]  
            return f'Predicted House Price of Unit Area: {prediction:.2f}'
        except Exception as e:
            return f'Error during prediction: {str(e)}'
    elif n_clicks > 0:
        return 'Please enter all values to get a prediction'
    return ''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)