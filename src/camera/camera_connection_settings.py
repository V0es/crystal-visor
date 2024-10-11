from dataclasses import dataclass


@dataclass
class CameraConnection:
    ip_address: str = None
    port: int = None
    username: str = None
    password: str = None
    stream: int = 'main'
