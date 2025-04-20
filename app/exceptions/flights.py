class FlightTimeConflictError(Exception):
    """时间冲突异常，同一飞机在同一时间段内已被安排其他航班"""
    pass

class FlightTimestampOrderError(Exception):
    """时间顺序错误异常，到达时间早于起飞时间"""
    pass

class FlightActualVsEstimatedError(Exception):
    """实际时间早于预计时间异常"""
    pass

class FlightInvalidStatusError(Exception):
    """无效状态值异常，状态值不在预定义字典中"""
    pass