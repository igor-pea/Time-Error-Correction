# -*- coding: utf-8 -*-
"""Contains methods for data assimilation."""


import numpy as analytics
from scipy import stats     
import math                 
import EnsembleOperations  






def get_posterior(ensembleValues, observation, observationError):
    """
    Assuming normality, uses Bayes' Rule to find the posterior distribution from an ensemble/prior and an observation distribution.
    
    Takes ensembleValues (observed only, as returned by get_observed_values_from_ensemble), observation as array of variable values in same order as ensemble, and assumed error in observations.
    """
    #Convenience
    numberOfVariables = len(ensembleValues)    
    
    #Priors    
    ensembleMeans = [analytics.mean(valueList) for valueList in ensembleValues]
    ensembleSpreads = [analytics.std(valueList) for valueList in ensembleValues]
    
    #Compute Posterior 
    posteriorMeans = []
    posteriorSpreads = []
    for variable in range(numberOfVariables):
        #If there is no spread in the ensemble, it is completely certain and we don't need to adjust it.
        if ensembleSpreads[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(ensembleMeans[variable])
        #If there is no spread in the observation likelihood, we are completely certain it is accurate and we can set the ensemble to its value.
        elif observationError[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(observation[variable])
            
        #If there is spread in both ensemble and observation:
        #                 ______________________
        #                /__________1___________
        #std-post =     /____1____  + ___1___    
        #             \/(std-pri)^2  (std-lik)^2
        # and
        #
        #mean-post = (std-post)^2 *   ___mean-pri___  +  ____obs____
        #                              (std-pri)^2       (std-lik)^2
        #
        #where pri is prior, obs is observed (lik is observation likelihood), and post is posterior
        
        else:
            spread = ensembleSpreads[variable]
            observationLikelihoodError = observationError[variable]
            posteriorSpread = math.sqrt(1/((spread)**-2 + (observationLikelihoodError)**-2))
            posteriorSpreads.append(posteriorSpread)
            posteriorMeans.append((posteriorSpreads[variable]**2)*(ensembleMeans[variable]*ensembleSpreads[variable]**-2 + observation[variable]*observationError[variable]**-2))
               
    return posteriorSpreads, posteriorMeans
    



    
def get_state_inc(ensembleValues, observationIncrements, index):
    """
    Regresses observation increments for one variable onto other variables.

    Takes ensembleValues in full, observation increments for one variable, and the index(position in ensembleValues) of the observed variable.    
    """
    stateIncrements = []
    for unobserved in range(len(ensembleValues)):
        slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleValues[index][1],ensembleValues[unobserved][1])
        stateIncrements.append(list(analytics.array(observationIncrements)*slope))
    return stateIncrements
  

      
    
    
def apply_state_inc(ensembleValues, stateIncrements):
    """
    Applies state increments from one variable generated by get_state_inc.
    """
    newEnsembleValues = EnsembleOperations.copy_ensemble_values(ensembleValues)
    for var in range(len(stateIncrements)):
        newEnsembleValues[var][1] = [newEnsembleValues[var][1][point] + stateIncrements[var][point] for point in range(len(ensembleValues[var][1]))]
    return newEnsembleValues





def obs_inc_EAKF(ensembleValues, posteriorMean, posteriorSpread):
    """
    Calculates observation increments for one variable based on prior and posterior distributions.
    
    Takes one list of values i.e. ensembleValues[i] and information about posterior.
    Returns list of observation increments.
    """
    #Priors        
    ensembleMean = analytics.mean(ensembleValues)
    ensembleSpread = analytics.std(ensembleValues)
    observedIncrements = []
    meanDifference = posteriorMean - ensembleMean
    spreadRatio = posteriorSpread / ensembleSpread
    for point in ensembleValues:
        newValue = point + meanDifference
        distanceFromPosteriorMean = newValue - posteriorMean
        distanceFromPosteriorMean *= spreadRatio
        observedIncrements.append(posteriorMean + distanceFromPosteriorMean - point)
    return observedIncrements
        
        
        
        
        
def EAKF(ensemble, observation, observationError, observedStatus):
    """
    Performs an EAKF assimilation with linear regression. 
    
    Takes ensemble in standard format, observation, assumed observation error, observedStatus as array with length = number of variables. Returns ensemble.
    """
    ensembleValues = EnsembleOperations.get_values_from_ensemble(ensemble, observedStatus) #Yes
    observedValues = EnsembleOperations.get_observed_values_from_ensemble(ensembleValues)  #Yes
    posteriorSpreads, posteriorMeans = get_posterior(observedValues, observation, observationError)
    for i in range(len(ensembleValues)):
        ensembleValues = apply_state_inc(ensembleValues, get_state_inc(ensembleValues,obs_inc_EAKF(ensembleValues[i][1], posteriorMeans[i], posteriorSpreads[i]) ,i))
    #observedIncrements = obs_incs_EAKF(observedValues, posteriorMeans, posteriorSpreads)
    #newEnsembleValues = EnsembleOperations.copy_ensemble_values(ensembleValues)
    #newEnsembleValues = apply_state_increments(ensembleValues, get_state_incs(ensembleValues, observedIncrements)[0])
    ensemble = EnsembleOperations.get_ensemble_from_values(ensembleValues)
    return ensemble
                
            
            
    
    
