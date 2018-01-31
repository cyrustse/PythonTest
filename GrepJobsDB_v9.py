import urllib.request;
from bs4 import BeautifulSoup;
import csv;
import datetime;
import os;

def decodeStr(String):
    return String.encode("utf-8").decode("utf-8").replace(u"\u2013", "-").replace(u"\u2014", "-").replace(u"\u2015", "-").encode('cp950', 'replace').decode('cp950').encode('cp1252', 'replace').decode('cp1252');



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
            # print(title);
            jobCompany = eachJob.find('p', attrs={'class': 'job-company'});
            company = jobCompany.text.strip();
            # print(company);
            poslinks = eachJob.find('a', attrs={'class': 'posLink'});
            link = poslinks['href'];
            # print(link);
            jobPostTime = eachJob.find('div', attrs={'class': 'job-quickinfo'});
            PostTimeLink = jobPostTime.find('meta');
            PostTime = PostTimeLink.get('content');
            # print(PostTime[:10]);
        returnList.append([decodeStr(title),decodeStr(company),decodeStr(link),decodeStr(str(PostTime[:10])),decodeStr(str(pageNo))]);
    return returnList;

def writeCSV(FileName,JobList):
    _fileName = FileName + '.csv';
    print('Creating file ' + _fileName + '...... ');
    with open(_fileName, 'a', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL);
        wr.writerow(['Pos','Company','Link','PostDate','Page No']);
        for job in JobList:
            wr.writerow(job);

def removeCSV(FileName):
    _fileName = FileName + '.csv';
    if os.path.exists(_fileName):
        print('File ' + _fileName + ' already existed, now deleting it.......');
        os.remove(_fileName);
        print(_fileName + ' Removed');
    else:
        return;

def main():
    pageYouNeed = 50;
    csvName = str(datetime.datetime.now().strftime('%Y-%m-%d'));
    removeCSV(csvName);
    JobList = [];
    url = "https://hk.jobsdb.com/HK/EN/Search/FindJobs?KeyOpt=COMPLEX&JSRV=1&RLRSF=1&JobCat=132,134,142&JSSRC=JSRSB";
    # print("Loading.....Page 1");
    print(url);
    # print("Loading.", "\n");
    soup = websiteParser(url);
    JobList = JobList + websiteHTMLExtractor(soup, 1);
    for pageNo in (range(1, pageYouNeed)):
        url = "https://hk.jobsdb.com/HK/en/Search/FindJobs?AD=30&Blind=1&Host=J&JobCat=132%2c134%2c142&JSRV=1&page=" + str(pageNo);
        # print(".",  "\n");
        # print("Loading.....Page " + str(pageNo + 1));
        print(url);
        soup = websiteParser(url);
        JobList = JobList + websiteHTMLExtractor(soup, pageNo + 1);
    # printJobResult(JobList);
    print('');
    writeCSV(csvName, JobList);




if __name__ == "__main__":
    main();
