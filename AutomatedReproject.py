# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:46:45 2022

@author: joefa
"""
# This script reprojects all feature classes in a target folder into
# the spatial reference of the target dataset if the spatial references do
# not already match

import arcpy

# Set input variables for the target folder and target dataset, allowing for 
# user input 
targetFolder = arcpy.GetParameterAsText(0)
targetProjectionDataset = arcpy.GetParameterAsText(1)

# Set the workspace to the target folder so the reprojected feature classes are
# saved there
arcpy.env.workspace = targetFolder

# Get a list of feature classes from target folder
featureClasses = arcpy.ListFeatureClasses()

# Get spatial reference object of the target dataset and save it to variable
# targetProj to be used as a parameter in the project tool. Get the name of 
# the spatial reference and save it as targetProjName to be used to 
# compare to the spatial references of the other feature classes.
desc = arcpy.Describe(targetProjectionDataset)
targetProj = desc.spatialReference
targetProjName = targetProj.Name


# Create an string that all reprojected feature classes can be appended to 
# to be used as an message to the user. 
reprojMessage = "Projected "

# Set up a try-except to exit program and deliver error message to user in the event
# of a failure. 
try: 
    # Loop through each feature class in the target folder and get the name of their
    # spatial reference. 
    for feature in featureClasses:
        featureProj = arcpy.Describe(feature).spatialReference.Name
        # Compare the feature's spatial reference to that of the target dataset's
        # if they are different, reproject the feature to the target dataset's spatial 
        # reference, remove .shp at the end, and appened _projected to the output name.
        # Save the new feature classes to the target folder. If they are the same, do nothing. 
        if featureProj != targetProjName:
            # Add the name of reprojected feature classes to the reprojMessage string.
            reprojMessage += feature + ", "
            outputName = feature.replace(".shp", "")
            outputName += "_projected"
            arcpy.Project_management(feature, outputName, targetProj)
       
        
        
    # Remove the final comma from the list of reprojected feature classes 
    # and return the message to the user. 
    reprojMessage = reprojMessage.rstrip(", ")
    print(reprojMessage)
    arcpy.AddMessage(reprojMessage)
    
except:
    arcpy.AddMessage("Reproject Data In Folder Tool Failed.")