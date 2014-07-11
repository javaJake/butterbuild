__all__ = ["java"]

class BaseUnit():
    
    def __init__(self, dependencies, sourceDir, targetDir):
        self.dependencies = dependencies
        self.sourceDir = sourceDir
        self.targetDir = targetDir
