import unittest
import tempfile
from ruamel.yaml import YAML
from flux import Flux
from lib.path_reader import find_cartridge, read_yaml_cartridge, read_python_cartridge
import os

class TestIngest(unittest.TestCase):
    def test_can_read_yaml_file(self):
        try:
          flux = Flux()
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
            yaml = YAML(typ="safe", pure=True)
            yaml_data = {'a': [1, 2]}
            yaml.dump(yaml_data, temp_file)

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
            os.rename(temp_file.name, new_file_path)

            found_contents = read_yaml_cartridge(new_file_path)
            self.assertEqual(found_contents, yaml_data)

        finally:
          os.remove(new_file_path)

    def test_automatically_reads_yaml_file(self):
        try:
          flux = Flux()
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
            yaml = YAML(typ="safe", pure=True)
            yaml_data = {'a': [1, 2]}
            yaml.dump(yaml_data, temp_file)

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
            os.rename(temp_file.name, new_file_path)

            found_contents = find_cartridge()
            self.assertEqual(found_contents, yaml_data)

        finally:
          os.remove(new_file_path)

    def test_sees_python_file(self):
        try:
          flux = Flux()
          # Create a temporary python file called cartridge.py
          with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            # Add some contents to temp_file
            file_contents = b"cartridge = 'foo'"
            temp_file.write(file_contents)
            temp_file.close()

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.py
            new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.py")
            os.rename(temp_file.name, new_file_path)

            found_cartridge = find_cartridge()
            self.assertEqual(found_cartridge, 'foo')

        finally:
          os.remove(new_file_path)

    def test_prefers_yaml_file_over_python_file_if_both_exist(self):
        try:
          flux = Flux()
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
            yaml = YAML(typ="safe", pure=True)
            yaml_data = {'a': [1, 2]}
            yaml.dump(yaml_data, temp_file)

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path_yaml = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
            os.rename(temp_file.name, new_file_path_yaml)

          with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            # Add some contents to temp_file
            file_contents = b"cartridge = 'foo'"
            temp_file.write(file_contents)
            temp_file.close()

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.py")
            os.rename(temp_file.name, new_file_path)

            found_cartridge = find_cartridge()
            self.assertEqual(found_cartridge, yaml_data)


        finally:
          os.remove(new_file_path_yaml)
          os.remove(new_file_path)

    def test_reads_yaml_file_at_specific_path(self):
        try:
          flux = Flux()
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
            weird_name = "blartridge.yaml"
            yaml = YAML(typ="safe", pure=True)
            yaml_data = {'a': [1, 2]}
            yaml.dump(yaml_data, temp_file)

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), weird_name)
            os.rename(temp_file.name, new_file_path)

            found_contents = read_yaml_cartridge(weird_name)
            self.assertEqual(found_contents, yaml_data)

        finally:
          os.remove(new_file_path)

    def test_reads_python_file_at_specific_path(self):
        try:
          flux = Flux()
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            # Add some contents to temp_file
            weird_name = "blartridge.py"
            file_contents = b"cartridge = 'foo'"
            temp_file.write(file_contents)
            temp_file.close()

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), weird_name)
            os.rename(temp_file.name, new_file_path)

            found_cartridge = find_cartridge(weird_name)
            self.assertEqual(found_cartridge, 'foo')

        finally:
          os.remove(new_file_path)

    def test_assumes_yaml_file_at_specific_path(self):
        # If no extension is provided, flux assumes it's .py
        try:
          flux = Flux()
          weird_name = "blartridge"
          # Create a temporary yaml file called cartridge.yaml
          with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
            yaml = YAML(typ="safe", pure=True)
            yaml_data = {'a': [1, 2]}
            yaml.dump(yaml_data, temp_file)

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path_yaml = os.path.join(os.path.dirname(__file__), "%s.yaml"%weird_name)
            os.rename(temp_file.name, new_file_path_yaml)

          with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            # Add some contents to temp_file
            file_contents = b"cartridge = 'foo'"
            temp_file.write(file_contents)
            temp_file.close()

            self.assertTrue(os.path.exists(temp_file.name))

            # Move the temporary file to the current directory and rename to cartridge.yaml
            new_file_path = os.path.join(os.path.dirname(__file__), "%s.py"%weird_name)
            os.rename(temp_file.name, new_file_path)

            found_cartridge = find_cartridge(weird_name)
            self.assertEqual(found_cartridge, yaml_data)

        finally:
          os.remove(new_file_path_yaml)
          os.remove(new_file_path)

class TestDataStore(unittest.TestCase):
  def test_can_read_initial_data(self):
      self.assertTrue(True)

class TestAdvancedFunctions(unittest.TestCase):
  def test_data_is_manipulated_with_before_function(self):
    flux = Flux()

    def change_data(data):
      data["foo"] = "fizz"
      return data

    data = {
      'START': {
        'role': '',
        'prompt': '',
        'events': [ 

        ]
        'data': { "foo": "bar" }
      },
      'DOTHING': {
        'prompt': '',
        'events': [],
        'before': change_data
      }
    }

    # TODO
    cartridge = None
    state = None
    method = None

    flux.call_method_on_state(cartridge, state, method)

    self.assertTrue(False)