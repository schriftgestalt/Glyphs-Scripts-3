#MenuTitle: Generate avar xml
# -*- coding: utf-8 -*-
"""
Generates an avar table for patching in xml
Works based on the following assumptions:
	• Font has a custom parameter for “Variation Font Origin”
	• Masters are ordered thinnest to boldest
	• The extreme masters have the custom parameter “Axes Location”
	• Instances are ordered thinnest to boldest
	• Instances are named conventionally
"""

import re

font = Glyphs.font

cssMin = float(font.masters[0].customParameters['Axis Location'][0]['Location'])
cssMax = float(font.masters[-1].customParameters['Axis Location'][0]['Location'])
cssDefault = font.masters[font.customParameters['Variation Font Origin']].customParameters['Axis Location'][0]['Location']
weightMin = font.instances[0].weightValue
weightMax = font.instances[-1].weightValue
weightDefault = font.masters[font.customParameters['Variation Font Origin']].weightValue

def convertWeight(inputWeight):
	outputWeight = (((inputWeight - weightMin) / (weightMax-weightMin)) * (cssMax - cssMin)) + cssMin
	return outputWeight
	
table = "<avar>\n  <segment axis=\"wght\">\n"

def stripItalic(name):
	name = re.sub(' Italic', '', name)
	return name
	

for instance in font.instances:
	if instance.active == True:
		# scaled fvar weight based on a min and max intended weights
		scaledWeight = convertWeight(instance.weightValue)

		
		# css weight based on canonical naming
		if stripItalic(instance.name)  == "Thin":
			cssWeight = 100
		elif stripItalic(instance.name)  == "ExtraLight" or stripItalic(instance.name) == "UltraLight":
			cssWeight = 200
		elif stripItalic(instance.name)  == "Light":
			cssWeight = 300
		elif stripItalic(instance.name)  == "Regular":
			cssWeight = 400
		elif stripItalic(instance.name)  == "Medium":
			cssWeight = 500
		elif stripItalic(instance.name)  == "SemiBold":
			cssWeight = 600
		elif stripItalic(instance.name)  == "Bold":
			cssWeight = 700
		elif stripItalic(instance.name)  == "ExtraBold" or stripItalic(instance.name) == "UltraBold":
			cssWeight = 800
		elif stripItalic(instance.name)  == "Black" or stripItalic(instance.name) == "Heavy":
			cssWeight = 900
		elif stripItalic(instance.name)  == "Hairline":
			cssWeight = 0
		else:
			cssWeight = 1000
		
		# toValue is the normalized value on the original scale (based on scaled weight)
		# fromValue is the normalized value on the post-mapping scale (100, 200, 300, etc.)
		if instance.weightValue <= weightDefault and weightMin != weightDefault:
			toValue = ((scaledWeight - cssMin) / (convertWeight(weightDefault) - cssMin)) - 1
			fromValue = ((cssWeight - cssMin) / (cssDefault - cssMin)) - 1
		elif instance.weightValue >= weightDefault:
			toValue = (scaledWeight - convertWeight(weightDefault)) / (cssMax - convertWeight(weightDefault))
			fromValue = (cssWeight - cssDefault) / (cssMax - cssDefault)
		
		# print values
		print stripItalic(instance.name)
		print "Original weight = %f" % instance.weightValue
		print "Scaled Weight = %f" % scaledWeight
		print "CSS weight = %f" % cssWeight
		print "avar to value = %f" % toValue
		print "avar from value = %f" % fromValue
		print "\n"
		mapping = "    <mapping from=\"%f\" to=\"%f\" />\n" % (fromValue, toValue)
		table = table + mapping
		
table = table + "  </segment>\n</avar>"
print table

Glyphs.showMacroWindow()
