# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 10:53:43 2020

@author: mottig
"""
import json,codecs
import os

class JsonNode:
    
    def __init__(self,jsonDic = {},path = ""):
        
        if type(jsonDic) == dict and len(jsonDic) != 0:
            self.__jsonDic = jsonDic
        elif len(path).equale() != 0 and len(jsonDic) == 0:
            with open(path,mode = "r+",encoding="utf8") as jsonFile:
                self.__jsonDic = json.load(jsonFile)
        elif len(path) != 0 and len(jsonDic) !=0 :
            raise Exception("Please insert Dict object or a valid path not both")
        else:
            self.__jsonDic = {}
            
    def __repr__(self):
        
        return str(self.__jsonDic)
    
    def getJson(self):
        
        return self.__jsonDic
    
    def setNewJson(self,newDic):
        
        if isinstance(newDic,dict):
            self.__jsonDic = newDic
        else:
            raise Exception("please insert valid Dict") 
    
    def getAllKeys(self,passingDic={}):
        keysList = set()
        for mainKey in passingDic.keys():
                keysList.add(mainKey)
        for key,value in passingDic.items():
            if self.__checkNotDictAndNotList(value) and key not in keysList:
                keysList.add(key)
                
            elif  isinstance(value,dict):
                for keyInDic in self.getAllKeys(value):
                    keysList.add(keyInDic)
                          
            elif  isinstance(value,dict):
                for dic in value:
                    if isinstance(dic,dict):
                            for keyInSmallDic in self.getAllKeys(dic):
                                keysList.add(keyInSmallDic)
        return keysList

    def checkIfKeyExsists(self,searchKey):
        if searchKey not in self.getAllKeys(self.getJson()):
            return False
        else:
            return True
    
    def minimizeJsonByKey(self,key):
        
       if isinstance(self.__jsonDic[key],dict):
           self.__jsonDic = self.__jsonDic[key]
       else: 
           raise Exception("The key is not exists or the value is not valid dict")        

    def loadJsonFileFromDir(self,path):
        
        if path.endswith("json"):
            with open(path,mode = "r+",encoding="utf8") as jsonFile:
                self.__jsonDic = json.load(jsonFile)
        else:
            raise Exception ("Please insert valid path to a JSON file")
        
    def updateValueByKey(self,key,value):
        if self.checkIfKeyExsists(key):
            self.__jsonDic[key] = value
        else:
            raise Exception ("The key is not exists")
        
    def createNewJsonFileInDir(self,newFileName="New File"):
        jsonObject = json.dumps(self.__jsonDic)
        with codecs.open(newFileName+".json", 'w',encoding="utf8") as r:
                r.write(jsonObject)
    
    def replaceKey(self,keyToReplace,newKey):
        if keyToReplace not in self.getAllKeys(self.__jsonDic):
            raise Exception ("The key is not exists")
        jsonString = json.dumps(self.__jsonDic).replace(keyToReplace,newKey)
        self.__jsonDic = json.loads(jsonString)
    
    def getAllValuesOccurrence(self,passingDic,newDict = {}):
        for value in passingDic.values():
            if self.__checkNotDictAndNotList(value) and value not in newDict:
                newDict[value] = 1
            elif self.__checkNotDictAndNotList(value) and value in newDict:
                newDict[value] = newDict[value] + 1
            elif isinstance(value,dict):
                 self.getAllValuesOccurrence(value,newDict)
            elif isinstance(value,list):
                 for itemInList in value:
                     if isinstance(itemInList,dict):
                         self.getAllValuesOccurrence(itemInList,newDict)
                     elif self.__checkNotDictAndNotList(itemInList) and itemInList not in newDict:
                         newDict[itemInList] = 1
                     elif self.__checkNotDictAndNotList(itemInList) and itemInList  in newDict:
                         newDict[itemInList] = newDict[itemInList] + 1
                     
        return newDict
    
    def __checkNotDictAndNotList(self,value):
        if not isinstance(value,dict) and not isinstance(value,list):
            return True
        else:
            return False 