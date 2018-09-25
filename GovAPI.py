
import urllib.request;
import json;
import requests;

def getParkingSpaces():
    ReturnString = "";
    URL ="https://sps-opendata.pilotsmartke.gov.hk/rest/getCarparkInfos";
    Results = urllib.request.urlopen(URL).read().decode();
    Results = json.loads(Results);
    Results = Results["results"];
    for Result in Results:
        carparkid = str(Result["_id"]);
        carparkName = str(Result["name"]);
        space = str(Result["privateCar"]["space"]);
        ReturnString += carparkid + " - " + carparkName + ": " + space + "\n";
    return ReturnString;

def getParkingVacancies():
    ReturnString = "";
    URL ="https://sps-opendata.pilotsmartke.gov.hk/rest/getCarparkVacancies";
    Results = urllib.request.urlopen(URL).read().decode();
    Results = json.loads(Results);
    Results = Results["results"];
    for Result in Results:
        carparkid = str(Result["_id"]);
        vacancy = str(Result["privateCar"]["vacancy"]);
        ReturnString += carparkid + ": " + vacancy + "\n";
    return ReturnString;

def getParkingSpacesWithVacancies():
    ReturnString = "";
    URL ="https://sps-opendata.pilotsmartke.gov.hk/rest/getCarparkInfos";
    URL2 ="https://sps-opendata.pilotsmartke.gov.hk/rest/getCarparkVacancies";
    Results = urllib.request.urlopen(URL).read().decode();
    Results = json.loads(Results);
    Results = Results["results"];
    Results2 = urllib.request.urlopen(URL2).read().decode();
    Results2 = json.loads(Results2);
    Results2 = Results2["results"];
    for Result in Results:
        carparkid = Result["_id"];
        carparkName = str(Result["name"]);
        space = str(Result["privateCar"]["space"]);
        for Result2 in Results2:
            carparkid2 = Result2["_id"]
            if carparkid2==carparkid:
                vacancy2 = str(Result2["privateCar"]["vacancy"]);
                ReturnString += str(carparkid) + " - " + carparkName + "- Space:" + space + " Vacancy:" + vacancy2 +"\n";
            else:
                vacancy2 = str(0);
    return ReturnString;

SAMPLE_API_KEY = '615727c0054646e5d73969f76d3b4223';

def weatherConversion(From,Degree):    # First Para: Kelvin/Fahrenheit, Sec Para: degree
    # This Function is used for converting Kelvin/Fahrenheit to Celsius
    if From =='Kelvin':
        return float(Degree) - 273.15;
    elif From =='Fahrenheit':
        return (float(Degree) - 32) * 5 / 9;
    else:
        return 0;

def current_weather(location, api_key=SAMPLE_API_KEY):
    url = 'https://api.openweathermap.org/data/2.5/weather';
    query_params = {
        'q': location,
        'appid': api_key,
    };
    response = requests.get(url, params=query_params);
    # return response.json()['weather'][0]['description'];

    return_dict= {"temp": 0, "temp_max": 0, "temp_min": 0, "lat":0, "lon":0 ,"description":""};

    # return_dict.setdefault("temp",response.json()['main']['temp'])
    return_dict["temp"] =response.json()['main']['temp'];
    return_dict["temp_max"] = response.json()['main']['temp_max'];
    return_dict["temp_min"] = response.json()['main']['temp_min'];
    return_dict["lat"] = response.json()['coord']['lat'];
    return_dict["lon"] = response.json()['coord']['lon'];
    return_dict["description"] = response.json()['weather'][0]['description'];
    # response.json()['main']['temp'];
    # filled_dict["four"] = 4;
    # print(filled_dict.items());
    # filled_dict.setdefault("five",5);
    # return response.json()['main']['temp'];
    return return_dict;

def main():
    # Degree = current_weather('Hong Kong');
    # print(Degree);

    # print("Current Degree: " + str(weatherConversion('Kelvin', Degree["temp"])));
    # print("Today Max: " + str(weatherConversion('Kelvin', Degree["temp_max"])));
    # print("Today Min: " + str(weatherConversion('Kelvin', Degree["temp_min"])));
    # print(weatherConversion('Kelvin',Degree));
    # print(getParkingSpacesWithVacancies());
    # print(getParkingVacancies());
    print(getParkingSpaces());

if __name__ == "__main__":
    main();
