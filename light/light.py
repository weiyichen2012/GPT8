from yeelight import *
import time
import os
import json
import regex

class LightRunner():
    def __init__(self, baseDir, ifDebug=True):
        self.baseDir = baseDir
        self.selfBaseDir = baseDir + '/light/'
        self.ifDebug = ifDebug
        self.bulb = Bulb("192.168.1.101")

    def startFlow(self, transitions, count):
        flow = Flow(
            count=count,
            transitions=transitions,
            action=Flow.actions.recover
        )
        self.bulb.start_flow(flow)

    def getLightJSONDuration(self, json):
        durations = []
        for transition in json['transitions']:
            if 'RGBTRansition' in transition:
                tmp_transition = transition['RGBTRansition']

                tmp_duration = 1
                pattern = regex.findall(r'duration=(.*)', tmp_transition[3])
                if len(pattern) > 0:
                    tmp_duration = int(pattern[0])

                durations.append(tmp_duration / 1000.0)
            elif 'SleepTransition' in transition:
                tmp_duration = 1
                pattern = regex.findall(r'duration=(.*)', transition['SleepTransition'][0])
                if len(pattern) > 0:
                    tmp_duration = int(pattern[0])
                durations.append(tmp_duration / 1000.0)
            else:
                print('Error in light: unknown transition type')
        
        for i in range(1, json['flow']['count']):
            durations.extend(durations.copy())

        if self.ifDebug:
            print(durations)

        return durations

    def getLightJSONDurationByFile(self, filename):
        os.chdir(self.selfBaseDir)
        f = open(filename, 'r')
        obj = json.loads(f.read())
        return self.getLightJSONDuration(obj)

    def startFlowByJSON(self, json):
        transitions = []
        for transition in json['transitions']:
            # print(transition)
            if 'RGBTRansition' in transition:
                tmp_transition = transition['RGBTRansition']

                duration = 1000
                brightness = 50

                pattern = regex.findall(r'duration=(.*)', tmp_transition[3])
                if len(pattern) > 0:
                    duration = int(pattern[0])
                
                pattern = regex.findall(r'brightness=(.*)', tmp_transition[4])
                if len(pattern) > 0:
                    brightness = int(pattern[0])

                transitions.append(RGBTransition(tmp_transition[0], tmp_transition[1], tmp_transition[2], duration=duration, brightness=brightness))
            elif 'SleepTransition' in transition:
                duration = 1000
                pattern = regex.findall(r'duration=(.*)', transition['SleepTransition'][0])
                if len(pattern) > 0:
                    duration = int(pattern[0])

                transitions.append(SleepTransition(duration=duration))
            else:
                print('Error in light: unknown transition type')
        
        # print(json['flow']['count'])
        self.startFlow(transitions, json['flow']['count'])
        if self.ifDebug:
            print(json['flow']['count'], transitions)


    def startFlowByFile(self, filename):
        os.chdir(self.selfBaseDir)
        f = open(filename, 'r')
        obj = json.loads(f.read())
        return self.startFlowByJSON(obj)


if __name__ == "__main__":
    lightRunner = LightRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    # json = json.loads()
    lightRunner.startFlowByFile('effect1.json')
    lightRunner.getLightJSONDurationByFile('effect1.json')