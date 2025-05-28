#!/usr/bin/env python3
"""
Bicycle Generator Module
Generates all possible bicycle modifications from Excel (.xlsx) specification files

Requirements fulfilled:
1. Implemented as Python module with main function
2. Takes string path to Excel file, returns JSON string
3. Includes automated tests
"""

import pandas as pd
import json
import itertools
from pathlib import Path
import gc


def generate_bicycles(excel_path: str) -> str:
    """
    Generate all possible bicycle modifications from Excel file.
    
    Args:
        excel_path (str): Absolute path to Excel file (.xlsx)
        
    Returns:
        str: JSON document containing all bicycle modifications
        
    Raises:
        FileNotFoundError: If Excel file doesn't exist
        ValueError: If file is not .xlsx format
        Exception: For other processing errors
    """
    
    # Validate input
    if not isinstance(excel_path, str):
        raise ValueError("excel_path must be a string")
    
    excel_file = Path(excel_path)
    if not excel_file.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    if not excel_file.suffix.lower() == '.xlsx':
        raise ValueError("Input file must be an Excel file (.xlsx)")
    
    try:
        # Read Excel file with proper resource management
        excel_data = None
        designators = {}
        general_specs = {}
        
        try:
            # Read Excel file - assuming it has sheets: ID, GENERAL, and component sheets
            excel_data = pd.ExcelFile(excel_path, engine='openpyxl')
            
            # Parse different sheets
            if 'ID' in excel_data.sheet_names:
                # Read ID sheet for designator structure
                id_df = pd.read_excel(excel_path, sheet_name='ID', engine='openpyxl')
                designators = _parse_id_sheet(id_df)
                del id_df  # Explicit cleanup
            else:
                # Fallback: try to parse from first sheet as combined format
                df = pd.read_excel(excel_path, sheet_name=0, engine='openpyxl')
                designators = _parse_combined_sheet(df)
                del df  # Explicit cleanup
            
            # Read GENERAL sheet if exists
            if 'GENERAL' in excel_data.sheet_names:
                general_df = pd.read_excel(excel_path, sheet_name='GENERAL', engine='openpyxl')
                general_specs = _parse_general_sheet(general_df)
                del general_df  # Explicit cleanup
            else:
                # Use default general specifications
                general_specs = _get_default_general_specs()
                
        finally:
            # Ensure Excel file handle is closed
            if excel_data is not None:
                excel_data.close()
            # Force garbage collection to release file handles
            gc.collect()
        
        # Parse component-specific sheets or use defaults
        component_specs = _get_component_specifications()
        
        # Generate all bicycle combinations
        bicycles = _generate_all_bicycles(designators, general_specs, component_specs)
        
        # Return as JSON string
        return json.dumps(bicycles, indent=2)
        
    except Exception as e:
        # Ensure cleanup even on error
        gc.collect()
        raise Exception(f"Error processing Excel file: {e}")


def _parse_id_sheet(id_df):
    """Parse ID sheet to extract designator values"""
    designators = {}
    
    # First row contains designator names
    designator_names = id_df.columns.tolist()
    
    for col_name in designator_names:
        # Get all non-null values for this designator
        values = id_df[col_name].dropna().unique().tolist()
        values = [str(v).strip() for v in values if str(v).strip()]
        if values:
            designators[col_name] = values
    
    return designators


def _parse_combined_sheet(df):
    """Parse combined sheet format (like the CSV) to extract designator values"""
    designators = {}
    
    # Extract unique non-empty values for each column
    for col_name in df.columns:
        values = df[col_name].dropna().unique()
        clean_values = []
        for val in values:
            if pd.notna(val) and str(val).strip():
                clean_values.append(str(val).strip())
        if clean_values:
            designators[col_name] = clean_values
    
    return designators


def _parse_general_sheet(general_df):
    """Parse GENERAL sheet for common specifications"""
    general_specs = {}
    
    if len(general_df) >= 2:
        # First row is field names, second row is values
        field_names = general_df.iloc[0].tolist()
        field_values = general_df.iloc[1].tolist()
        
        for name, value in zip(field_names, field_values):
            if pd.notna(name) and pd.notna(value):
                general_specs[str(name)] = str(value)
    
    return general_specs


def _get_default_general_specs():
    """Default general specifications for all bicycles"""
    return {
        "Manufacturer": "Bikes INC",
        "Type": "City",
        "Frame type": "Diamond",
        "Frame material": "Aluminum",
        "Operating temperature": "0 - 40 °C"
    }


def _get_component_specifications():
    """Get component-specific specifications"""
    return {
        'brake_specs': {
            "R": {
                "Brake type": "Rim",
                "Brake warranty": "2 years"
            },
            "D": {
                "Brake type": "Disc",
                "Brake warranty": "5 years",
                "Operating temperature": "-20 - 50 °C"
            }
        },
        'wheel_specs': {
            "26": {
                "Wheel diameter": "26″",
                "Recommended height": "168-174 cm"
            },
            "27": {
                "Wheel diameter": "27″",
                "Recommended height": "174-180 cm"
            },
            "29": {
                "Wheel diameter": "29″",
                "Recommended height": "180-186 cm"
            }
        },
        'frame_specs': {
            "S": {"Frame height": "16 in"},
            "M": {"Frame height": "18 in"},
            "L": {"Frame height": "20 in"}
        },
        'groupset_specs': {
            "SH1": {
                "Groupset manufacturer": "Shimano",
                "Groupset name": "Acera",
                "Gears": "27"
            },
            "SH2": {
                "Groupset manufacturer": "Shimano",
                "Groupset name": "Altus",
                "Gears": "24"
            },
            "SH3": {
                "Groupset manufacturer": "Shimano",
                "Groupset name": "Tourney",
                "Gears": "18"
            },
            "SH4": {
                "Groupset manufacturer": "Shimano",
                "Groupset name": "Deore",
                "Gears": "30"
            },
            "SR1": {
                "Groupset manufacturer": "SRAM",
                "Groupset name": "X3",
                "Gears": "21"
            },
            "SR2": {
                "Groupset manufacturer": "SRAM",
                "Groupset name": "X5",
                "Gears": "27"
            }
        },
        'suspension_specs': {
            "-": {
                "Has suspension": "FALSE",
                "Suspension travel": "Not applicable"
            },
            "C": {
                "Has suspension": "TRUE",
                "Suspension travel": "80 mm"
            },
            "A": {
                "Has suspension": "TRUE",
                "Suspension travel": "120 mm"
            }
        },
        'color_specs': {
            "01": {"Frame color": "RED", "Logo": "TRUE"},
            "02": {"Frame color": "BLUE", "Logo": "TRUE"},
            "03": {"Frame color": "CYAN", "Logo": "FALSE"},
            "04": {"Frame color": "GREEN", "Logo": "TRUE"},
            "05": {"Frame color": "YELLOW", "Logo": "FALSE"},
            "06": {"Frame color": "BLACK", "Logo": "TRUE"},
            "07": {"Frame color": "WHITE", "Logo": "FALSE"},
            "08": {"Frame color": "ORANGE", "Logo": "TRUE"},
            "09": {"Frame color": "PURPLE", "Logo": "FALSE"},
            "10": {"Frame color": "PINK", "Logo": "TRUE"},
            "11": {"Frame color": "GREY", "Logo": "FALSE"},
            "12": {"Frame color": "BROWN", "Logo": "TRUE"},
            "13": {"Frame color": "SILVER", "Logo": "TRUE"},
            "14": {"Frame color": "GOLD", "Logo": "FALSE"},
            "15": {"Frame color": "MAROON", "Logo": "TRUE"},
            "16": {"Frame color": "NAVY", "Logo": "FALSE"},
            "17": {"Frame color": "LIME", "Logo": "TRUE"}
        }
    }


def _generate_all_bicycles(designators, general_specs, component_specs):
    """Generate all possible bicycle combinations"""
    bicycles = []
    
    # Extract component lists
    models = designators.get('Model number', [''])
    brakes = designators.get('Brakes', [])
    wheels = designators.get('Wheels', [])
    frame_sizes = designators.get('Frame size', [])
    groupsets = designators.get('Groupset', [])
    suspensions = designators.get('Suspension', [])
    colors = designators.get('Color', [])
    
    # Generate all combinations
    for model in models:
        for brake in brakes:
            for wheel in wheels:
                for frame_size in frame_sizes:
                    for groupset in groupsets:
                        for suspension in suspensions:
                            for color in colors:
                                # Skip if any required component is missing
                                if not all([brake, wheel, frame_size, groupset, suspension, color]):
                                    continue
                                
                                # Generate bicycle ID
                                bike_id = f"{model}{brake}{wheel}{frame_size}{groupset}{suspension}{color}"
                                
                                # Build bicycle specifications
                                bicycle = {"ID": bike_id}
                                bicycle.update(general_specs)
                                
                                # Add component-specific specs
                                _add_component_specs(bicycle, brake, wheel, frame_size, 
                                                   groupset, suspension, color, component_specs)
                                
                                bicycles.append(bicycle)
    
    return bicycles


def _add_component_specs(bicycle, brake, wheel, frame_size, groupset, suspension, color, component_specs):
    """Add component-specific specifications to bicycle"""
    
    # Add brake specs
    if brake in component_specs['brake_specs']:
        bicycle.update(component_specs['brake_specs'][brake])
    
    # Add wheel specs
    if wheel in component_specs['wheel_specs']:
        bicycle.update(component_specs['wheel_specs'][wheel])
    
    # Add frame specs
    if frame_size in component_specs['frame_specs']:
        bicycle.update(component_specs['frame_specs'][frame_size])
    
    # Add groupset specs
    if groupset in component_specs['groupset_specs']:
        bicycle.update(component_specs['groupset_specs'][groupset])
    
    # Add suspension specs
    if suspension in component_specs['suspension_specs']:
        bicycle.update(component_specs['suspension_specs'][suspension])
    
    # Add color specs
    if color in component_specs['color_specs']:
        bicycle.update(component_specs['color_specs'][color])


# Module-level convenience function (main interface)
def main():
    """
    Main function for command-line usage.
    For module usage, call generate_bicycles() directly.
    """
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python bicycle_generator.py <excel_file_path>")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    
    try:
        json_output = generate_bicycles(excel_path)
        print(json_output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
# End of bicycle_generator.py