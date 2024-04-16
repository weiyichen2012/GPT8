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
        # self.bulb = Bulb("192.168.1.101")

    def startFlow(self, transitions, count):

        self.bulb = Bulb("192.168.1.101")
        flow = Flow(
            count=count,
            transitions=transitions,
            action=Flow.actions.recover
        )
        self.bulb.start_flow(flow)
        # self.bulb.

    def getLightJSONDuration(self, json):
        durations = []
        for transition in json['transitions']:
            if 'RGBTransition' in transition:
                tmp_transition = transition['RGBTransition']

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
            elif 'HSVTransition' in transition:
                tmp_duration = 1
                pattern = regex.findall(r'duration=(.*)', transition['HSVTransition'][2])
                if len(pattern) > 0:
                    tmp_duration = int(pattern[0])
                durations.append(tmp_duration / 1000.0)
            elif 'TemperatureTransition' in transition:
                tmp_duration = 1
                pattern = regex.findall(r'duration=(.*)', transition['TemperatureTransition'][1])
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
        # os.chdir(self.selfBaseDir)
        f = open(self.selfBaseDir + filename, 'r')
        obj = json.loads(f.read())
        return self.getLightJSONDuration(obj)

    def startFlowByJSON(self, json):
        transitions = []
        for transition in json['transitions']:
            # print(transition)
            if 'RGBTransition' in transition:
                tmp_transition = transition['RGBTransition']

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
            elif 'TemperatureTransition' in transition:
                temperature = 3500
                duration = 1000
                brightness = 60
                
                pattern = regex.findall(r'temperature=(.*)', transition['TemperatureTransition'][0])
                if len(pattern) > 0:
                    temperature = int(pattern[0])

                pattern = regex.findall(r'duration=(.*)', transition['TemperatureTransition'][1])
                if len(pattern) > 0:
                    duration = int(pattern[0])
                
                pattern = regex.findall(r'brightness=(.*)', transition['TemperatureTransition'][2])
                if len(pattern) > 0:
                    brightness = int(pattern[0])
                
                transitions.append(TemperatureTransition(temperature, duration=duration, brightness=brightness))
            elif 'HSVTransition' in transition:
                hue = transition['HSVTransition'][0]
                saturation = transition['HSVTransition'][1]
                duration = 1000
                brightness = 60
                
                pattern = regex.findall(r'duration=(.*)', transition['HSVTransition'][2])
                if len(pattern) > 0:
                    duration = int(pattern[0])
                
                pattern = regex.findall(r'brightness=(.*)', transition['HSVTransition'][3])
                if len(pattern) > 0:
                    brightness = int(pattern[0])
                
                transitions.append(HSVTransition(hue=hue, saturation=saturation, duration=duration, brightness=brightness))
            else:
                print('Error in light: unknown transition type')
        
        # print(json['flow']['count'])
        self.startFlow(transitions, json['flow']['count'])
        if self.ifDebug:
            print(json['flow']['count'], transitions)


    def startFlowByFile(self, filename):
        # os.chdir(self.selfBaseDir)
        f = open(self.selfBaseDir + filename, 'r')
        obj = json.loads(f.read())
        return self.startFlowByJSON(obj)


if __name__ == "__main__":
    lightRunner = LightRunner(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    # json = json.loads()
    lightRunner.startFlowByFile('effect2.json')
    lightRunner.getLightJSONDurationByFile('effect2.json')