from NBReader import NBReader


class NBComparator(object):
    def __init__(self):
        self.flag = True
        self.__file1 = None
        self.__file2 = None

    """
    Reads the Jupyter NB file
    """

    def __read_file(self, path):
        self.__reader = NBReader()
        try:
            self.__reader.read(path)
            return self.__reader.cells
        except Exception as e:
            print(e)
            print("Error in reading file at {}".format(path))

    """
    Compares the two notebook files
    """

    def compare(self, path1, path2):
        self.__file1 = self.__read_file(path1)
        self.__file2 = self.__read_file(path2)

        print(len(self.__file1) == len(self.__file2))
        assert len(self.__file1) == len(self.__file2), "First File has {} cells while second file has {}".format(
            len(self.__file1), len(self.__file2))

        for cell_num in range(len(self.__file1)):
            if self.__file1[cell_num] == self.__file2[cell_num]:
                pass
            else:
                self.flag = False
                print("Mismatch occured at cell number {}".format(cell_num))

        return self.flag
