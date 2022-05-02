# coding=utf-8
from airtest.core.api import *

def runTest(self, poco):
    poco("com.fanmao.bookkeeping:id/rela_tab_4").wait(3).click()
    poco("com.fanmao.bookkeeping:id/img_my_header").click()
    wait(Template(r"res/img/logout.png", record_pos=(0.003, -0.504), resolution=(1040, 1664)))
    poco("com.fanmao.bookkeeping:id/et_mobile").set_text(os.getenv('et_mobile'))
    poco("com.fanmao.bookkeeping:id/et_password").set_text(os.getenv('et_password'))
    poco("com.fanmao.bookkeeping:id/btn_login").click()
    assert_equal(poco("com.fanmao.bookkeeping:id/tv_my_name").wait(3).get_text(), 'null')

def name(self):
    return 'login'