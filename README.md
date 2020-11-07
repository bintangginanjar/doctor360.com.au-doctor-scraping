Scrape doctor profile and schedule from https://www.doctor360.com.au using following library

    request
    json
    BeautifulSoup
    Selenium

Flow of scraper are following

    1. Extract doctor name and their specialty from every city in Australia from following URL, https://www.doctor360.com.au/
    2. For each doctor specialty and their city, extract their name while at the same time extract clinic they've already registered also the schedule
    3. Import the result into JSON
    
Front page contain list of doctor category for each city
![Screenshot](Selection_278.png)

Second page, contains list of doctor member for each city and specialty
![Screenshot](Selection_279.png)

Third page, contains doctor profile detail
![Screenshot](Selection_280.png)

Third page, also contains doctor schedule
![Screenshot](Selection_281.png)
