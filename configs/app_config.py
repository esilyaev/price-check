from sys import platform


class Config:

    @staticmethod
    def GetChromeDriverPath():
        if platform == 'linux':
            return './lib/driver/chromedriver'
        if platform == 'win32':
            return 'Lib\driver\chromedriver.exe'
