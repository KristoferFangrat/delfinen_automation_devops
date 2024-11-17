import streamlit as st
from map import get_position_from_map
from get_weather import WeatherData
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dotenv
import os

dotenv.load_dotenv('.env')


def layout():
    """create the layout for the web application"""

    st.title("Delfinen - Temperature")
    st.write("Please select a location on the map to see the temperature at that location.")
    position = get_position_from_map()
    if position is not None:
        lat, lon = position[0], position[1]
    else:
        lat, lon = 59.3293, 18.0686
        
    st.markdown("## Temperature")
    weather_data = WeatherData(lat=lat, lon=lon, api_key=os.getenv('api_key'))
    current_temp = weather_data.get_current_temp()
    
    # Kontrollera om current_temp är None
    if current_temp is not None:
        try:
            st.metric("Current temperature", f"{int(current_temp)} °C")
        except (TypeError, ValueError) as e:
            st.metric("Current temperature", "N/A")
            st.error(f"Error converting current temperature: {e}")
    else:
        st.metric("Current temperature", "N/A")
    
    st.write(f"Showing temperature at latitude {lat} and longitude {lon}.")

    st.markdown("## Hourly forecast for the next 24 hours")
    
    # Hämta väderdata för de kommande 24 timmarna
    temp_next_24h = weather_data.get_temp_next_24h()
    
    # Kontrollera om temp_next_24h innehåller None-värden
    if temp_next_24h is None or any(temp is None for _, temp in temp_next_24h):
        st.write("Temperature data is not available for the next 24 hours.")
        return
    
    # Skapa två kolumner för att visa data och grafik
    col1, col2 = st.columns([2, 1])

    with col2:
        # Visa en DataFrame med temperaturer för de kommande 24 timmarna
        df = pd.DataFrame(temp_next_24h, columns=['Time', 'Temperature'])
        st.write(df)

    with col1:
        # Skapa och visa en linjediagram för temperaturförutsägelser
        fig, ax = plt.subplots()
        ax.plot(df['Time'], df['Temperature'])
        
        # Lägg till temperaturvärden på linjediagrammet
        for i, value in enumerate(df['Temperature']):
            if value is not None:
                plt.text(df['Time'][i], df['Temperature'][i], f"{round(value)}°", fontsize=8, ha='left', va='bottom')
        
        # Anpassa diagrammets axlar och etiketter
        ax.set_xlim(min(df['Time']), max(df['Time']))
        ax.xaxis.set_tick_params(rotation=45, labelsize=9)
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Hourly Temperature Forecast")
        
        st.pyplot(fig)

if __name__ == '__main__':
    layout()