from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements()->List[str]:
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and not requirement.startswith(HYPHEN_E_DOT):
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print('Requirements.txt not found!!!')
    
    return requirement_list
                    

setup(
    name = 'Course-Recommender-System',
    version = '0.0.1',
    author = 'Subrat Mishra',
    author_email='3subratmishra1sep@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements()
)