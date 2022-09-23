
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

categoryBgcolorClass = {
    '行政': 'bg1',
    '演講': 'bg2',
    '學術': 'bg3',
    '招生': 'bg4',
    '徵才': 'bg5',
    '校園活動': 'bg6',
    '藝文活動': 'bg7',
    '其他': 'bg8'
}

mail_sender = 'sender@example.com'
mail_receiver = 'user@example.com'

error_msg = ''


def get_categoryName(imageUrl):

    if(imageUrl == 'images/bt01.png'):
        name = '行政'
    
    elif(imageUrl == 'images/bt02.png'):
        name = '演講'

    elif(imageUrl == 'images/bt03.png'):
        name = '學術'

    elif(imageUrl == 'images/bt04.png'):
        name = '招生'

    elif(imageUrl == 'images/bt05.png'):
        name = '徵才'

    elif(imageUrl == 'images/bt06.png'):
        name = '校園活動'

    elif(imageUrl == 'images/bt07.png'):
        name = '藝文活動'

    elif(imageUrl == 'images/bt09.png'):
        name = '其他'

    else:
        name = ''

    return name


def fetchNews():

    global error_msg
    news = []
    today = datetime.now().strftime('%Y %m.%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y %m.%d')
    pageNo = 1

    while pageNo <= 10:
        url = 'https://infonews.nycu.edu.tw/index.php?SuperType=2&action=more&categoryid=all&pagekey=' + str(pageNo)
        sourceCode = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"}).content
        
        try:
            sourceCode.decode('cp950')
        except UnicodeDecodeError:
            error_msg += 'Failed to decode News in page ' + str(pageNo) + '<br />'
        else:
            soup = BeautifulSoup(sourceCode, 'html.parser').find('div', {'id': 'layout_more'})

            if soup != None:
                rows = soup.findAll('tr')
                rowsLength = len(rows)

                for i in range(rowsLength):
                    row = rows[i]

                    if row.find('img', {'class': 'style1'}) != None:
                        category = ''
                        title = ''
                        link = ''
                        dateStart = ''
                        dateEnding = ''
                        publisher = ''

                        # Fetch category.
                        category = get_categoryName(row.find('img', {'class': 'style1'})['src'])

                        # Fetch title and link.
                        element = row.find('td', {'class': 'style2'})

                        if element != None:
                            element = element.find('a')

                            if element != None:
                                title = element.contents[0]

                                link = element['href']
                                link = 'https://infonews.nycu.edu.tw/' + link

                        # Fetch date.
                        if i + 1 < rowsLength:
                            element = rows[i+1].find('td', {'class': 'style4'})

                            if element != None:
                                date = element.contents[0]
                                dateSepIndex = date.find('-')

                                if dateSepIndex != -1:
                                    dateStart = date[:dateSepIndex]
                                    dateStart = datetime.strptime(dateStart, '%Y/%m/%d')
                                    dateStartStr = dateStart.strftime('%Y %m.%d')

                                    dateEnding = date[dateSepIndex+1:]
                                    dateEnding = datetime.strptime(dateEnding, '%Y/%m/%d')
                                    dateEndingStr = dateEnding.strftime('%Y %m.%d')

                        # Fetch publisher.
                        if i + 2 < rowsLength:
                            element = rows[i+2].find('td', {'class': 'style4'})

                            if element != None:
                                publisher = element.contents[0]

                        # Check start date.
                        if dateStartStr == yesterday:
                            news.append({
                                'category': category,
                                'title': title,
                                'link': link,
                                'dateStart': dateStartStr,
                                'dateEnding': dateEndingStr,
                                'publisher': publisher
                            })

        pageNo += 1

    return news


def fetchActivity():

    news = []
    today = datetime.now().strftime('%Y %m.%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y %m.%d')
    pageNo = 1

    while pageNo <= 10:
        url = 'https://infonews.nycu.edu.tw/index.php?SuperType=1&action=more&categoryid=all&pagekey=' + str(pageNo)
        sourceCode = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"}).content

        try:
            sourceCode.decode('cp950')
        except UnicodeDecodeError:
            error_msg += 'Failed to decode Activity in page ' + str(pageNo) + '<br />'
        else:
            rows = BeautifulSoup(sourceCode, 'html.parser').find('div', {'id': 'layout_more'}).findAll('tr')
            rowsLength = len(rows)

            for i in range(rowsLength):
                row = rows[i]

                if row.find('img', {'class': 'style1'}) != None:
                    category = ''
                    title = ''
                    link = ''
                    dateStart = ''
                    dateEnding = ''
                    publisher = ''

                    # Fetch category.
                    category = get_categoryName(row.find('img', {'class': 'style1'})['src'])

                    # Fetch title and link.
                    element = row.find('td', {'class': 'style2'})

                    if element != None:
                        element = element.find('a')

                        if element != None:
                            title = element.contents[0]

                            link = element['href']
                            link = 'https://infonews.nycu.edu.tw/' + link

                    # Fetch date.
                    if i + 1 < rowsLength:
                        element = rows[i+1].find('td', {'class': 'style4'})

                        if element != None:
                            date = element.contents[0]
                            dateSepIndex = date.find('-')

                            if dateSepIndex != -1:
                                dateStart = date[:dateSepIndex]
                                dateStart = datetime.strptime(dateStart, '%Y/%m/%d')
                                dateStartStr = dateStart.strftime('%Y %m.%d')

                                dateEnding = date[dateSepIndex+1:]
                                dateEnding = datetime.strptime(dateEnding, '%Y/%m/%d')
                                dateEndingStr = dateEnding.strftime('%Y %m.%d')

                    # Fetch publisher.
                    if i + 2 < rowsLength:
                        element = rows[i+2].find('td', {'class': 'style4'})

                        if element != None:
                            publisher = element.contents[0]

                    # Check start date.
                    if dateStartStr == yesterday:
                        news.append({
                            'category': category,
                            'title': title,
                            'link': link,
                            'dateStart': dateStartStr,
                            'dateEnding': dateEndingStr,
                            'publisher': publisher
                        })

        pageNo += 1

    return news


def sendMail(news, activities):

    global error_msg

    mailContent = """
        <html>
            <body>
                <header>
                    <h1>交大公告推播</h1>
                </header>
                
                <table>
                    <tr>
                        <th class="news_category_cell" colspan="2">公告</th>
                        <th class="news_published_cell">發布時間</th>
                    </tr>
    """

    for item in news:
        mailContent += '<tr><td class="news_category_cell"><span class="news_category_text ' + categoryBgcolorClass[item['category']] + '">' + item['category'] + '</span></td>'
        mailContent += '<td class="news_title_cell"><a href="' + item['link'] + '">' + item['title'] + '</a></td><td class="news_published_cell">' + item['dateStart'] + '</td></tr>'

    mailContent += """
        </table>

        <div class="space_medium"></div>

        <header>
            <h1>交大活動推播</h1>
        </header>
        
        <table>
            <tr>
                <th class="news_category_cell" colspan="2">公告</th>
                <th class="news_published_cell">發布時間</th>
            </tr>
    """

    for item in activities:
        mailContent += '<tr><td class="news_category_cell"><span class="news_category_text ' + categoryBgcolorClass[item['category']] + '">' + item['category'] + '</span></td>'
        mailContent += '<td class="news_title_cell"><a href="' + item['link'] + '">' + item['title'] + '</a></td><td class="news_published_cell">' + item['dateStart'] + '</td></tr>'

    mailContent += """
        </table>
        
        <p id="error_text">
    """

    mailContent += error_msg

    mailContent += """
                </p>
                
                <div class="space_medium"></div>
    
                <style>
    
                    body
                    {
                        margin: 0px auto;
                        width: 1024px;
                    }
    
                    header h1
                    {
                        margin: 20px 0px 40px;
                        font-size: 30px;
                        letter-spacing: 5px;
                        text-align: center;
                    }
    
                    a:link,
                    a:visited
                    {
                        border-bottom: 1px solid transparent;
                        color: #000000;
                        text-decoration: none;
                    }
    
                    a:hover,
                    a:active
                    {
                        border-bottom: 1px solid #000000;
                    }
    
                    table
                    {
                        width: 100%;
                        border-collapse: collapse;
                    }
    
                    th, td
                    {
                        padding: 10px;
                        font-size: 20px;
                        font-weight: normal;
                    }
    
                    th
                    {
                        border-bottom: 1px solid #000000;
                        letter-spacing: 5px;
                    }
    
                    td
                    {
                        border-bottom: 1px solid #a4a3a3;
                    }
    
                    .news_category_cell
                    {
                        padding-right: 0px;
                        width: 70px;
                    }
    
                    .news_category_text
                    {
                        padding: 5px 10px;
                        background-color: #505050;
                        border-radius: 10px;
                        color: #ffffff;
                        font-size: 18px;
                    }
    
                    .news_title_cell
                    {
                        line-height: 1.7;
                    }
    
                    .news_published_cell
                    {
                        width: 130px;
                        text-align: center;
                    }
                    
                    #error_text
                    {
    """

    if len(error_msg) == 0:
        mailContent += 'display: none;'

    mailContent += """
                        margin-top: 200px;
                        font-size: 20px;
                        font-weight: bold;
                        color: #ff0000;
                    }
    
                    .bg1
                    {
                        background-color: #C425A3;
                    }
    
                    .bg2
                    {
                        background-color: #F9A02B;
                    }
    
                    .bg3
                    {
                        background-color: #B8980A;
                    }
    
                    .bg4
                    {
                        background-color: #2EBA3E;
                    }
    
                    .bg5
                    {
                        background-color: #2C9DA7;
                    }
    
                    .bg6
                    {
                        background-color: #2C48A7;
                    }
    
                    .bg7
                    {
                        background-color: #D82F2F;
                    }
    
                    .bg8
                    {
                        background-color: #8F3A84;
                    }
    
                    .space_medium
                    {
                        height: 200px;
                    }
    
                </style>
            </body>
        </html>
    """

    mail = EmailMessage()
    mail.set_content(mailContent, subtype='html')
    mail['To'] = mail_receiver
    mail['From'] = mail_sender
    mail['Subject'] = '交大公告與活動推播 (僅蒐集昨天發布的訊息)'

    mailServer = smtplib.SMTP('localhost')
    mailServer.send_message(mail)
    mailServer.quit()


news = fetchNews()
activities = fetchActivity()

sendMail(news, activities)
