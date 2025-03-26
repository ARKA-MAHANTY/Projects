import random
import math
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class IoTSensorNetwork:
    def __init__(self):
        self.sensors = {
            'traffic': {'vehicle_count': 100, 'avg_speed': 40},
            'air_quality': {'pm2_5': 35, 'co2': 450},
            'temperature': {'value': 22},
            'humidity': {'value': 65},
            'noise': {'db_level': 55}
        }
        
    def collect_data(self):
        self.sensors['traffic']['vehicle_count'] = max(10, 
            self.sensors['traffic']['vehicle_count'] + random.randint(-5, 5))
        self.sensors['traffic']['avg_speed'] = max(10, min(80, 
            self.sensors['traffic']['avg_speed'] + random.uniform(-2, 2)))
        self.sensors['air_quality']['pm2_5'] = max(5, 
            self.sensors['air_quality']['pm2_5'] + random.uniform(-2, 2))
        self.sensors['air_quality']['co2'] = max(300, 
            self.sensors['air_quality']['co2'] + random.uniform(-10, 10))
        self.sensors['temperature']['value'] = max(-10, min(40, 
            self.sensors['temperature']['value'] + random.uniform(-0.5, 0.5)))
        self.sensors['humidity']['value'] = max(10, min(95, 
            self.sensors['humidity']['value'] + random.uniform(-2, 2)))
        self.sensors['noise']['db_level'] = max(30, min(90, 
            self.sensors['noise']['db_level'] + random.uniform(-1, 1)))
        
        return self.sensors

class LocationDatabase:
    INDIAN_CITIES = {
        "Delhi": {"type": "Capital Territory", "population": "31 million", "landmark": "India Gate"},
        "Mumbai": {"type": "Metro City", "population": "20 million", "landmark": "Gateway of India"},
        "Bangalore": {"type": "IT Hub", "population": "12 million", "landmark": "Vidhana Soudha"},
        "Chennai": {"type": "Coastal City", "population": "10 million", "landmark": "Marina Beach"},
        "Kolkata": {"type": "Cultural Capital", "population": "15 million", "landmark": "Howrah Bridge"},
        "Hyderabad": {"type": "IT & Pharma Hub", "population": "9 million", "landmark": "Charminar"},
        "Jaipur": {"type": "Tourist City", "population": "4 million", "landmark": "Hawa Mahal"},
        "Ahmedabad": {"type": "Business Hub", "population": "7 million", "landmark": "Sabarmati Ashram"}
    }
    
    WORLD_CAPITALS = {
        "Tokyo": {"country": "Japan", "population": "37 million", "landmark": "Tokyo Tower"},
        "London": {"country": "UK", "population": "9 million", "landmark": "Big Ben"},
        "Paris": {"country": "France", "population": "11 million", "landmark": "Eiffel Tower"},
        "Washington D.C.": {"country": "USA", "population": "7 million", "landmark": "White House"},
        "Beijing": {"country": "China", "population": "21 million", "landmark": "Forbidden City"},
        "Berlin": {"country": "Germany", "population": "4 million", "landmark": "Brandenburg Gate"},
        "Moscow": {"country": "Russia", "population": "12 million", "landmark": "Red Square"},
        "Canberra": {"country": "Australia", "population": "0.5 million", "landmark": "Parliament House"}
    }

class SmartCityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart City IoT Dashboard")
        self.sensor_network = IoTSensorNetwork()
        self.locations = LocationDatabase()
        
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_dashboard_tab()
        self.create_indian_cities_tab()
        self.create_world_capitals_tab()
        
        self.update_dashboard()
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        main_frame = ttk.Frame(self.dashboard_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_sensor_display(main_frame)
        self.create_traffic_graph(main_frame)
    
    def create_indian_cities_tab(self):
        """Create tab for Indian cities information"""
        self.india_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.india_tab, text="Indian Cities")
        
        container = ttk.Frame(self.india_tab)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for city, info in self.locations.INDIAN_CITIES.items():
            city_frame = ttk.LabelFrame(scrollable_frame, text=city, padding="10")
            city_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(city_frame, text=f"Type: {info['type']}").pack(anchor=tk.W)
            ttk.Label(city_frame, text=f"Population: {info['population']}").pack(anchor=tk.W)
            ttk.Label(city_frame, text=f"Famous Landmark: {info['landmark']}").pack(anchor=tk.W)
            
            ttk.Separator(city_frame).pack(fill=tk.X, pady=5)
    
    def create_world_capitals_tab(self):
        """Create tab for world capitals information"""
        self.world_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.world_tab, text="World Capitals")
        
        container = ttk.Frame(self.world_tab)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for capital, info in self.locations.WORLD_CAPITALS.items():
            capital_frame = ttk.LabelFrame(scrollable_frame, text=capital, padding="10")
            capital_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(capital_frame, text=f"Country: {info['country']}").pack(anchor=tk.W)
            ttk.Label(capital_frame, text=f"Population: {info['population']}").pack(anchor=tk.W)
            ttk.Label(capital_frame, text=f"Famous Landmark: {info['landmark']}").pack(anchor=tk.W)
            
            ttk.Separator(capital_frame).pack(fill=tk.X, pady=5)
    
    def create_sensor_display(self, parent):
        """Create sensor value display frames"""
        sensor_frame = ttk.Frame(parent)
        sensor_frame.pack(fill=tk.X, pady=10)
        
        traffic_frame = ttk.LabelFrame(sensor_frame, text="Traffic Monitoring", padding="10")
        traffic_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(traffic_frame, text="Vehicle Count:").grid(row=0, column=0, sticky=tk.W)
        self.traffic_label = ttk.Label(traffic_frame, text="100", font=('Arial', 12, 'bold'))
        self.traffic_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(traffic_frame, text="Avg Speed (km/h):").grid(row=1, column=0, sticky=tk.W)
        self.speed_label = ttk.Label(traffic_frame, text="40.0", font=('Arial', 12, 'bold'))
        self.speed_label.grid(row=1, column=1, sticky=tk.W)
        
        air_frame = ttk.LabelFrame(sensor_frame, text="Air Quality", padding="10")
        air_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(air_frame, text="PM2.5 (µg/m³):").grid(row=0, column=0, sticky=tk.W)
        self.pm25_label = ttk.Label(air_frame, text="35.0", font=('Arial', 12, 'bold'))
        self.pm25_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(air_frame, text="CO2 (ppm):").grid(row=1, column=0, sticky=tk.W)
        self.co2_label = ttk.Label(air_frame, text="450", font=('Arial', 12, 'bold'))
        self.co2_label.grid(row=1, column=1, sticky=tk.W)
        
        env_frame = ttk.LabelFrame(sensor_frame, text="Environment", padding="10")
        env_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(env_frame, text="Temperature (°C):").grid(row=0, column=0, sticky=tk.W)
        self.temp_label = ttk.Label(env_frame, text="22.0", font=('Arial', 12, 'bold'))
        self.temp_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(env_frame, text="Humidity (%):").grid(row=1, column=0, sticky=tk.W)
        self.humidity_label = ttk.Label(env_frame, text="65", font=('Arial', 12, 'bold'))
        self.humidity_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(env_frame, text="Noise (dB):").grid(row=2, column=0, sticky=tk.W)
        self.noise_label = ttk.Label(env_frame, text="55", font=('Arial', 12, 'bold'))
        self.noise_label.grid(row=2, column=1, sticky=tk.W)
    
    def create_traffic_graph(self, parent):
        """Create a simple traffic graph using tkinter Canvas"""
        self.graph_frame = ttk.LabelFrame(parent, text="Traffic Pattern", padding="10")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.canvas = tk.Canvas(self.graph_frame, bg='white', height=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.create_text(30, 10, text="Vehicles", anchor=tk.NW, angle=90)
        self.canvas.create_text(40, 190, text="Hour of Day", anchor=tk.NW)
        
        self.draw_axes()
    
    def draw_axes(self):
        """Draw graph axes and hour markers"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        self.canvas.delete("all")
        
        self.canvas.create_line(50, 30, 50, height-30, width=2)  # Y-axis
        self.canvas.create_line(50, height-30, width-20, height-30, width=2)  # X-axis
        
        for hour in range(0, 24, 3):
            x = 50 + (width-70) * hour / 23
            self.canvas.create_line(x, height-30, x, height-25, width=2)
            self.canvas.create_text(x, height-20, text=str(hour))
    
    def draw_traffic_graph(self, current_traffic, current_hour):
        """Draw traffic pattern graph using tkinter Canvas"""
        self.draw_axes()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        points = []
        for hour in range(24):
            x = 50 + (width-70) * hour / 23
            y = height-30 - (height-60) * (50 + 30 * math.sin(hour/24*2*math.pi)) / 100
            points.extend([x, y])
        
        self.canvas.create_line(*points, fill='blue', width=2, smooth=True)
        
        x = 50 + (width-70) * current_hour / 23
        y = height-30 - (height-60) * current_traffic / 100
        self.canvas.create_oval(x-4, y-4, x+4, y+4, fill='red', outline='red')
        
        self.canvas.create_text(width-100, 40, text="Typical Traffic", fill='blue', anchor=tk.W)
        self.canvas.create_text(width-100, 60, text="Current Traffic", fill='red', anchor=tk.W)

    def update_dashboard(self):
        """Update all dashboard elements"""
        sensor_data = self.sensor_network.collect_data()
        current_hour = datetime.now().hour
        
        self.traffic_label.config(text=str(int(sensor_data['traffic']['vehicle_count'])))
        self.speed_label.config(text=f"{sensor_data['traffic']['avg_speed']:.1f}")
        self.pm25_label.config(text=f"{sensor_data['air_quality']['pm2_5']:.1f}")
        self.co2_label.config(text=str(int(sensor_data['air_quality']['co2'])))
        self.temp_label.config(text=f"{sensor_data['temperature']['value']:.1f}")
        self.humidity_label.config(text=str(int(sensor_data['humidity']['value'])))
        self.noise_label.config(text=str(int(sensor_data['noise']['db_level'])))
        
        self.draw_traffic_graph(sensor_data['traffic']['vehicle_count'], current_hour)
        
        self.root.after(3000, self.update_dashboard)

if __name__ == '__main__':
    root = tk.Tk()
    dashboard = SmartCityDashboard(root)
    root.mainloop()