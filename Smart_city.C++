#include <iostream>
#include <map>
#include <vector>
#include <iomanip>
#include <cmath>
#include <ctime>
#include <algorithm>

struct CityData {
    int vehicleCount;
    double trafficRate; 
    int airQuality; 
};

class SmartCityAnalyzer {
private:
    std::map<std::string, CityData> indiaStates;
    std::map<std::string, double> worldTrafficRates;
    std::map<std::string, int> worldAirQuality;

public:
    SmartCityAnalyzer() {
        
        indiaStates = {
            {"Maharashtra", {450000, 0.85, 3}},
            {"Delhi", {980000, 0.95, 5}},
            {"Karnataka", {320000, 0.75, 2}},
            {"Tamil Nadu", {380000, 0.78, 3}},
            {"West Bengal", {290000, 0.72, 4}}
        };

         worldTrafficRates = {
            {"Tokyo", 0.92},
            {"New York", 0.88},
            {"London", 0.76},
            {"Singapore", 0.81},
            {"Dubai", 0.79}
        };

         worldAirQuality = {
            {"Zurich", 1},
            {"Vancouver", 1},
            {"Beijing", 4},
            {"Mexico City", 4},
            {"Mumbai", 5}
        };
    }

    void analyzeIndianTraffic() {
        std::cout << "\n=== INDIAN STATES TRAFFIC ANALYSIS ===\n";
        std::cout << std::left << std::setw(15) << "State" 
                  << std::setw(15) << "Vehicles" 
                  << std::setw(15) << "Traffic Rate" 
                  << "Air Quality\n";

        for (const auto& state : indiaStates) {
            std::cout << std::setw(15) << state.first 
                      << std::setw(15) << state.second.vehicleCount 
                      << std::setw(15) << std::fixed << std::setprecision(2) << state.second.trafficRate 
                      << std::setw(15) << getAirQualityText(state.second.airQuality) << "\n";
        }
    }

    void compareGlobalTraffic() {
        std::cout << "\n=== GLOBAL TRAFFIC COMPARISON ===\n";
        std::cout << std::left << std::setw(15) << "City" 
                  << std::setw(15) << "Traffic Rate" 
                  << "Status\n";

        for (const auto& city : worldTrafficRates) {
            std::cout << std::setw(15) << city.first 
                      << std::setw(15) << std::fixed << std::setprecision(2) << city.second 
                      << trafficStatus(city.second) << "\n";
        }
    }

    void displayAirQualityReport() {
        std::cout << "\n=== GLOBAL AIR QUALITY INDEX ===\n";
        std::cout << std::left << std::setw(15) << "City" 
                  << std::setw(15) << "AQI Level" 
                  << "Health Impact\n";

        for (const auto& city : worldAirQuality) {
            std::cout << std::setw(15) << city.first 
                      << std::setw(15) << getAirQualityText(city.second) 
                      << getHealthImpact(city.second) << "\n";
        }
    }

private:
    std::string getAirQualityText(int aqi) {
        switch (aqi) {
            case 1: return "Good";
            case 2: return "Moderate";
            case 3: return "Unhealthy";
            case 4: return "Very Unhealthy";
            case 5: return "Hazardous";
            default: return "Unknown";
        }
    }

    std::string trafficStatus(double rate) {
        if (rate > 0.9) return "Severe Congestion";
        else if (rate > 0.7) return "Heavy Traffic";
        else if (rate > 0.5) return "Moderate";
        else return "Smooth";
    }

    std::string getHealthImpact(int aqi) {
        switch (aqi) {
            case 1: return "No risk";
            case 2: return "Minor concern";
            case 3: return "Limit outdoor activity";
            case 4: return "Health alert";
            case 5: return "Emergency conditions";
            default: return "Unknown";
        }
    }
};

int main() {
    SmartCityAnalyzer analyzer;

    std::cout << "==== SMART CITY ANALYTICS SYSTEM ====\n";
    analyzer.analyzeIndianTraffic();
    analyzer.compareGlobalTraffic();
    analyzer.displayAirQualityReport();

    return 0;
}