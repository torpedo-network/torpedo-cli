"creates a vast ai instance given an id"
# XMTP
# FINISH SPAWNER
# WEB3 STORAGE

from vast_utils import *
import os
import json
import time
#service type, gpu type, number of gpus, number of cpus,{ ram, persistence storage,} total time



def create_vast():
    output = os.popen("./vast search offers 'reliability > 0.99 num_gpus=1 gpu_name=RTX_3090' -o 'flops_usd-' --raw").read()
    y = json.loads(output)
    id = y[1]['id']
    print(y[1])
    payload = os.popen("./vast create instance " + str(id) + " --jupyter-lab --image pytorch/pytorch --disk 32").read()
    instances = os.popen("./vast show instances").read()
    print("instances")
    print(instances)
    #time.sleep(1000)
    #os.popen("./vast destroy instance " + str(id))

def vast_spawner():
    payload = 'https://jupyter.vast.ai/jm/4/31972/?token=bb34dca17a01cbdedc06baa4d373e51db6b5e11c7470c03b3ec28721203ef9ac'
    return payload

def create_gcloud():
    #create gcloud vm instancve
    return
    
    
def gcloud_spawner():
    return 'https://5d516aeb21e48632-dot-us-west1.notebooks.googleusercontent.com/lab/workspaces/auto-V'


def clean_up():
    return



