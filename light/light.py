from yeelight import *
import time
import os

class LightRunner():
    def __init__(self, baseDir, ifDebug=True):
        self.baseDir = baseDir
        self.ifDebug = ifDebug
        self.bulb = Bulb("192.168.10.83")

    def startFlow(self, transitions):
        flow = Flow(
        count=1,
        transitions=transitions,
        action=Flow.actions.recover
        )
        self.bulb.start_flow(flow)

if __name__ == "__main__":
    lightRunner = LightRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    transitions = [
        RGBTransition(0, 0, 128, duration=3000, brightness=10),  # 深蓝色，低亮度，模拟天空刚开始亮起
        RGBTransition(255, 140, 0, duration=3000, brightness=60),  # 橙红色，中等亮度，模拟太阳刚刚升起
        RGBTransition(255, 215, 0, duration=3000, brightness=100),  # 金黄色，高亮度，模拟太阳完全升起
    ]
    lightRunner.startFlow(transitions)