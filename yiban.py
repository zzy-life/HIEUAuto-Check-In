'''

@ 文件功能描述：涉外自动化打卡

@ 创建人：时不待我

@ 博客：http://www.zhangzhiyu.live:8900/

'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
from email.mime.text import MIMEText
import smtplib

# 设置服务器所需信息
# 163邮箱服务器地址
mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'My1998zzy@163.com'
# 密码(部分邮箱为授权码)
mail_pass = '请填写授权码'
# 邮件发送方邮箱地址
sender = 'My1998zzy@163.com'


def to_mail(MimeText, Subject):
    """
        发送邮件
        :param MimeText:邮件标题
        :param Subject:邮件正文
        """
    # 设置收件人
    receivers = [sys.argv[3]]

    # 邮件内容设置
    message = MIMEText(MimeText, 'plain', 'utf-8')
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]
    # 邮件主题
    message['Subject'] = sys.argv[1] + Subject
    smtpObj = smtplib.SMTP()
    # 连接到服务器
    smtpObj.connect(mail_host, 25)
    # 登录到服务器
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(mail_user, mail_pass)
    # 发送
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    # 退出
    smtpObj.quit()
    with open(tmp_file_name, 'a') as f:
        f.write("{}".format(str(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))))
        f.write(Subject + "\n\n")


# 目标地址
url = "http://xg.hieu.edu.cn/index"
# 日志名
tmp_file_name = '/db/yiban/' + sys.argv[1] + '打卡日志.txt'
mobile_emulation = {

    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},

    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  "
                 "Mobile/15E148 yiban_iOS/5.0"}

chrome_options = Options()

chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)  # 这里看清楚了，不是add_argument
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # 这个配置很重要
with open('/db/yiban/stealth.min.js') as f:
    js = f.read()

# 操作的目标浏览器
driver = webdriver.Chrome(
    chrome_options=chrome_options)  # 这里的chrome_options 建议都使用 desired_capabilities ，应为在Grid分布式中比较方便

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

flag = False
# 浏览器打开目标地址
try:
    driver.get(url)
    time.sleep(3)
    # 定位输入框
    driver.find_element(By.ID, "uname").click()
    # 清除输入框中的内容
    driver.find_element(By.ID, "uname").clear()
    # 输入框账号
    driver.find_element(By.ID, "uname").send_keys(sys.argv[1])
    # 定位输入框
    driver.find_element(By.ID, "pd_mm").click()
    # 清除输入框中的内容
    driver.find_element(By.ID, "pd_mm").clear()
    # 输入框密码
    driver.find_element(By.ID, "pd_mm").send_keys(sys.argv[2])
    # 点击登陆
    driver.find_element(By.NAME, "submit").click()
    # 等待网页加载
    # 创建显示等待对象
    # 设置等待条件（等搜索结果的div出现）
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[2]/ul[2]/li[1]')
        )
    )
    # 点击今日打卡
    driver.find_element(By.XPATH, "/html/body/div/div[2]/ul[2]/li[1]").click()
    # 等待网页加载
    time.sleep(1)
    # 设置等待条件（等确定的div出现）
    spantext = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div[2]/div[1]/button/span[2]')
        )
    )

    if spantext.text == "打卡":
        # 点击打卡
        driver.find_element(By.ID, "data_list_id_add_btn").click()
        # 等待网页加载
        # 设置等待条件（等确定的div出现）
        # 等待网页加载
        time.sleep(1)
        weizhibutton = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '.btn.btn-default')
            )
        )
        # 点击位置确定
        weizhibutton.click()
        # 点击保存
        driver.find_element(By.ID, "form_body_save_btn").click()
        # 点击确定
        # 设置等待条件（等确定的div出现）
        quedingbutton = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                  (By.CSS_SELECTOR, '.btn.btn-default')
            )
        )
        quedingbutton.click()
        time.sleep(1)
        # 等待网页加载
        spantext = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div[1]/button/span[2]")
            )
        )
        
        if spantext.text == "已打卡":
            flag = True
        else:
            to_mail(sys.argv[1] + '打卡失败', '错误定位142行')

    else:
        with open(tmp_file_name, 'a') as f:
            f.write("{}".format(str(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))))
            f.write("已过打卡\n\n")
    if flag:
        to_mail(sys.argv[1] + '打卡成功', '打卡成功')
    else:
        to_mail(sys.argv[1] + '打卡失败', '打卡失败')

    driver.close()
    driver.quit()
except Exception as e:
    
    to_mail(sys.argv[1] + '打卡失败', '服务器错误')
    driver.close()
    driver.quit()
    print('错误明细是',e.__class__.__name__,e)



