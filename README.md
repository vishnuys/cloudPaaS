# cloudPaaS
### PaaS for real-time analytics of stream data.
This PaaS supports creation of piplines for common operations like max, min, avg and supports storage of intermediate results. User can run these operations in any order to create a pipeline.

#### Requirements:
- Python 3
- rabbitMQ

#### Installation:
1) Clone the repo in each node of your cluster.
2) Create a virtualenv `cloudpaas` and activate it. If you do not have virtualenv installed, install it. (Installation: [Windows](https://thinkdiff.net/python/how-to-install-python-virtualenv-in-windows/), [Linux & MAC OS](https://medium.com/@garimajdamani/https-medium-com-garimajdamani-installing-virtualenv-on-ubuntu-16-04-108c366e4430))
3) To start job_manager on worker nodes run `rabbitstream/job_manager.py job_queue`.
4) Execute the following command to apply migrations: `python manage.py migrate`.
5) To run the server on local IP assigned with default port, execute the command `python manage.py runserver 0:8000`. 

#### Usage:
Visit `http://{your IP address}:8000` and register your account. You can now login and use the application.

###### Client functionality 
- **Add Job:** 
        - *NOTE*: This service only supports CSV file format with field names on the first row. 
- **See Result:** 
        - Shows the most recent result. you can download the intermediate results file from here.

###### Admin functionality 
- **View Users:** 
        - View all users who have logged in.
- **View Pipelines:** 
        - Shows the Jobs and pipelines by each user
- **View Pricing:** 
        - Shows pricing details for each user