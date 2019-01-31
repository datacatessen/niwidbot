import imp
import inspect
import os
import time

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)

    def decorate(func):
        lastTimeCalled = [0.0]

        def rateLimitedFunction(*args, **kargs):
            elapsed = time.time() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.time()
            return ret
        return rateLimitedFunction
    return decorate

def getPlugins(plugin_folder, main_module = "__init__"):
    plugins = []
    possibleplugins = os.listdir(plugin_folder)
    for i in possibleplugins:
        location = os.path.join(plugin_folder, i)
        if not os.path.isdir(location) or not main_module + ".py" in os.listdir(location):
            continue
        info = imp.find_module(main_module, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def loadPlugin(plugin, main_module = "__init__"):
    return imp.load_module(main_module, *plugin["info"])

def getPluginsByType(plugin_folder, type_str):
    for module in getPlugins(plugin_folder):
        for name, obj in inspect.getmembers(loadPlugin(module), inspect.isclass):
            if inherits_from(obj, type_str): 
                yield obj

def inherits_from(child, parent_name):
    if inspect.isclass(child):
        if parent_name in [c.__name__ for c in inspect.getmro(child)[1:]]:
            return True
    return False
