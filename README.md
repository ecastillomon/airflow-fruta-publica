# Airflow Fruta Publica

## Install
Install through dockerfile is not working on RPi, could be setup but doesn't work with default docker repository for ARMv7 architecture.

Clone the repository in your device (RPi) using:
`git clone git@github.com:ecastillomon/airflow-fruta-publica.git`
This will copy the repository and contains resources for your Airflow setup. Go to your new directory using:
`cd ~/airflow-fruta-publica`
then create a python venv with
`python3 -m venv venv`
This will install Airflow in your RPi.


## First Setup 
Modify the file `~/airflow/airflow.cfg`  in your RPi to change any behaviour behind Airflow. You should at least modify the line:
`dags_folder = /home/leonarda/airflow-fruta-publica/dags` with the correct path of the `airflow-fruta-publica` folder. In this case the RPis user's home is `leonarda`. 

(Optional) You can also modify `web_server_port` with the number of the port you want airflow to be displayed. This will be part of the url of your home airflow installlation, ex:  if you set `web_server_port` port to 8181, airflow will be found in your home network at`http://192.168.1.69:8181/home`  

Modify the file `airflow-fruta-publica/entrypoint.sh` to include your device location for airflow's virtual environment you created a few steps back.

Create at least one user for Airflow with:
`airflow users create --username admin --firstname Peter --lastname Parker  --role Admin --email spiderman@superhero.org`

You can test everything is working by running 
`./entrypoint.sh` on the terminal and airflow will start on your device if everything is working. If installing with docker, entrypoint.sh should be modified accordingly with commands to start all airflow services.

Modify the crontab in your device using in your RPi terminal: `contab -e` 
Add this line with the location of your entrypoint.sh file:
`@reboot /home/leonarda/airflow-fruta-publica/entrypoint.sh`



