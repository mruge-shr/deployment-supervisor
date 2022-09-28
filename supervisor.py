import kubernetes
import kopf
import yaml 
import logging

@kopf.on.create('batch', 'v1', 'Job')
def job_created(body, **kwargs):
    logging.info(f"A Job was created!")


@kopf.on.field('batch', 'v1', 'jobs', field='status')
def job_changed(old, new, **kwargs):
    print(f'FIELD CHANGED: {old} -> {new}')