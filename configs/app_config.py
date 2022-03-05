from sys import platform


class Config:

    @staticmethod
    def GetChromeDriverPath():
        if platform == 'linux':
            return './lib/driver/chromedriver'
