# this is the I/O implementation class
import importlib
import json
import os
import pathlib
import sys

import pandas as pd


def ReadPortfolio(fileName, logger) -> pd.core.frame.DataFrame:
    logger.LogDebug("Start to read portolio from " + str(fileName))
    try:
        if str(fileName).endswith(".xlsx"):
            portfolio = pd.read_excel(fileName)
        # portfolio.to_json(str(fileName).split('.')[0] + "_Input.json", orient="records")
        elif str(fileName).endswith(".json"):
            portfolio = pd.read_json(fileName)
        else:
            raise Exception("ReadPortfolio failed: File type not supported for file {}. only support .xlsx and .json".format(fileName))
        return portfolio
    except:
        logger.LogAndRaiseException(
            "something wrong with portfolio file  " + str(fileName) + " with error message :" + str(
                sys.exc_info()[0]) + " abort ")


def WriteToFile(fileName: str, data: str, logger) -> bool:
    try:
        with open(fileName, 'w') as f:
            f.write(data)
        return True
    except:
        logger.LogAndRaiseException("Write into file failed")
        return False


def WriteDictToJson(fileName: str, data: dict, logger) -> bool:
    try:
        with open(fileName, 'w') as json_file:
            json.dump(data, json_file)
        return True
    except:
        logger.LogAndRaiseException("Export to Json failed")
        return False


def WriteDataFrameToJson(fileName: str, logger, data: pd.DataFrame, orient="columns") -> bool:
    try:
        data.to_json(fileName, orient=orient)
        return True
    except:
        logger.LogAndRaiseException("Export to Json failed")
        return False


def ReadFromJson(fileName: str, logger) -> dict:
    try:
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)
        return data
    except:
        logger.LogAndRaiseException("Read form Json failed")
        return {}


def IsFileExist(filename: str, logger) -> bool:
    return pathlib.Path(filename).is_file()


def IsFilePathExist(filepath: pathlib.Path, logger) -> bool:
    return filepath.is_file()


def resetCwd(logger) -> None:
    logger.LogDebug("Current cwd is " + str(getRootPath(logger)))
    os.chdir(pathlib.Path(__file__).parents[2])  #
    logger.LogDebug("cwd changed to " + str(getRootPath(logger)))


def getRootPath(logger) -> pathlib.Path:
    # note: the IO Helper is placed under \src\utilities. so 2 layers from root
    return pathlib.Path(__file__).parents[2]


def loadConfig(file: pathlib.Path, logger) -> dict:
    # load config json file. Can also make a .py file and change the FrtbSaSbm.py a bit. but a py file may be difficult to distinguish plain config from executables.
    logger.LogInfo("config fileName:" + str(file))
    try:
        with open(file) as json_config_file:
            config = json.load(json_config_file)
        return config
    except:
        logger.LogAndRaiseException("failed to load config file")


def loadModules(moduleFolder: pathlib.Path, modulesWhiteList: list, logger) -> dict:
    # find modules
    modulesDir = []
    for aDir in moduleFolder.iterdir():
        if aDir.is_dir() and aDir.joinpath("__init__.py").is_file():
            modulesDir.append(aDir)
            logger.LogDebug("module found:" + str(aDir))
    # load the modules
    moduleList = {}
    for d in modulesDir:
        try:
            module_name = d.name.split('_')[0]  # remove _imp or _Engine
            if module_name not in modulesWhiteList:
                logger.LogDebug("module name {} not in config list, skip".format(d.name))
                continue

            # https://docs.python.org/3/library/importlib.html
            spec = importlib.util.spec_from_file_location(module_name, d.joinpath(module_name + ".py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # fill dictionary with modulename:module object
            moduleList[module_name] = getattr(module, module_name)(logger)  # getattr(module, str) returns a func handler by name, then () call it. a constructor returns the object
            logger.LogDebug("module loaded: " + module_name)

        except:
            logger.LogAndRaiseException('Module: {} not valid'.format(module_name))
            continue

    return moduleList


