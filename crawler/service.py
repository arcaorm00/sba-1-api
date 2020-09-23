import sys
sys.path.insert(0, '/Users/saltQ/sbaProject')
from urllib.request import urlopen
from crawler.entity import Entity
from bs4 import BeautifulSoup
from pandas import DataFrame
import os, shutil

class Service:
    def __init__(self):
        self.entity = Entity()

    def bugs_music(self):
        pass

    def naver_movie(self, url):
        myparser = self.entity.parser
        html = urlopen(url)
        soup = BeautifulSoup(html, myparser)

        Service.crawlingMovies(soup)

    def naver_cartoon(self, url):
        myparser = self.entity.parser
        response = urlopen(url)
        soup = BeautifulSoup(response, myparser)

        Service.crawlingCartoons(soup)

    # 네이버 웹툰: 폴더 생성
    @staticmethod
    def create_folder_weekend():
        # 요일별 폴더 생성
        weekday_dict = {'mon': '월요일', 'tue': '화요일', 'wed': '수요일', 'thu': '목요일', 'fri': '금요일', 'sat': '토요일', 'sun': '일요일'}        
        
        myFolder = 'c:\\cartoonTest\\'

        try:
            if not os.path.exists(myFolder):
                os.mkdir(myFolder)

            for mydir in weekday_dict.values():
                mypath = myFolder + mydir

                if os.path.exists(mypath):
                    shutil.rmtree(mypath)

                os.mkdir(mypath)
        except FileExistsError as err:
            print(err)
        return weekday_dict
        
    # 네이버 웹툰: 각 이미지를 저장해주는 함수
    @staticmethod
    def saveFile(weekday_dict, mysrc, myweekday, mytitle):
        image_file = urlopen(mysrc)
        filename = 'c:\\cartoonTest\\' + weekday_dict[myweekday] + '\\' + mytitle + '.jpg'

        myfile = open(filename, mode='wb')
        myfile.write(image_file.read())
        myfile.close()

    # 네이버 웹툰: 크롤링
    @staticmethod
    def crawlingCartoons(soup):
        weekday_dict = Service.create_folder_weekend()

        mytarget = soup.find_all('div', attrs={'class': 'thumb'})
        print(len(mytarget))

        mylist = []  # 데이터를 저장할 리스트

        for abcd in mytarget:
            myhref = abcd.find('a').attrs['href']
            myhref = myhref.replace('/webtoon/list.nhn?', '')
            result = myhref.split('&')

            mytitleid = result[0].split('=')[1]
            myweekday = result[1].split('=')[1]

            imgtag = abcd.find('img')
            mytitle = imgtag.attrs['title'].strip()
            mytitle = mytitle.replace('?','').replace(':','')

            mysrc = imgtag.attrs['src']

            Service.saveFile(weekday_dict, mysrc, myweekday, mytitle)

            sublist = []
            sublist.append(mytitleid)
            sublist.append(myweekday)
            sublist.append(mytitle)
            sublist.append(mysrc)
            mylist.append(sublist)

        Service.makeCsvForCartoons(mylist)

    # 네이버 웹툰: csv 파일 저장
    @staticmethod
    def makeCsvForCartoons(myList):
        mycolumns = ['타이틀 번호', '요일', '제목', '링크']
        myframe = DataFrame(myList, columns=mycolumns)

        filename = './crawler/crawlingCsv/cartoon.csv'

        myframe.to_csv(filename, encoding='utf-8', index=False)
        print(filename + '파일로 저장됨')


    # 네이버 영화: 크롤링
    @staticmethod
    def crawlingMovies(soup):
        tags = soup.findAll('div', attrs={'class': 'tit3'}) # findAll과 find_all은 동일. 전자는 bs의 올드스타일 레거시

        url_header = 'http://movie.naver.com'

        mytrs = soup.find_all('tr')

        no = 0  # 순서를 의미하는 번호
        totallist = []  # 전체를 저장할 리스트

        for one_tr in mytrs:
            title = ''
            up_down = '' # 순위 변동

            mytd = one_tr.find('td', attrs={'class': 'title'})
            if mytd is not None:
                no += 1
                newno = str(no).zfill(2)

                mytag = mytd.find('div', attrs={'class': 'tit3'})
                title = mytag.a['title'] # title 속성에도 위의 a.string과 마찬가지로 제목이 담겨있다

                # 순위 변동 부분 파싱
                mytd = one_tr.select_one('td:nth-of-type(3)')  # 세 번째 td를 선택
                myimg = mytd.find('img')
                if myimg.attrs['alt'] == 'up':
                    up_down = '상승'
                elif myimg.attrs['alt'] == 'down':
                    up_down = '하락'
                else:
                    up_down = '유지'

                change = one_tr.find('td', attrs={'class': 'range ac'})
                if change is None:
                    change = '신규 진입'
                else:
                    change = change.string

                totallist.append((newno, title, up_down, change))

        Service.makeCsvForMovie(totallist)

    # 네이버 영화: csv 파일 저장
    @staticmethod
    def makeCsvForMovie(totallist):
        mycolumns = ['순위', '제목', '변동', '변동폭']
        myframe = DataFrame(totallist, columns=mycolumns)

        filename = './crawler/crawlingCsv/naverMovieRank.csv'

        myframe.to_csv(filename)

        print(filename + ' 파일 저장됨')