import os
import subprocess

# check conda environment exists
def verify_conda_env(env_name):
  """Verifies the environment exists."""
  env_list = subprocess.check_output('conda env list', shell=True)
  if env_name in env_list.decode().split():
    return True

def get_conda_package_list(env_name):
  """Gets the list of packages installed in the specified conda environment."""
  cmd = ["conda", "list", "--explicit", '--name ' + env_name]
  output = subprocess.check_output(cmd).decode("utf-8")
  return output.splitlines()

def get_requirements_file_list(requirements_file_path):
  """Gets the list of packages in the specified requirements file."""
  with open(requirements_file_path, "r") as f:
    lines = f.readlines()
  return [line.strip() for line in lines]

def compare_package_lists(conda_list, requirements_list):
  """Compares two lists of packages and returns a dictionary of differences."""
  differences = {}
  for package in conda_list:
    if package not in requirements_list:
      differences[package] = "conda"
  for package in requirements_list:
    if package not in conda_list:
      differences[package] = "requirements"
  return differences

def move_to_script_dir():
  """Get current directory and the directory where the script is located, and move to script directory if not currently there."""
  # Get the current working directory.
  current_working_directory = os.getcwd()
  print('current working directory: {}'.format(current_working_directory))

  # Get the directory where the script is located.
  script_directory = os.path.dirname(os.path.abspath(__file__))
  print('script directory: {}'.format(script_directory))

  # Compare the two directories.
  if current_working_directory != script_directory:
    # Change the current working directory to the directory where the script is located.
    os.chdir(script_directory)
    current_working_directory = os.getcwd()
    print('new current working directory:{}'.format(current_working_directory))
  
def build_conda_environment(requirements_file_path, env_name):
  """Build conda environment based off requirements file"""
  # Install conda ml environment with requirements.txt packages
  cmd = 'conda create -y --name ' + env_name + ' --file ' + requirements_file_path 
  os.system(cmd)
  
def install_conda_requirements(requirements_file_path, env_name):
  """Install conda packages to environment based off requirements file"""
  cmd = 'conda install -y --name ' + env_name + ' --file ' + requirements_file_path
  os.system(cmd)  

if __name__ == "__main__":

  # set env_name and file path
  env_name = 'ml'
  requirements_file_path = 'requirements.txt'

  # Move to script directory
  move_to_script_dir()
  
  # verify if conda environment exists
  if verify_conda_env(env_name=env_name):
    
    # Get the list of packages installed in the conda environment and the list of packages in the requirements file.
    conda_list = get_conda_package_list(env_name)
    requirements_list = get_requirements_file_list(requirements_file_path)
    
    # Used for debugging only   
    #print(type(conda_list))
    #print(type(requirements_list))
    #print("Conda list: {}".format(conda_list))
    #print("Requirements list: {}".format(requirements_list))
    #print('{} is in the environment list'.format(env_name))

    # Compare the two lists of packages and print the differences.
    differences = compare_package_lists(conda_list, requirements_list)
    if differences:
      print("The following packages are different between the conda environment and the requirements file:")
      for package, source in differences.items():
        print(f"{package} ({source})")
      install_conda_requirements(requirements_file_path=requirements_file_path, env_name=env_name)
    else:
      print("The conda environment ({}) packages and the requirements file are identical.".format(env_name))
  else: 
    print("The conda environment ({}) does not exist and will be created.".format(env_name))
    # If the environment doesn't exist at all, build environment
    build_conda_environment(requirements_file_path=requirements_file_path, env_name=env_name)
