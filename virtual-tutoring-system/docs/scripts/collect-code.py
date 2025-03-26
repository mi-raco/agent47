import os

def read_files_in_folder(folder_path):
    result = {}

    for root, _, files in os.walk(folder_path):
        print(root, files)
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                result[relative_path] = f.read()

    return result

# Example usage:
folder_path = './server'  # Replace with your folder path
files_object = read_files_in_folder(folder_path)
output_file = './docs/file-content-server.txt'  # Replace with your desired output file path
with open(output_file, 'w', encoding='utf-8') as f:
  for file_path, content in files_object.items():
    f.write('---\n')
    f.write(f'File: {file_path}\n')
    f.write('---\n')
    f.write(content)
    f.write('---\n')
    f.write('\n\n')