import os


class Media:
    def __init__(self, rootDirPath) -> None:
        self.rootDirPath = rootDirPath
        self.mediaDirectories = list(
            filter(lambda f: not (f in ".DS_Store"), os.listdir(rootDirPath))
        )
        pass

    # def getMedia(self, extensionPath):
    #     return self.rootDir

    def getMedia(self, mediaDir):
        if mediaDir:
            mediaDirPath = os.path.join(self.rootDirPath, mediaDir)
            return list(
                filter(lambda f: not (f in ".DS_Store"), os.listdir(mediaDirPath))
            )
        else:
            return self.mediaDirectories
