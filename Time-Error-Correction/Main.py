# -*- coding: utf-8 -*-
"""Mainfile for running the experimental code."""

import AnalysisOperations
import AssimDiagTest
import DataAssimilation
import EnsembleOperations
import ExperimentalThings
import Files
import Graphics
import IntegrationMethods
import MiscFunctions
import Process
import Systems

#Preconditions for experiment
assimilationMethods = ["RHF"]
testingTypes = [True, False]
stateErrors = [[0.01, 0.01, 0.01], [0.05, 0.05, 0.05], [0.1, 0.1, 0.1]]
timeErrors = [0.001*i for i in range(0, 100)]
errors = [i+j for i in stateErrors for j in timeErrors]
startTime = 0
endTime = 200
trials = 3
observationIntervals = [0.5]
systems = ["L63+time", "L84+time"]

#Writing to files
filename = "" + ".csv"
file = open(filename, "a")
file.write("testingType, system, assimilationMethod, observationInterval, stateError, timeError, RMSE")
file.close()

#Python was not made for this many for loops :|
for testingType in testingTypes:
    for system in systems:
        for assimilationMethod in assimilationMethods:
            for observationInterval in observationIntervals:
                for error in errors:
                    for trial in range(trials):
                        Experiment = Process.Process(system=system, assimilation=assimilationMethod)
                        truthList, timeList = Experiment.get_truth(startTime, endTime, 0.01, [1,1,1,0])
                        obsList, obsTimeList = Experiment.get_observations(observationInterval, error, ["State", "State", "State", "Time"])
                        ensembleList, ensembleTimeList = Experiment.run_ensemble(startTime, endTime, 0.01, 80, error, [1,1,1,0], obsList[0], [True, True, True, False], [1.5, 1.5, 1.5, 0])
                        ensembleMeans = Experiment.get_ensemble_means()
                        rmse = AnalysisOperations.get_RMSE(ensembleMeans, truthList, [True, True, True, False])
                        #TODO: Move file writing to its own module
                        file = open(filename, "a")
                        file.write(str(testingType) + "," + str(system) + "," + str(assimilationMethod) + "," + str(observationInterval) + "," + str(error[0]) + "," + str(error[3]) + "," + str(rmse))
                        file.close()    #Free up system resources and make sure not everything is lost if the code errors
                    
                
            
 

