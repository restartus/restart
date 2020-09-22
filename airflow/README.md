# Airflow pulls

### To create and develop Airflow applications here are the steps:

- Copy the [airflow-template](airflow-template) directory to a new name with

    ```
    cp -r airflow.template/ _yournewproject_
    ```

- Jump into that project

    ```
    cd _yournewproject_
    make airflow-install
    ```

- This will create everything you need and you can create your dags in the `dags`
folder.

- Then, to run the system, open two terminal windows and cd to your desired airflow project dir.
    Start a pipenv in both windows:

    ```
    pipenv shell
    ```

    In one of your terminal windows, run the scheduler:
    ```
    make scheduler
    ```

    In the other terminal window, run the webserver:

    ```
    make airflow
    ```
- This should, by default, allow the Airflow Dashboard to be availabe on 'localhost:8080'

- When shutting down your airflow application, ensure to control-C to close both the
server and scheduler properly. If you do not, this will cause problems next time you
attempt to run the airflow webserver.

    If you unknowingly left port 8080 open, you will see a series of errors outputted in
    the window you start your webserver in.
    In this case, you'll want to shut down the server via control-C and find out which
    processes are occupying the port:

    ```
    sudo lsof -i :8080
    ```

    Then, for the `PID` from the last time you started the webserver, do:

    ```
    sudo kill -9 PID
    ```
    This will shut down the previous one. Now you should be able to get everything up and
    running properly again.

- If things get messy and you want a fresh environment, from inside your airflow/proj dir,

    ```
    pipenv shell
    make airflow-clean
    make airflow-install
    ```
