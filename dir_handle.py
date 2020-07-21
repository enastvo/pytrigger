import os


class directoryHandler:

    def __init__(self):
        self.dirName = "."

    def retrieve_file_paths(self, directory="none"):
        if directory == "none":
            directory = self.dirName
        # setup file paths variable
        fileList = []
        # Read all directory, subdirectories and file lists
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Create the full filepath by using os module.
                file_path = os.path.join(root, filename)
                fileList.append(file_path)
        # return all file paths
        return fileList


#current = directoryHandler()
#print(current.retrieve_file_paths())
