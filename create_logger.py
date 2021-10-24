import os
import logging
from datetime import datetime



####################################################################################################
#                                             Function                                             #
####################################################################################################
# 簡單的寫法
def create_logger():

    # 基本參數設定
    FILENAME = f'./log/{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}.log'
    FORMAT = '%(asctime)s %(levelname)s %(message)s'

    # 若參數不給 filemode、filename，則錯誤訊息會顯示在console中
    logging.basicConfig(level=logging.ERROR,
                        filemode='w',
                        filename=FILENAME,
                        format=FORMAT)
    
    # 輸出log資訊，參數exc_info=True 可將except訊息傳出
    logging.error('CatchError: ', exc_info=True)                # 也可寫成logger.exception('CatchError: ')



# 複雜詳細的寫法 (Recommend)
def create_logger():

    # 基本參數設定
    FILENAME = f'./log/{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}.log'
    FORMATE = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(FORMATE)

    # 建立logger、formatter
    # level等級：DEBUG(10) < INFO(20) < WARNING(30)	< ERROR(40) < CRITICAL(50)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # 建立file handler 用FileHandler將log輸出成檔案
    fileHandler = logging.FileHandler(filename=FILENAME, mode='w', encoding='utf-8')
    fileHandler.setFormatter(formatter)                         # 沒額外設定該Handler的level級數，就為logger.setLevel(logging.XXX)的初始設定
    logger.addHandler(fileHandler)

    # 建立console handler 用StreamHandler將log輸出到console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(logging.INFO)                       # 可額外設定每個Handler的level級數，若不設定就為logger.setLevel(logging.XXX)的初始設定
    logger.addHandler(consoleHandler)

    # 輸出log資訊，參數exc_info=True 可將except訊息傳出
    logger.error('CatchError: ', exc_info=True)                # 也可寫成logger.exception('CatchError: ')

    # 刪掉用完的Handler，避免程式在反覆呼叫function時，會重複出現之前的訊息
    logger.removeHandler(fileHandler)
    logger.removeHandler(consoleHandler)



####################################################################################################
#                                               Test                                               #
####################################################################################################
if __name__ == '__main__':

    # Create log directory
    if not os.path.exists('./log/'):
        os.makedirs('./log/')

    try:
        1 / 0
    except:
        create_logger()
        os._exit(0)
