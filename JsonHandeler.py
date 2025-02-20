import json

class Json :
    def __init__(self, jsonName : str) -> None:
        self.jsonName = jsonName

    def Store(self, items : map) -> None :
        with open(self.jsonName, "w") as outfile : # save the json with updated info
            json.dump(items, outfile)
    
    def Open(self, item : str = None) -> map:
        with open(self.jsonName) as fp: #open the jsonfile
            items : map = json.load(fp)
        if item == None :
            return items
        return items[item]
    
    def Change(self, index : str, item : any) -> None:
        items = self.Open()
        items[index] = item
        self.Store(items)
        