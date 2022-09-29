import kubernetes
import kopf
import yaml 
import logging

@kopf.on.create('batch', 'v1', 'Job')
def job_created(body, **kwargs):
    logging.info(f"A Job was created!")


@kopf.on.field('batch', 'v1', 'jobs', field='status')
def job_changed(body, namespace, **kwargs):
    job_id = body.metadata.uid
    job_name = body.metadata.name
    client = kubernetes.client
    corev1 = client.CoreV1Api()
    pod_list = corev1.list_namespaced_pod(namespace)
    for pod in pod_list.items:
        meta = pod.metadata
        name = meta.name
        owners = [owner.uid for owner in meta.owner_references]
        if job_id in owners:
            logs = corev1.read_namespaced_pod_log(name=name, namespace=namespace)
            exists = [cm for cm in corev1.list_namespaced_config_map( namespace=namespace).items if cm.metadata.name==f"{job_name}"]
            print(exists)
            configmap = client.V1ConfigMap(
                api_version="v1", kind="ConfigMap", 
                data={f"{name}": logs}, 
                metadata=client.V1ObjectMeta(name=f"{job_name}", namespace=namespace)
            )
            if not exists:
                corev1.create_namespaced_config_map(
                    namespace=namespace, body=configmap, pretty='True',
                )
            else:
                corev1.replace_namespaced_config_map(
                    name=f"{job_name}", namespace=namespace, body=configmap, pretty='True',
                )
        else:
            print("Not one of mine")
        # print("%s\t%s\t%s" % (pod.metadata.name,
        #                       pod.status.phase,
        #                       pod.status.pod_ip))
