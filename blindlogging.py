import logging
import logging.config

logging.config.fileConfig('logging.conf')
blind_logger = logging.getLogger('blind_logger')
member_logger = logging.getLogger('member_logger')
member_DAO_logger = logging.getLogger('member_DAO_logger')
board_DAO_logger = logging.getLogger("blind_board_DAO")
logger_reply = logging.getLogger('blind_reply_DAO')
logger_board = logging.getLogger("board")
logging.getLogger('werkzeug').disabled=True

# # Werkzeug 로거를 가져옵니다.
# werkzeug_log = logging.getLogger('werkzeug')

# # Werkzeug 로그를 저장할 별도의 파일 핸들러를 생성합니다.
# werkzeug_file_handler = logging.FileHandler('werkzeug.log')

# # Werkzeug 로그 핸들러를 로거에 추가합니다.
# werkzeug_log.addHandler(werkzeug_file_handler)


if __name__ == '__main__' :
    blind_logger.debug('debug...')
    member_logger.info('info...')
    member_DAO_logger.warning('warning...')
    blind_logger.error('error...')
    member_logger.critical('critical...')