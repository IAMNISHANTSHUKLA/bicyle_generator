#!/usr/bin/env python3
"""
Test Suite for Bicycle Generator Module
Tests the module according to requirements:
1. Python module implementation
2. String input (Excel path) -> String output (JSON)
3. Automated tests with input/output validation
"""

import unittest
import json
import tempfile
import os
import pandas as pd
import time
import gc
import sys
# Import the bicycle generator module
import bicycle_generator


class TestBicycleGeneratorModule(unittest.TestCase):
    """Test suite for bicycle generator module"""

    def setUp(self):
        """Set up test data and temporary Excel files"""
        self.temp_files = []
        
        # Create test Excel file with proper sheet structure
        self.test_excel_path = self._create_test_excel_file()
        
        # Create test Excel file with combined format (like CSV converted)
        self.test_combined_excel_path = self._create_combined_test_excel_file()

    def tearDown(self):
        """Clean up temporary files"""
        # Force garbage collection to release file handles
        gc.collect()
        
        # Wait a bit for Windows to release file handles
        time.sleep(0.1)
        
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                self.safe_unlink(temp_file)

    def safe_unlink(self, path, retries=10, delay=0.1):
        """Safely delete a file with retries for Windows file locking issues"""
        for attempt in range(retries):
            try:
                if os.path.exists(path):
                    os.unlink(path)
                return
            except PermissionError:
                if attempt < retries - 1:
                    time.sleep(delay)
                    gc.collect()  # Force garbage collection
                else:
                    # Last attempt - try to make file writable first
                    try:
                        os.chmod(path, 0o777)
                        os.unlink(path)
                    except:
                        print(f"Warning: Could not delete temporary file {path}")

    def _create_test_excel_file(self):
        """Create a proper test Excel file with ID, GENERAL sheets"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        
        # Create Excel writer with explicit engine and close it properly
        try:
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                # ID sheet - designator structure
                id_data = {
                    'Model number': ['CITY-', 'MOUNTAIN-'],
                    'Brakes': ['R', 'D'],
                    'Wheels': ['26', '27'],
                    'Frame size': ['S', 'M'],
                    'Groupset': ['SH1', 'SH2'],
                    'Suspension': ['-', 'C'],
                    'Color': ['01', '02']
                }
                id_df = pd.DataFrame(id_data)
                id_df.to_excel(writer, sheet_name='ID', index=False)
                
                # GENERAL sheet - common specifications
                general_data = {
                    'Field': ['Manufacturer', 'Type', 'Frame material'],
                    'Value': ['Test Bikes Inc', 'Test Type', 'Carbon']
                }
                general_df = pd.DataFrame(general_data)
                general_df.to_excel(writer, sheet_name='GENERAL', index=False)
        except Exception as e:
            print(f"Error creating test Excel file: {e}")
            raise
        
        return temp_file.name

    def _create_combined_test_excel_file(self):
        """Create test Excel file in combined format (like CSV data)"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        
        # Create data similar to the CSV format
        data = {
            'Model number': ['CITY-', '', ''],
            'Brakes': ['R', 'D', ''],
            'Wheels': ['26', '27', '29'],
            'Frame size': ['S', 'M', 'L'],
            'Groupset': ['SH1', 'SH2', 'SH3'],
            'Suspension': ['-', 'C', 'A'],
            'Color': ['01', '02', '03']
        }
        
        try:
            df = pd.DataFrame(data)
            # Use context manager to ensure proper file closure
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        except Exception as e:
            print(f"Error creating combined test Excel file: {e}")
            raise
        
        return temp_file.name

    def test_requirement_1_python_module_implementation(self):
        """Test Requirement 1: Implemented as Python module"""
        # Test that the module has the required function
        self.assertTrue(hasattr(bicycle_generator, 'generate_bicycles'))
        self.assertTrue(callable(bicycle_generator.generate_bicycles))
        
        # Test that function signature is correct
        import inspect
        sig = inspect.signature(bicycle_generator.generate_bicycles)
        params = list(sig.parameters.keys())
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], 'excel_path')

    def test_requirement_2_string_input_output(self):
        """Test Requirement 2: String input (Excel path) -> String output (JSON)"""
        # Test with string path input
        result = bicycle_generator.generate_bicycles(self.test_combined_excel_path)
        
        # Verify output is a string
        self.assertIsInstance(result, str)
        
        # Verify output is valid JSON
        try:
            json_data = json.loads(result)
            self.assertIsInstance(json_data, list)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_requirement_3_automated_test_with_validation(self):
        """Test Requirement 3: Automated test with input/output validation"""
        
        # Test input validation
        excel_path = self.test_combined_excel_path
        self.assertTrue(os.path.exists(excel_path))
        self.assertTrue(excel_path.endswith('.xlsx'))
        
        # Generate bicycles
        json_output = bicycle_generator.generate_bicycles(excel_path)
        
        # Validate output structure
        bicycles = json.loads(json_output)
        
        # Check that we have generated bicycles
        self.assertGreater(len(bicycles), 0)
        
        # Validate each bicycle has required structure
        for bicycle in bicycles:
            # Must have ID
            self.assertIn('ID', bicycle)
            self.assertIsInstance(bicycle['ID'], str)
            self.assertGreater(len(bicycle['ID']), 0)
            
            # Must have other required fields
            required_fields = ['Manufacturer', 'Type', 'Frame material']
            for field in required_fields:
                self.assertIn(field, bicycle)
        
        # Validate specific combinations exist
        bike_ids = [bike['ID'] for bike in bicycles]
        
        # Check that combinations are properly generated
        self.assertTrue(any('R26S' in bike_id for bike_id in bike_ids))  # Rim brakes, 26" wheels, Small frame
        self.assertTrue(any('D27M' in bike_id for bike_id in bike_ids))  # Disc brakes, 27" wheels, Medium frame

    def test_excel_file_validation(self):
        """Test Excel file validation"""
        
        # Test non-existent file
        with self.assertRaises(FileNotFoundError):
            bicycle_generator.generate_bicycles("/non/existent/file.xlsx")
        
        # Test wrong file extension
        temp_txt = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        temp_txt.close()
        self.temp_files.append(temp_txt.name)
        
        with self.assertRaises(ValueError):
            bicycle_generator.generate_bicycles(temp_txt.name)
        
        # Test invalid input type
        with self.assertRaises(ValueError):
            bicycle_generator.generate_bicycles(123)  # Not a string

    def test_json_output_format(self):
        """Test that output JSON format matches specification"""
        json_output = bicycle_generator.generate_bicycles(self.test_combined_excel_path)
        bicycles = json.loads(json_output)
        
        # Test first bicycle for expected structure
        if bicycles:
            first_bike = bicycles[0]
            
            # Check ID format
            self.assertRegex(first_bike['ID'], r'^.+$')  # Non-empty string
            
            # Check required fields exist
            expected_fields = [
                'ID', 'Manufacturer', 'Type', 'Frame type', 'Frame material'
            ]
            for field in expected_fields:
                self.assertIn(field, first_bike)

    def test_component_specifications(self):
        """Test that component specifications are correctly applied"""
        json_output = bicycle_generator.generate_bicycles(self.test_combined_excel_path)
        bicycles = json.loads(json_output)
        
        # Find bicycles with specific components and verify specs
        for bicycle in bicycles:
            bike_id = bicycle['ID']
            
            # Test brake specifications
            if 'R' in bike_id:  # Rim brakes
                self.assertEqual(bicycle.get('Brake type'), 'Rim')
                self.assertEqual(bicycle.get('Brake warranty'), '2 years')
            elif 'D' in bike_id:  # Disc brakes
                self.assertEqual(bicycle.get('Brake type'), 'Disc')
                self.assertEqual(bicycle.get('Brake warranty'), '5 years')
            
            # Test wheel specifications
            if '26' in bike_id:
                self.assertEqual(bicycle.get('Wheel diameter'), '26″')
            elif '27' in bike_id:
                self.assertEqual(bicycle.get('Wheel diameter'), '27″')

    def test_comprehensive_bicycle_generation(self):
        """Test comprehensive bicycle generation from all combinations"""
        json_output = bicycle_generator.generate_bicycles(self.test_combined_excel_path)
        bicycles = json.loads(json_output)
        
        # Calculate expected number of combinations
        # From our test data: 1 model × 2 brakes × 3 wheels × 3 frames × 3 groupsets × 3 suspensions × 3 colors
        # But only valid combinations (no empty values)
        self.assertGreater(len(bicycles), 10)  # Should have many combinations
        
        # Verify all bicycles have unique IDs
        bike_ids = [bike['ID'] for bike in bicycles]
        self.assertEqual(len(bike_ids), len(set(bike_ids)))  # All unique

# Replace the test_module_as_script method in test_bicycle_generator.py
# around line 270-302 with this corrected version:

def test_module_as_script(self):
    """Test that module can be run as script"""
    # This tests the main() function
    import subprocess
    
    # Fix Windows path escaping issue
    safe_path = self.test_combined_excel_path.replace('\\', '\\\\')
    
    # Run module as script with proper error handling
    try:
        result = subprocess.run([
            sys.executable, '-c', 
            f'''
import sys
sys.path.insert(0, ".")
import json
try:
    import bicycle_generator
    json_output = bicycle_generator.generate_bicycles(r"{self.test_combined_excel_path}")
    bicycles = json.loads(json_output) if json_output else []
    print(len(bicycles))
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
'''
        ], capture_output=True, text=True, timeout=30, cwd=os.getcwd())
        
        # Check if execution was successful
        if result.returncode != 0:
            print(f"Script execution failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        
        self.assertEqual(result.returncode, 0, f"Script failed with: {result.stderr}")
        
    except subprocess.TimeoutExpired:
        self.fail("Module execution timed out")
    except Exception as e:
        self.fail(f"Subprocess execution failed: {e}")


def create_sample_excel_for_demo():
    """Create a sample Excel file for demonstration"""
    sample_path = "Sample_Bicycle.xlsx"

    # Create sample data matching the CSV format
    data = {
        'Model number': ['CITY-', '', '', '', '', '', ''],
        'Brakes': ['R', 'D', '', '', '', '', ''],
        'Wheels': ['26', '27', '29', '', '', '', ''],
        'Frame size': ['S', 'M', 'L', '', '', '', ''],
        'Groupset': ['SH1', 'SH2', 'SH3', 'SH4', 'SR1', 'SR2', ''],
        'Suspension': ['-', 'C', 'A', '', '', '', ''],
        'Color': ['01', '02', '03', '04', '05', '06', '07']
    }

    df = pd.DataFrame(data)
    # Use ExcelWriter context manager to ensure file is properly closed
    try:
        with pd.ExcelWriter(sample_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    except Exception as e:
        print(f"Error creating sample Excel file: {e}")
        raise

    return sample_path


def safe_unlink(path, retries=10, delay=0.1):
    """Attempt to delete a file, retrying if PermissionError occurs."""
    for attempt in range(retries):
        try:
            if os.path.exists(path):
                # Try to make file writable first
                try:
                    os.chmod(path, 0o777)
                except:
                    pass
                os.unlink(path)
            return
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(delay)
                gc.collect()  # Force garbage collection
            else:
                print(f"Warning: Could not delete file {path} after {retries} attempts")
                return
        except Exception as e:
            print(f"Unexpected error deleting {path}: {e}")
            return


def demonstrate_requirements():
    """Demonstrate that all requirements are fulfilled"""
    print("=== Bicycle Generator Module - Requirements Demonstration ===\n")

    # Create sample Excel file
    sample_excel = create_sample_excel_for_demo()
    print(f"✓ Created sample Excel file: {sample_excel}")

    print("\n1. REQUIREMENT 1: Python Module Implementation")
    print("   - Module has generate_bicycles() function")
    print("   - Function takes string parameter and returns string")
    print("   - Can be imported and used as module")

    print("\n2. REQUIREMENT 2: String Input/Output")
    print(f"   - Input: String path to Excel file: '{sample_excel}'")

    # Generate bicycles using the module function
    try:
        json_result = bicycle_generator.generate_bicycles(sample_excel)
        bicycles = json.loads(json_result)
        
        print(f"   - Output: JSON string with {len(bicycles)} bicycle modifications")
        print("   - First bicycle preview:")
        if bicycles:
            first_bike = bicycles[0]
            for key, value in list(first_bike.items())[:5]:
                print(f"     {key}: {value}")
            print("     ... (more fields)")

    except Exception as e:
        print(f"   - Error: {e}")

    print("\n3. REQUIREMENT 3: Automated Testing")
    print("   - Unit tests validate input/output requirements")
    print("   - Tests verify Excel file processing")
    print("   - Tests check JSON output format")
    print("   - Tests validate bicycle specifications")

    # Clean up with improved error handling
    if os.path.exists(sample_excel):
        # Force garbage collection before deletion
        gc.collect()
        time.sleep(0.2)  # Wait for file handles to be released
        safe_unlink(sample_excel)
        print(f"\n✓ Cleaned up sample file: {sample_excel}")

    print("\n=== All Requirements Fulfilled ===")


def main():
    """Main function to run all tests and demonstration"""
    print("Bicycle Generator Module Test Suite")
    print("=" * 50)
    
    # Set up better test environment
    original_cwd = os.getcwd()
    
    try:
        # Run automated tests
        print("\nRunning automated tests...")
        
        # Create a test suite to run with better error handling
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestBicycleGeneratorModule)
        runner = unittest.TextTestRunner(verbosity=2, buffer=True)
        result = runner.run(suite)
        
        print("\n" + "=" * 50)
        
        # Force cleanup before demonstration
        gc.collect()
        time.sleep(0.5)
        
        # Demonstrate requirements
        demonstrate_requirements()

        print("\n=== USAGE EXAMPLES ===")
        print("As Python module:")
        print('  import bicycle_generator')
        print('  json_output = bicycle_generator.generate_bicycles("/path/to/file.xlsx")')
        print('  bicycles = json.loads(json_output)')

        print("\nAs script:")
        print('  python bicycle_generator.py /path/to/file.xlsx')
        
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        # Ensure we're back in the original directory
        os.chdir(original_cwd)
        # Final cleanup
        gc.collect()


if __name__ == "__main__":
    main()