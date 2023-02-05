# DE2-Project
Project 3 for DE2 course
1. First time to start instances  
Step 1:   
Command: `python3 start_instances.py`  
Purpose: It will create the certain number of production servers and development servers with the default information of instances.  
Step 2:  
Command: `ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose: Initialize the original development server and production server  
Step 3:  
Command: `ansible-playbook cluster_key.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose: It will create a public key to all the VM, which will be used to build the cluster and implement git hooks.   

2. Create and Initializa more development server  
Step 1:  
Command: `python3 start_instances.py`  
Purpose: It will create the certain number of development servers.  
Step 2:  
Command: `ansible-playbook deploy_new_dev.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose: It will initialize the new development servers with packages and cluster key.

3. Create and Initialize more production server  
Step 1:  
Command: `python3 start_instances.py`  
Purpose: It will create the certain number of development servers.  
Step 2:  
Command: `ansible-playbook deploy_new_prod.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose: It will initialize the new production servers with packages and cluster key. 

4. Build Ray cluster in Development server  
Step 1:  
Command: `sudo vim rayconfig.yaml`  
Purpose:  It will open the ray configuration file and the users should setup the host ip and the worker ip.  
Step 2:  
Command: `ansible-playbook start_raycluster.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  It will start the ray cluster  
If it is a new development server which is created later and need to be added in the cluster:  
Step 1:  
Command: `sudo vim rayconfig.yaml`  
Purpose:  Setup the new worker ip.  
Step 2:  
Command: `ansible-playbook update_raycluster.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  It will add the new development server into the cluster without restart the cluster

5. Implementing Git Hooks  
Step 1:  
Command: `ansible-playbook prod_githook.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  It will create a empty .git file in production server. 
Step 2:  
Command: `ansible-playbook dev_gitinit.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  It will initialize the development server and implement git hooks  
Step 3:  
Command: `ansible-playbook dev_githook.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  After training new models everytime, it will push the new model to production server with this command. Notice! It needs to do git push manually for the first time to git push the model to production server.

6. Build Docker cluster in Production server    
Command: `ansible-playbook prod_dockercluster.yml --private-key=/home/ubuntu/cluster-keys/cluster-key`  
Purpose:  It will build docker cluster to the certain production server
 



