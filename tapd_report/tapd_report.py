# !/usr/env/bin python3
# -*- coding:utf-8 -*-
# Author:T5-10858(xuwanle@addcn.com)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



def open_window(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(8)
    return driver


def login(driver, usr, psw):
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(usr)
    driver.find_element(By.XPATH, '//*[@id="password_input"]').send_keys(psw)
    driver.find_element(By.XPATH, '//*[@id="tcloud_login_button"]').click()

# 判断element是否存在，如果存在则返回True
def isElementExist(driver, element_name):
    flag = True
    try:
        driver.find_element(By.NAME, element_name)
        return flag
    except:
        flag = False
        return flag


def set_time(driver, start_time, end_time):
    # 時間格式，例如：2021-08-16 00:00
    driver.find_element(By.NAME, "data[Bugreport][time_setting][from]").clear()
    driver.find_element(By.NAME, "data[Bugreport][time_setting][from]").send_keys(start_time)
    driver.find_element(By.NAME, "data[Bugreport][time_setting][to]").clear()
    driver.find_element(By.NAME, "data[Bugreport][time_setting][to]").send_keys(end_time)
    if isElementExist(driver, "data[Bugreport][create_time_setting][from]"):
        driver.find_element(By.NAME, "data[Bugreport][create_time_setting][from]").clear()
        driver.find_element(By.NAME, "data[Bugreport][create_time_setting][from]").send_keys(start_time)
        driver.find_element(By.NAME, "data[Bugreport][create_time_setting][to]").clear()
        driver.find_element(By.NAME, "data[Bugreport][create_time_setting][to]").send_keys(end_time)


def draw_report(report_info, bug_info, login_info):
    name = report_info[0]
    url = report_info[1]

    # 打开窗口并进行登录
    print("###########################################")
    driver = open_window(url)
    login(driver, login_info['usr'], login_info['psw'])

    print('需求【{}】的\"{}\"正在绘制中...'.format(bug_info['story_id'], name))
    # 根据需求id号搜寻缺陷
    driver.find_element(By.NAME, "title").send_keys(bug_info['story_id'])

    # 设置缺陷生效时间
    set_time(driver, bug_info['start_time'], bug_info['start_time'])

    # 点击生成按钮
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
    print('已完成绘制。')
    time.sleep(3)

    # # 调试用截图窗口
    # file_name = 'F:/Pictrue/{}.png'.format(name + str(int(time.time())))
    # driver.save_screenshot(file_name)
    # print('已完成绘制,报表结果保存路径：{}'.format(file_name))

    # 点击【另存为】按钮
    driver.find_element(By.CSS_SELECTOR, '.btn.j-bug_stat__save_new').click()
    # 点击【保存】按钮


    # 定位到弹出窗，并清空重新输入报告名称
    report_name = '【{}】{}'.format(bug_info['story_id'], name)
    rename_window = driver.find_element(By.CSS_SELECTOR, '.ui-dialog.d-animation.ui-draggable.d-animation-show')
    rename_window.find_element(By.NAME, 'data[Bugreport][title]').clear()
    rename_window.find_element(By.NAME, 'data[Bugreport][title]').send_keys(str(report_name))
    # 点击【保存】按钮
    rename_window.find_element(By.CSS_SELECTOR, '.btn.btn-primary').click()
    time.sleep(3)

if __name__ == '__main__':
    # 报表模板地址
    report_info = {
        # '缺陷每日变化趋势': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_trend/trend/customreport-1163835346001001011',
        '各端缺陷類型分佈圖': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_general/general/customreport-1163835346001001010',
        '各端缺陷根源分布图': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_general/general/customreport-1163835346001001008',
        '各端缺陷級別分佈圖': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_general/general/customreport-1163835346001001009',
        '缺陷年齡報告': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_age/age/customreport-1163835346001001012',
        '缺陷解决率': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_other/resolution/customreport-1163835346001001013',
        '缺陷回歸分佈圖': 'https://www.tapd.cn/63835346/bugtrace/bugreports/stat_other/regression/customreport-1163835346001001014'
    }

    # 输入缺陷信息
    bug_info = {}
    bug_info['story_id'] = ''  # 输入你的缺陷需求
    bug_info['start_time'] = ''  # 输入你的缺陷开始时间, 格式例如：2021-08-16
    bug_info['end_time'] = ''  # 输入你的缺陷结束时间

    # 输入登录信息
    login_info = {}
    login_info['usr'] = ''  # 输入你的Tapd账号
    login_info['psw'] = ''  # 输入你的Tapd密码

    for r in report_info.items():
        draw_report(r, bug_info, login_info)
