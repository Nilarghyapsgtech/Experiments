from fastmcp import FastMCP

mcp=FastMCP("Demo")

WEATHER = {
    "london": {"temp_c": 14, "condition": "cloudy", "wind_kph": 18},
    "mumbai": {"temp_c": 31, "condition": "humid", "wind_kph": 12},
    "new york": {"temp_c": 22, "condition": "clear", "wind_kph": 9},
}

def city_name(city:str):
    return city.strip().lower()

@mcp.tool
def current_weather(city:str):
    """Gives the Current weather for a specified Location"""
    city=city_name(city)
    if city not in WEATHER:
        raise ValueError(f"{city} not supported.Try out London,Mumbai or New York")
    return {"city": city, **WEATHER[city]}

@mcp.tool
def weather_forecast(city:str,days:int):
    """Gives a forecast of the weather for 1 to 5 days"""
    if days<1 or days>5:
        raise ValueError(f"Can predict weather between 1 to 5 days")
    current_weather_details=current_weather(city)
    return [
        {
            "day":day,
            "city":city,
            "temp_c":current_weather_details["temp_c"]+day-1,
            "condition":current_weather_details["condition"]

        }
        for day in range(1,days+1)
    ]

@mcp.tool
def packing_details(city:str,day:str):
    """Advices on how to do packing Based on the Weather conditions"""
    weather_details=weather_forecast(city,5)[day]
    if weather_details["condition"]=="clear" or weather_details["condition"]=="humid":
        return "Pack Small Weather is Ok"
    else:
        return "Pack Heavily Weather might backfire"
    

if __name__=="__main__":
    mcp.run(transport="http")


