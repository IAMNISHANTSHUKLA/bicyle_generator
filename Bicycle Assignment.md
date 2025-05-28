# Bicycle Assignment

We are managing a bicycle store and sell bicycles from various manufacturers. Manufacturers produce many modifications of same bicycle type using different parts and we document those modifications using excel files. We want to track stock of every specific modification in our warehouse and provide its specification to the users. Your task is to help us by implementing a bicycle generator.

## Excel file format

Input Excel file (.xlsx) contains bicycle specifications in a condensed format. A file contains multiple sheets:
1. Sheet "ID" contains a table which should be used to construct all possible bicycle IDs. ID can be dissected into designators - substrings having a specific meaning. For example, we could say that a calendar date "January 31st, 1999" expressed as "19990131" has 3 designators: year, month and day with their values respectively "1999", "01" and "31". So the "ID" sheet contains ID designator names in the first row with all their possible values in subsequent rows. 
2. Sheet "GENERAL" contains a table with fields common to all modifications. First row contains field names and the second row contains field values.
3. All other sheets contain one table each with fields that are dependent on specific designator values. First column contains designator name with designator values and other columns contain field name and values that should be assigned respectively to bicycle modifications with ID containing the designator value on the left column.

**Note** - all field names and values can be interpreted as strings.

An example Excel file "Bicycle.xlsx" will be provided with the task.

## Output JSON document format

The output of the bycicle generator must be a JSON document containing all possible bicycle permutations from the input Excel file. The content of the JSON document must be a list of JSON objects, where each object is a description for a single bycicle modification with keys being field names and values being field values from the specification in Excel file. The only mandatory bicycle object key is "ID" with its value being the generated bicycle modification ID. Here is an example of the JSON output produced from the example "Bicycle.xlsx" (note that the example contains only 2 modifications, while your bicycle generator must generate all possible modifications).
```
[
    {
        "ID": "CITY-R26SSH1-01",
        "Manufacturer": "Bikes INC",
        "Type": "City",
        "Frame type": "Diamond",
        "Frame material": "Aluminum",
        "Brake type": "Rim",
        "Brake warranty": "2 years",
        "Operating temperature": "0 - 40 °C",
        "Wheel diameter": "26″",
        "Recommended height": "168-174 cm",
        "Frame height": "16 in",
        "Groupset manufacturer": "Shimano",
        "Groupset name": "Acera",
        "Gears": "27",
        "Has suspension": "FALSE",
        "Suspension travel": "Not applicable",
        "Frame color": "RED",
        "Logo": "TRUE"
    },
    {
        "ID": "CITY-D27MSH3C08",
        "Manufacturer": "Bikes INC",
        "Type": "City",
        "Frame type": "Diamond",
        "Frame material": "Aluminum",
        "Brake type": "Disc",
        "Brake warranty": "5 years",
        "Operating temperature": "-20 - 50 °C",
        "Wheel diameter": "27″",
        "Recommended height": "174-180 cm",
        "Frame height": "18 in",
        "Groupset manufacturer": "Shimano",
        "Groupset name": "Tourney",
        "Gears": "18",
        "Has suspension": "TRUE",
        "Suspension travel": "80 mm",
        "Frame color": "CYAN",
        "Logo": "FALSE"
    }
]
```

## Requirements

1. The bicycle generator must be implemented as Python module. 
2. The input for the bicycle generator must be a string with an absolute path to a single Excel file (.xlsx) and its output must be a string containing the JSON document.
3. (optional) at least one automated test using input and checking output as required above.

