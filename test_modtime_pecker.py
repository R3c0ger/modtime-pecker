import unittest
from modtime_pecker import *

class TestCli(unittest.TestCase):
    def test_path_noargs(self):
        sys.argv = ['modtime_pecker.py']
        self.assertEqual(cli(), None)

    def test_path_onearg(self):
        sys.argv = ['modtime_pecker.py', '-p', 'C:\\']
        self.assertEqual(cli(), None)

    def test_path_multiargs(self):
        sys.argv = ['modtime_pecker.py', '-p', 'C:\\', 'D:\\', 'E:\\']
        self.assertEqual(cli(), None)
        
    def test_path_novalue(self):
        sys.argv = ['modtime_pecker.py', '-p']
        with self.assertRaises(SystemExit):
            cli()

    # def test_gui(self):
    #     sys.argv = ['modtime_pecker.py', '-g']
    #     self.assertEqual(cli(), None)
    #
    # def test_gui_with_other_args(self):
    #     sys.argv = ['modtime_pecker.py', '-g', '-p', 'C:\\']
    #     self.assertEqual(cli(), None)

    def test_import(self):
        # 在脚本所在文件夹下创建一个txt文件，写入路径
        paths = "C:\\Users\nC:\\Program Files"
        with open('paths.txt', 'w') as f:
            f.write(paths)
        sys.argv = ['modtime_pecker.py', '-i', 'paths.txt',
                    '-p', 'C:\\', 'C:\\', 'D:\\']
        self.assertEqual(cli(), None)

    def test_multiimport(self):
        paths1 = "C:\\Users\nC:\\Program Files"
        paths2 = "C:\\Windows\nC:\\Program Files"
        with open('paths1.txt', 'w') as f:
            f.write(paths1)
        with open('paths2.txt', 'w') as f:
            f.write(paths2)
        sys.argv = ['modtime_pecker.py', '-i', 'paths1.txt', 'paths2.txt',
                    '-p', 'C:\\', 'C:\\', 'E:\\']
        self.assertEqual(cli(), None)

    def test_invalid_import(self):
        sys.argv = ['modtime_pecker.py', '-i', 'paths.txt', 'invalid.txt']
        with self.assertRaises(FileNotFoundError):
            cli()

    def test_current(self):
        sys.argv = ['modtime_pecker.py', '-c', '-p', 'C:\\']
        self.assertEqual(cli(), None)


class TestGetLatestModificationTime(unittest.TestCase):
    def test_valid_path(self):
        print(get_latest_modification_time('C:\\Program Files\\Windows Defender')[0])
        self.assertTrue(True)

    def test_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            print(get_latest_modification_time('C:\\Progr4m Files\\Wind0ws Defender')[0])


if __name__ == '__main__':
    unittest.main()
