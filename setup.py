from setuptools import find_packages, setup
from typing import List

dot_e = "-e ."

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n", "")for req in requirements]

        if dot_e in requirements:
            requirements.remove(dot_e)

        return requirements

setup(
    name="stockml",
    version="0.0.1",
    author="Duncan",
    author_email="otienoduncan99@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)