import telegram;
import urllib.request;
import json;
import requests;

from time import sleep;
from time import gmtime, strftime

from bs4 import BeautifulSoup;
import datetime;

# For Telegram Bot
BOT_TOKEN ="457922992:AAGcXqur9W7OLOuH8ay5x9n0W3sTABgOMF4";
Bot = telegram.Bot(BOT_TOKEN);
# Bot = Telegram.Bot(BOT_TOKEN);

# For weather API
SAMPLE_API_KEY = '615727c0054646e5d73969f76d3b4223';


lastMessageId = 0;


def getText(Update):
    return Update["message"]["text"];

def getMessageId(Update):
    return Update["update_id"];

def getUserId(Update):
    return Update["message"]["from_user"]["id"];

def messageHandler(Update):
    global lastMessageId;
    text = getText(Update);
    msg_id = getMessageId(Update);
    user_id = getUserId(Update);
    lastMessageId = msg_id;
    if(text=="/time"):
        Bot.sendMessage(user_id, strftime("The time now is.. %a, %d %b %Y %H:%M:%S +0000", gmtime()));
        return;
    elif(text=="/parking"):
        Bot.sendMessage(user_id, " " + getParkingSpacesWithVacancies())
        return;
    elif(text=="/whatsmyip"):
        Bot.sendMessage(user_id, "IP is..")
        return;
    elif(text=="/weather"):
        Bot.sendMessage(user_id, " " + getCurrentWeather('Hong Kong'))
        return;
    elif(text=="/job"):
        Bot.sendMessage(user_id, " " + getJobList())
        return;
    print(user_id, msg_id, text);
    return;

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
    return_dict= {"temp": 0, "temp_max": 0, "temp_min": 0, "lat":0, "lon":0 ,"description":""};
    return_dict["temp"] =response.json()['main']['temp'];
    return_dict["temp_max"] = response.json()['main']['temp_max'];
    return_dict["temp_min"] = response.json()['main']['temp_min'];
    return_dict["lat"] = response.json()['coord']['lat'];
    return_dict["lon"] = response.json()['coord']['lon'];
    return_dict["description"] = response.json()['weather'][0]['description'];
    return return_dict;

def getCurrentWeather(location):
    Degree = current_weather(location);
    return_str = "Current Degree: " + str(weatherConversion('Kelvin', Degree["temp"]));
    return return_str;



def decodeStr(String):
    return String.encode("utf-8").decode("utf-8").encode('cp950', 'replace').decode('cp950').encode('cp1252', 'replace').decode('cp1252');


def websiteParser(URL): #need URL
    # print(URL);
    # req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'});
    req = urllib.request.Request(URL, headers={'User-Agent': 'Chrome/63.0.3239.132'});
    webPage = urllib.request.urlopen(req).read();
    soup = BeautifulSoup(webPage, 'html.parser');
    return soup;

def websiteHTMLExtractor(SOUP,pageNo): #need soup object, and return List object as a result
    returnList =[];
    job_mains = SOUP.find_all('div', attrs={'class': 'result-sherlock-cell'});
    # print(job_mains);
    for eachJob in job_mains:
        if len(eachJob) == 5:   #standard cell will contain 5 Div 'job-cell-tools','job-main','job-summary-container','job-quickinfo' and 'job-applied-status'
            jobTitle = eachJob.find('h3', attrs={'class': 'job-title'});
            title = jobTitle.text.strip();
            jobCompany = eachJob.find('p', attrs={'class': 'job-company'});
            company = jobCompany.text.strip();
        returnList.append([decodeStr(title),decodeStr(company)]);
    return returnList;

def getJobList():
    JobList = [];
    url = "https://hk.jobsdb.com/HK/EN/Search/FindJobs?KeyOpt=COMPLEX&JSRV=1&RLRSF=1&JobCat=132,134,142&JSSRC=JSRSB";
    soup = websiteParser(url);
    JobList = websiteHTMLExtractor(soup, 1);
    return_str = "";
    for x in JobList:
        return_str += x[0] + '--' + x[1];
    return return_str;

def main():
    global lastMessageId;
    Updates = Bot.getUpdates();
    if(len(Updates) > 0):
        lastMessageId = Updates[-1]["update_id"];
    while(True):
        Updates = Bot.getUpdates(offset=lastMessageId); #List
        Updates = [Update for Update in Updates if Update["update_id"] > lastMessageId];
        for Update in Updates:
            #text = Update["message"]["text"];
            #msg_id = Update["update_id"];
            #lastMessageId = msg_id;
            #print(msg_id, text);
            messageHandler(Update)
        sleep(0.5);

if __name__ == "__main__":
    main();
