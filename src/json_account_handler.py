import json

class JSON_Account_Handler(object):
    def __init__(self,*,json_key, json_value_list):
        self.__data = {}
        self.__verbose = []
        self.add_to_json (json_key=json_key,
                            json_value_list=json_value_list)

    def __is_hashable(self, json_key):
        return '__hash__' in dir(json_key)

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, *, new_json_dict):
        self.__data = new_json_dict
    
    @property
    def verbose(self):
        return self.__verbose
    
    @verbose.setter
    def verbose(self, *, new_verbose):
        self.__verbose = new_verbose

    def add_to_json(self, *,json_key, json_value_list):
        __verbose = self.__verbose
        __data = self.__data
        
        if self.__is_hashable(json_key) == False:
            raise KeyError("Immutable type cannot be json dictionary key")
        else:
            if json_key in __data:
                __verbose.append(f"Value of key:{json_key} has been updated")
            else:
                __data[json_key] = json_value_list
                __verbose.append(f"New key:{json_key} has been created")

    def write_json_to_txt(self):
        __data = self.__data
        __verbose = self.__verbose
        with open('json_data.txt', 'w') as outfile:
            json.dump(__data, outfile)
            __verbose.append(f"Json text file has been created")
    
    def read_json_from_txt(self):
        __data = self.__data
        __verbose = self.__verbose
        with open('json_data.txt') as json_file:
            __data = json.load(json_file)
            __verbose.append(f"Json file has been read")

    def print_verbose(self):
        __verbose = self.__verbose
        print(*__verbose,sep='\n')
        
    def __str__(self):
        __data = self.__data
        return f"{[key for key in __data]}"

    def __del__(self):
        pass

"""
if __name__ == "__main__":
    test_account = JSON_Account_Handler(
                                json_key='name',
                                json_value_list=[
                                    {
                                        'username': 'test_username',
                                        'password': 'test_password'
                                    }
                                ])

    test_account.write_json_to_txt()
    test_account.print_verbose()
"""