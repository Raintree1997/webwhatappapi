from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import urllib.request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WebWhatapi(object):
    _URL = 'http://web.whatsapp.com'
    phone_list = []  # 手机号码列表
    xpath_dir = {'stranger': 'http://web.whatsapp.com/send?phone={}&text={}',
             'send': '//*[@id="main"]/footer/div[1]/div[3]',
             'pic1': '//*[@id="main"]/header/div[3]/div/div[2]',
             'pic_import': '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input',
             'pic_send': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div',
             'pic_word': '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div',
             'URL':'//*[@id="main"]/div[4]',
             'mes_check':'//*[@class="vW7d1"]/div/div/div[2]/div/div/span'
             }

    def __init__(self, drive):
        self.drive = drive
        self.drive.get(self._URL)
        self.get_qrcode()

    def get_qrcode(self):
        '''
        保存图片到本地，18内每3秒探索一次是否扫码。超时后刷新界面，嵌套函数
        :return:
        '''
        img = self.drive.find_element_by_xpath('//div[@class="_2EZ_m"]/img')
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, 'E:/test/whatsapp'+str(time.time()) + ".png")
        print("Scan QRCODE")
        try:
            WebDriverWait(self.drive, 18, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"[class='_1FKgS app-wrapper-web bFqKf']")))
            return
        except:
            pass
        try:
            self.drive.refresh()
            WebDriverWait(self.drive,30,2).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_2EZ_m"]/img')))
            self.get_qrcode()
        except:pass

    def __contacts(self, contact):
        """
        判断传进来的是.CSV文件还是单个手机号码。文件按列读取存在列表中，使用时遍历列表
        :param contact:file or int
        :return:
        """
        if isinstance(contact,str):
            file = os.path.splitext(contact)
            filename, type = file
            try:
                if type == '.csv':
                    with open(contact) as f:
                        for i in range(0, 2):
                            phone = f.readline()
                            self.phone_list.append(phone)
                        return self.phone_list
            except:
                print('Wrong file type')
                self.drive.quit()
        else:
            self.phone_list.append(contact)
            return self.phone_list

    def __next_chat(self):
        '''
        取最后一条信息，判断data-icon状态
        :return:
        '''
        a=self.drive.find_elements_by_class_name('vW7d1')[-1].find_element_by_xpath(self.xpath_dir.get('mes_chcek'))
        while True:
            if a.get_attribute('data-icon') == 'msg-check':
                time.sleep(1)
                return
            else:continue

    def send_text(self, phone, text):
        """
        发送消息显式等待30秒，2秒探索一次，调用next-chat函数。切换下个用户页面会刷新
        :param contact:int
        :param text:str
        :return:null
        """
        self.text = text
        self.contact = self.__contacts(phone)
        for i in range(len(self.contact)):
            try:
                self.drive.get(self.xpath_dir.get('stranger').format(self.contact[i], self.text))
                WebDriverWait(self.drive,30,5).until(lambda x:x.find_element_by_xpath(self.xpath_dir.get('send'))).click()
                self.__next_chat()
            except:continue

    def send_url(self, phone, URL):
        """
        输入URL后，循环判断URL内容是否出现
        :param phone:int
        :param URL:str
        :return:null
        """
        self.URL = URL
        self.contact = self.__contacts(phone)
        for i in range(len(self.contact)):
            try:
                self.drive.get(self.xpath_dir.get('stranger').format(self.contact[i], self.URL))
                WebDriverWait(self.drive,30,5).until(lambda x:x.find_element_by_xpath(self.xpath_dir.get('URL')))
                while True:
                    if int(self.drive.find_element_by_xpath(self.xpath_dir.get('URL')).get_attribute('style')[-4])>0:break
                    else:
                        time.sleep(2)
                        continue
                self.drive.find_element_by_xpath(self.xpath_dir.get('send')).click()
                self.__next_chat()
            except:
                continue

    def send_pic(self, phone, path):
        '''
        发送图片
        :param phone:int
        :param path:str
        :return:null
        '''
        self.path = path
        self.contact = self.__contacts(phone)
        for i in range(len(self.contact)):
            try:
                self.drive.get(self.xpath_dir.get('stranger').format(self.contact[i], ' '))
                WebDriverWait(self.drive,30,5).until(lambda x: x.find_element_by_xpath(self.xpath_dir.get('pic1'))).click()
                WebDriverWait(self.drive, 30).until(lambda x: x.find_element_by_xpath(self.xpath_dir.get('pic_import'))).send_keys(self.path)
                time.sleep(2)
                self.drive.find_element_by_xpath(self.xpath_dir.get('pic_send')).click()
                self.__next_chat()
            except:continue

    def send_pictext(self, phone, path, word):
        """
        发送图片加描述
        :param phone:int
        :param path:str
        :param word:str
        :return:
        """
        self.path = path
        self.word = word
        self.contact = self.__contacts(phone)
        for i in range(len(self.contact)):
            try:
                self.drive.get(self.xpath_dir.get('stranger').format(self.contact[i], ' '))
                WebDriverWait(self.drive,30,5).until(lambda x: x.find_element_by_xpath(self.xpath_dir.get('pic1'))).click()
                WebDriverWait(self.drive, 30).until(lambda x: x.find_element_by_xpath(self.xpath_dir.get('pic_import'))).send_keys(self.path)
                picword = WebDriverWait(self.drive, 30).until(lambda x: x.find_element_by_xpath(self.xpath_dir.get('pic_word')))
                picword.send_keys(self.word)
                self.drive.find_element_by_xpath(self.xpath_dir.get('pic_send')).click()
                self.__next_chat()
            except:continue
