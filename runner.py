import os
import sys
import glob
import argparse
import pocounit
import importlib.util

from dotenv import load_dotenv
from pocounit.case import PocoTestCase
from pocounit.suite import PocoTestSuite
from pocounit.addons.poco.capturing import SiteCaptor
from pocounit.addons.poco.action_tracking import ActionTracker
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.api import connect_device, device as current_device, start_app, stop_app, uninstall

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--smoke', help='执行冒烟测试用例', action='store_true')
parser.add_argument('-f', '--file', help='指定执行文件, 如: test/test.py')
args = parser.parse_args()

load_dotenv()
package_name = os.getenv('package_name')
device_uri = os.getenv('device_uri')
project_root = os.path.dirname(os.path.abspath(__file__))
libs_root = os.path.join(project_root, os.getenv(
    'src_dir', 'testflow'), os.getenv('libs_dir', 'libs'))
test_case_dir = os.path.join(project_root, os.getenv(
    'src_dir', 'testflow'), os.getenv('scripts_dir', 'scripts'))

os.system('adb kill-server')  # 重启adb
sys.path.insert(0, os.path.join(
    project_root, os.getenv('src_dir', 'testflow')))


class AndroidAppCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(AndroidAppCase, cls).setUpClass()
        cls.poco = AndroidUiautomationPoco(
            use_airtest_input=True, screenshot_each_action=False)

        cls.project_root = project_root
        cls.test_case_dir = test_case_dir
        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)
        cls.site_capturer = SiteCaptor(cls.poco)
        cls.register_addon(cls.site_capturer)


class AndroidAppSuite(PocoTestSuite):
    def setUp(self):
        if not current_device():
            connect_device(device_uri)

        dev = current_device()
        # 去掉录制。如果需要录制，注释掉下面三行代码
        dev.recorder.start_recording = lambda max_time, bit_rate: self
        dev.recorder.stop_recording = lambda output, is_interrupted: self
        dev.recorder.pull_last_recording_file = lambda output: self

        start_app(package_name)

    def tearDown(self):
        stop_app(package_name)
        uninstall('com.netease.nie.yosemite')
        uninstall('com.netease.open.pocoservice')


def moduleFromFile(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def makeNewClass(x, file):
    dict = {}
    if hasattr(file, 'runTest'):
        dict['runTest'] = lambda self: file.runTest(self, self.poco)
    if hasattr(file, 'setUp'):
        dict['setUp'] = lambda self: file.setUp(self, self.poco)
    if hasattr(file, 'tearDown'):
        dict['tearDown'] = lambda self: file.tearDown(self, self.poco)

    new_class = type(x, (AndroidAppCase,), dict)

    if hasattr(file, 'getMetaInfo'):
        setattr(new_class, 'getMetaInfo', file.getMetaInfo)
    if hasattr(file, 'name'):
        setattr(new_class, 'name', file.name)
    return new_class


if __name__ == '__main__':
    file_list = glob.glob(test_case_dir + '/**/*.py', recursive=True)
    tests = []
    for file_path in file_list:
        file = moduleFromFile(project_root, file_path)
        test_case_filename, _ = os.path.splitext(
            os.path.relpath(file_path, test_case_dir))
        if args.file and args.file != test_case_filename+'.py':
            continue
        if args.smoke and ('smoke' not in test_case_filename):
            continue
        sub_class = makeNewClass(test_case_filename, file)
        tests.append(sub_class())

    if len(tests) > 0:
        suite = AndroidAppSuite(tests)
        pocounit.run(suite)
    else:
        raise Exception('未找到任何测试用例')