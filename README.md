# MC906A/MO416A - Introducition to Artificial Intelligence
## Institute of Computing - Unicamp

## Project 2 for MC906 disciplin

### Authors

- Matteus Vargas (ra: 262885)
- Christian Maekawa (ra: 231867)
- Stéfani Fernandes (ra: 147939)
- Maisa Silva (ra: 181831)
- Giovane de Morais (ra: 192683)


# Requisites
## Download Git

* Download and install Git [link](https://git-scm.com/).

## Clone repository
`````
git https://github.com/MatteusStranger/genetic_algorithm_mc906.git
`````



You can run this project using Anaconda or Docker

---

# How to run
## Install Conda (Summarized)

* Download and install Conda using this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#installing-conda-on-a-system-that-has-other-python-installations-or-packages)

* Open ananconda shell and go to project path

* Run jupyter

###  Some recommendation before run jupyter

#### Create an environment
`````powershell
conda create -y --name mo416_project2 python==3.7.7 
`````

#### Activate environment
`````powershell
conda activate mo416_project2
`````

#### Install requirements
`````powershell
pip install -r requirements.txt
`````

#### Run using python
`````powershell
python main.py
`````

#### Open using jupyter notebook

`````powershell
jupyter notebook
`````
Remember: Go to project path before run this command on your Anaconda Terminal


#### Uninstall environment
`````powershell
conda activate base
conda remove --name mo416_project2 --all
`````

---

## Install Docker

  Download and install Docker using this [link](https://www.docker.com/products/docker-desktop)

#### Create a slim image with python shell

`````powershell
docker build -t "python_light" .
`````

#### Create container with custom bash with environment
Developement mode (If you modify in /app you will see modification on your project)
`````powershell
docker run --rm -it -p 8888:8888 -v "$(pwd):/app" python_light
`````

Deploy mode (If you modify inside /app you won't see modification on your project)
`````powershell
docker run --rm -it -p 8888:8888  python_light
`````

#### Inside container to run jupyter-lab 

`````bash
root@hash:/app# ./jupyter-lab.sh
`````

#### Uninstall container and image 
`````powershell
docker rmi python_light
`````

<img src="https://media.githubusercontent.com/media/MatteusStranger/genetic_algorithm_mc906/assets/assets/gif/example.gif" width="800" height="400"/>