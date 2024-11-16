import streamlit as st
from map import get_position_from_map
from get_weather import WeatherData
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dotenv
import os

# Ladda miljövariabler från .env-filen
dotenv.load_dotenv('.env')

def layout():
    """Skapa layouten för webapplikationen"""
    
    st.title("Delfinen - Temperature")
    st.write("Please select a location on the map to see the temperature at that location.")
    position = get_position_from_map()
    
    # Sätt standardvärden om ingen position väljs
    if position is not None:
        lat, lon = position[0], position[1]
    else:
        lat, lon = 59.3293, 18.0686  # Standardposition för Stockholm
    
    st.markdown("## Temperature")
    
    # Skapa WeatherData objekt för att hämta väderdata
    weather_data = WeatherData(lat=lat, lon=lon, api_key=os.getenv('api_key'))
    current_temp = weather_data.get_current_temp()
    
    # Kontrollera om current_temp är None och visa rätt meddelande
    if current_temp is not None:
        st.metric("Current temperature", f"{int(current_temp)} °C")
    else:
        st.metric("Current temperature", "N/A")  # Om ingen temperatur finns tillgänglig
    
    # Visa vald position
    st.write(f"Showing temperature at latitude {lat} and longitude {lon}.")
    
    st.markdown("## Hourly forecast for the next 24 hours")
    
    # Hämta väderdata för de kommande 24 timmarna
    temp_next_24h = weather_data.get_temp_next_24h()
    
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
            plt.text(df['Time'][i], df['Temperature'][i], f"{round(value)}°", fontsize=8, ha='left', va='bottom')
        
        # Anpassa diagrammets axlar och etiketter
        ax.set_xlim(min(df['Time']), max(df['Time']))
        ax.xaxis.set_tick_params(rotation=45, labelsize=9)
        ax.yaxis.set_tick_params(labelsize=9)
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        # Ta bort oviktiga ramar
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Lägg till etiketter och titel
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature forecast for the next 24 hours')
        
        # Visa diagrammet
        st.pyplot(plt)

if __name__ == "__main__":
    layout()
