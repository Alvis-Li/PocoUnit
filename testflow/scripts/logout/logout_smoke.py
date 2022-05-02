# coding=utf-8
from airtest.core.api import *

def runTest(self, poco):
    poco("com.fanmao.bookkeeping:id/rela_tab_4").wait(3).click()
    poco("com.fanmao.bookkeeping:id/img_my_header").click()
    poco("com.fanmao.bookkeeping:id/view_setting_exit").wait(1).click()
    poco(text="确定").click()

    wait(Template(r"res/img/logout.png", record_pos=(0.003, -0.504), resolution=(1040, 1664)))

    poco("com.fanmao.bookkeeping:id/view_close").click()

    assert_equal(poco("com.fanmao.bookkeeping:id/tv_my_name").get_text(), '未登录')