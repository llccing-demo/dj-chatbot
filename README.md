
## Install Dependences
pip install -r requirements.txt

**Python version**
`python --version`

Python 3.10.12

## Run project
python manage.py runserver 0.0.0.0:8080

## Test API

`curl -i "http://localhost:8080/answer/?question=how%20to%20check%20group%20status%20in%20icluster%20web"`

Question:
```
how to check group status in icluster web
```
Examples result
```
{
answer: "To check the group status in iCluster, you can use the Full Cluster Status Monitor. This monitor lists all the groups in the cluster and provides their status.
If you need further details, you can view and activate out-of-sync and suspended objects, work with iCluster jobs, start sync checks, and view node details using the iCluster web interface."
}
```
