A Solution to Streamlined Bicycle Data Processing
Managing and transforming bicycle specification data from Excel files into structured, usable formats can often be tedious and error-prone—especially when dealing with large datasets and varied business logic. The Bicycle Generator Module offers a complete, modular, and testable Python-based solution to this problem. Designed with clarity and simplicity, it provides an easy-to-follow file structure and guide that lets users quickly get started. The project requires three key files in one directory: the main logic in bicycle_generator.py, a comprehensive test suite in test_bicycle_generator.py, and the input data in Bicycle.xlsx. With just a couple of commands, users can install the necessary dependencies (pandas, openpyxl), run a full-featured test suite, and see a demonstration of the module’s functionality including test data generation, validation checks, and output previews. Whether used interactively in Python, from the command line, or embedded in a production pipeline, this tool ensures that raw Excel data can be transformed into structured JSON outputs efficiently and reliably. The guide also covers troubleshooting common errors like missing dependencies or file path issues, ensuring a smooth setup experience. With robust testing and modularity at its core, this solution drastically simplifies the process of managing bicycle catalogs and enables seamless integration into broader applications or analytics workflows.



# Bicycle Generator

A Python module that generates all possible bicycle configurations from Excel specification files. This tool reads bicycle component options from an Excel file and produces a comprehensive JSON document containing every possible bicycle variant with complete specifications.

## Overview

The Bicycle Generator processes Excel files containing bicycle component options (brakes, wheels, frame sizes, etc.) and generates all valid combinations as fully-specified bicycle configurations. Each generated bicycle includes detailed specifications for all components, pricing, and technical details.

## Requirements Fulfilled

This implementation satisfies the following core requirements:

1. **Python Module Implementation**: Implemented as a proper Python module with importable functions
2. **String Input/Output Interface**: Takes a string path to an Excel file and returns a JSON string
3. **Automated Testing**: Includes comprehensive unit tests with input/output validation

## Installation

No external dependencies beyond standard Python libraries are required. The module uses:
- `pandas` - For Excel file processing
- `json` - For JSON output formatting
- `itertools` - For generating combinations
- `pathlib` - For file path handling

```bash
pip install pandas openpyxl
```

## Usage

### As a Python Module (Recommended)

```python
import bicycle_generator
import json

# Generate bicycles from Excel file
json_output = bicycle_generator.generate_bicycles("/path/to/bicycle_specs.xlsx")

# Parse the JSON output
bicycles = json.loads(json_output)

print(f"Generated {len(bicycles)} bicycle configurations")

# Access individual bicycle specifications
for bike in bicycles[:3]:  # Show first 3 bikes
    print(f"Bike ID: {bike['ID']}")
    print(f"Frame Color: {bike.get('Frame color', 'N/A')}")
    print(f"Brake Type: {bike.get('Brake type', 'N/A')}")
    print("---")
```

### As a Command Line Script

```bash
python bicycle_generator.py /path/to/bicycle_specs.xlsx
```

This will output the complete JSON document to stdout, which can be redirected to a file:

```bash
python bicycle_generator.py bicycle_specs.xlsx > generated_bicycles.json
```

## Input File Format

The module accepts Excel (.xlsx) files in two formats:

### Format 1: Multi-Sheet Structure
- **ID Sheet**: Contains component options in columns (Model number, Brakes, Wheels, Frame size, Groupset, Suspension, Color)
- **GENERAL Sheet**: Contains common specifications (Manufacturer, Type, Frame material)
- Additional component-specific sheets (optional)

### Format 2: Single Sheet (CSV-like)
A single sheet with component options in columns, where each column contains all possible values for that component type.

Example structure:
```
Model number | Brakes | Wheels | Frame size | Groupset | Suspension | Color
CITY-        | R      | 26     | S          | SH1      | -          | 01
             | D      | 27     | M          | SH2      | C          | 02
             |        | 29     | L          | SH3      | A          | 03
```

## Output Format

The module returns a JSON string containing an array of bicycle objects. Each bicycle includes:

- **ID**: Unique identifier combining all component codes
- **General specifications**: Manufacturer, type, frame material, etc.
- **Component-specific details**: Brake types, wheel specifications, groupset details, suspension info, color options

Example output:
```json
[
  {
    "ID": "CITY-R26SSH1-01",
    "Manufacturer": "Bikes INC",
    "Type": "City",
    "Frame type": "Diamond",
    "Frame material": "Aluminum",
    "Brake type": "Rim",
    "Brake warranty": "2 years",
    "Wheel diameter": "26″",
    "Recommended height": "168-174 cm",
    "Frame height": "16 in",
    "Groupset manufacturer": "Shimano",
    "Groupset name": "Acera",
    "Gears": "27",
    "Has suspension": "FALSE",
    "Frame color": "RED",
    "Logo": "TRUE"
  }
]
```

## Testing

The module includes comprehensive automated tests that validate:

- Input/output requirements
- Excel file processing
- JSON output format
- Component specification accuracy
- Error handling

Run the tests:

```bash
python test_bicycle_generator.py
```

Or run tests with the module:

```bash
python -m unittest test_bicycle_generator
```

## Error Handling

The module provides clear error messages for common issues:

- **FileNotFoundError**: When the Excel file doesn't exist
- **ValueError**: When the file is not in .xlsx format or invalid input types
- **Processing Errors**: Detailed error messages for Excel parsing issues

## Component Specifications

The module includes built-in specifications for common bicycle components:

### Brake Types
- **R (Rim)**: 2-year warranty, standard operating temperature
- **D (Disc)**: 5-year warranty, extended operating temperature range

### Wheel Sizes
- **26"**: Recommended for riders 168-174 cm
- **27"**: Recommended for riders 174-180 cm  
- **29"**: Recommended for riders 180-186 cm

### Groupsets
Supports both Shimano (SH1-SH4) and SRAM (SR1-SR2) groupsets with varying gear counts

### Suspension Options
- **- (None)**: No suspension
- **C (Cross-country)**: 80mm travel
- **A (All-mountain)**: 120mm travel

### Colors
17 different color options (01-17) with various frame colors and logo configurations

## Example Workflow

1. **Prepare Excel file** with component specifications
2. **Import the module** in your Python script
3. **Call generate_bicycles()** with the Excel file path
4. **Process the JSON output** for your specific needs (database insertion, web display, etc.)

```python
# Complete example
import bicycle_generator
import json

try:
    # Generate all bicycle configurations
    result = bicycle_generator.generate_bicycles("bike_specs.xlsx")
    
    # Parse and analyze results
    bikes = json.loads(result)
    
    print(f"Successfully generated {len(bikes)} bicycle configurations")
    
    # Group by brake type
    rim_bikes = [b for b in bikes if b.get('Brake type') == 'Rim']
    disc_bikes = [b for b in bikes if b.get('Brake type') == 'Disc']
    
    print(f"Rim brake models: {len(rim_bikes)}")
    print(f"Disc brake models: {len(disc_bikes)}")
    
except Exception as e:
    print(f"Error generating bicycles: {e}")
```


## Contributing

When contributing to this module, ensure that:
1. All tests pass
2. New features include appropriate test coverage
3. The string input/output interface is maintained
4. Error handling is comprehensive
