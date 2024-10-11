import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import ImageTk for background image support


# Function to get weather data using OpenWeatherMap API
def getweatherdata(api_key, city_name):
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
        messagebox.showerror("Input Error", "All the fields are not entered kindly re-check and enter")
        return

    api_key = "api_key"
    weather_data = getweatherdata(api_key, city_name)

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
root.geometry("800x600")

# Load the background image
image = Image.open("C:\\Users\\HP\\Pictures\\1.jpg")  # Add the path to your image file
bg_image = ImageTk.PhotoImage(image)

# Create a Label widget to display the background image
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make the label cover the entire window

# Labels and Entry fields
city_label = tk.Label(root, text="Enter City Name:", bg="lightblue")
city_label.place(relx=0.1, rely=0.1)
city_label.config(font=("Roman Bold",18))
city_entry = tk.Entry(root, width=30, bg="orange")
city_entry.config(font=("JOKERMAN",20))
city_entry.place(relx=0.5, rely=0.1)

power_label = tk.Label(root, text="Power Output (W):", bg="lightblue")
power_label.place(relx=0.1, rely=0.2)
power_label.config(font=("Roman Bold",20))
power_entry = tk.Entry(root, width=30, bg="white", fg="darkblue")
power_entry.config(font=("JOKERMAN",20))
power_entry.place(relx=0.5, rely=0.2)

area_label = tk.Label(root, text="Panel Area (m²):", bg="lightblue")
area_label.place(relx=0.1, rely=0.3)
area_entry = tk.Entry(root, width=30, bg="green")
area_label.config(font=("signage",20))
area_entry.config(font=("JOKERMAN",20))
area_entry.place(relx=0.5, rely=0.3)

# Button to calculate efficiency
calculate_button = tk.Button(root, text="Calculate Efficiency", command=calculate_efficiency)
calculate_button.config(font=("Helevetica bold",20))
calculate_button.place(relx=0.4, rely=0.4)

# Result labels
result_label = tk.Label(root, text="", bg="darkblue")
result_label.config(font=("Helevetica bold",26))
result_label.place(relx=0.3, rely=0.5)

weather_label = tk.Label(root, text="", bg="lightblue")
weather_label.config(font=("Helevetica bold",20))
weather_label.place(relx=0.3, rely=0.6)

# Start the GUI loop
root.mainloop()
