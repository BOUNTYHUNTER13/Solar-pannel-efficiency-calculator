import requests
import tkinter as tk
from tkinter import messagebox

# Function to get weather data using OpenWeatherMap API
def get_weather_data(api_key, city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # Extract weather information
        temperature = data['main']['temp']  # Temperature in Celsius
        cloud_coverage = data['clouds']['all']  # Cloud coverage in percentage

        # Estimate solar irradiance based on cloud coverage
        solar_irradiance = 1000 * ((100 - cloud_coverage) / 100)

        return {
            "temperature": temperature,
            "solar_irradiance": solar_irradiance,
            "cloud_coverage": cloud_coverage
        }
    else:
        return None

# Function to calculate solar panel efficiency
def calculate_solar_efficiency(power_output, solar_irradiance, panel_area):
    if solar_irradiance == 0 or panel_area == 0:
        return 0.0
    return (power_output / (solar_irradiance * panel_area)) * 100

# Function to get data from input fields and calculate efficiency
def calculate_efficiency():
    city_name = city_entry.get()
    power_output = float(power_entry.get())
    panel_area = float(area_entry.get())
    
    if not city_name or not power_output or not panel_area:
        messagebox.showerror("Input Error", "Please fill in all the fields!")
        return
    
    api_key = "YOUR_API_KEY"  # Replace with your actual OpenWeatherMap API key
    weather_data = get_weather_data(api_key, city_name)
    
    if weather_data:
        efficiency = calculate_solar_efficiency(power_output, weather_data['solar_irradiance'], panel_area)
        
        result_label.config(text=f"Solar Panel Efficiency: {efficiency:.2f}%")
        weather_label.config(
            text=f"Weather Data for {city_name}:\n"
                 f"Temperature: {weather_data['temperature']}°C\n"
                 f"Cloud Coverage: {weather_data['cloud_coverage']}%\n"
                 f"Estimated Solar Irradiance: {weather_data['solar_irradiance']} W/m²"
        )
    else:
        messagebox.showerror("Error", "Failed to fetch weather data. Please check the city name or API key.")

# Setting up the GUI
root = tk.Tk()
root.title("Solar Panel Efficiency Calculator")
root.geometry("400x400")

# Labels and Entry fields
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=10)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

power_label = tk.Label(root, text="Power Output (W):")
power_label.pack(pady=10)
power_entry = tk.Entry(root, width=30)
power_entry.pack(pady=5)

area_label = tk.Label(root, text="Panel Area (m²):")
area_label.pack(pady=10)
area_entry = tk.Entry(root, width=30)
area_entry.pack(pady=5)

# Button to calculate efficiency
calculate_button = tk.Button(root, text="Calculate Efficiency", command=calculate_efficiency)
calculate_button.pack(pady=20)

# Result labels
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

weather_label = tk.Label(root, text="")
weather_label.pack(pady=10)

# Start the GUI loop
root.mainloop()
