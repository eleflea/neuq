class Config(object):
    pass

class TestConfig(Config):
    DEBUG = True
    DB_LIST = [{"name": "高等数学", "rep": "GS", "db": "GS.db"},
               {"name": "概率论与数理统计", "rep": "GL", "db": "GL.db"},
               {"name": "复变函数与积分变换", "rep": "FB", "db": "FB.db"}]
