# coding=utf-8
from airtest.core.api import *

from libs.utils.login import selectTabMine

def runTest(self, poco):
    selectTabMine(poco)
    poco("com.xmiles.jdd:id/tv_mine_username").wait(1).click()
    poco("com.xmiles.jdd:id/tv_login_phone").wait(1).click()
    poco("com.xmiles.jdd:id/et_login_phone_num").wait(3).set_text(123)
    snapshot(msg="输入手机号")

def name(self):
    return 'CalculatorPlus (customized name)'