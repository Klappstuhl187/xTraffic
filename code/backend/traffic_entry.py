from typing import Optional

class TrafficEntry():
    id: int
    crossingId: int
    time1: Optional[float]
    time2: Optional[float]
    speed: Optional[float]
    countdown: Optional[float]
