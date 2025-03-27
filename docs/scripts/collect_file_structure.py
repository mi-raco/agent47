import os

def get_file_structure(folder_path):
  file_structure = []

  for root, _, files in os.walk(folder_path):
    for file in files:
      file_path = os.path.join(root, file)
      relative_path = os.path.relpath(file_path, folder_path)
      file_structure.append(relative_path)

  return file_structure

# Example usage:
folder_path = './server'  # Replace with your folder path
file_structure = get_file_structure(folder_path)
output_file = './docs/file-structure-server.txt'  # Replace with your desired output file path
with open(output_file, 'w', encoding='utf-8') as f:
  for file_path in file_structure:
    f.write(f'{file_path}\n')
