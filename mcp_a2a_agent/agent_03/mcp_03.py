from fastmcp import FastMCP
mcp=FastMCP("demo")

CITY_PROFILES = {
    "london": {"country": "UK", "timezone": "Europe/London", "best_month": "May"},
    "mumbai": {"country": "India", "timezone": "Asia/Kolkata", "best_month": "January"},
    "new-york": {"country": "USA", "timezone": "America/New_York", "best_month": "October"},
}

WEATHER = {
    "london": 14,
    "mumbai": 31,
    "new-york": 22,
}

@mcp.resource("weather://cities")            # Used for giving Context
def cities_weather():
    """Gives the list of cities for which weather is available"""
    return {"cities":list(CITY_PROFILES.keys())}


@mcp.resource("weather://cities/{city}")             #the URI pattern should be Same
def city_profiles(city:str):
    """Return the city profiles for the Specified City"""
    city=city.strip().lower().replace(" ","-")
    if city not in CITY_PROFILES:
        raise ValueError(f"{city} profile doesnot exist. Try among london,Mumbai or New York")
    return {"city":city,**CITY_PROFILES[city]}


@mcp.tool
def compare_temperatures(cityA:str,cityB:str):
    """Gives a Comparision between the temperature of two cities"""
    cityA=cityA.strip().lower().replace(" ","-")
    cityB=cityB.strip().lower().replace(" ","-")

    if cityA not in CITY_PROFILES or cityB not in CITY_PROFILES:
        raise ValueError(f"Select either of the cities Mumbai,London or New York")
    difference=WEATHER[cityA]-WEATHER[cityB]
    if difference>0:
        warmer=cityA
    else:
        warmer=cityB
    return f"The Warmer city is {warmer} with a temperature difference of {abs(difference)}"


@mcp.prompt
def prompt_structure(city:str,audience:str):
    """Gives a reusable weather prompt to get the weather in a specified city for a particular audience"""
    return (
        f"Write a concise weather briefing for a {audience} visiting {city}. "
        "Mention temperature, practical clothing advice, and one risk."
    )

if __name__=="__main__":
    mcp.run(transport="http")







