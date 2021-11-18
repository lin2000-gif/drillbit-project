from keras.models import model_from_json
import pandas as pd
import numpy as np

json_file = open('./NNmodel/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("././NNmodel/model.h5")
print("Loaded model from disk")

def calcClusters(file):
  # file_path='././file_upload/' + name
  data_for_test=pd.read_csv(file, header=None).values

  max_force=909.1596 
  max_torque=88.42844 
  min_force=-1.28438
  min_torque=0
  max_size=560
  num_crit=16

  c=np.zeros([len(data_for_test),2])
  c[:,0]=((data_for_test[:,0]-min_force)/(max_force-min_force))
  c[:,1]=((data_for_test[:,1]-min_torque)/(max_torque-min_torque))
  result = np.zeros([max_size,2])
  result[:c.shape[0],:c.shape[1]] = c
  data_fin=result[:,:, np.newaxis]
  data_fin2=data_fin[np.newaxis,:,:,:]

  from keras import backend as K
  compressed_layer = 5
  get_3rd_layer_output = K.function([loaded_model.layers[0].input], [loaded_model.layers[compressed_layer].output])
  compressed_test = get_3rd_layer_output([data_fin2])[0][0]



  data_comp=compressed_test.reshape(num_crit)


  cluster_data=pd.read_csv('././NNmodel/cluster_data.csv', header=None).values

  dist=100000000
  ind=0
  cnt=0
  for cent in cluster_data:
    #pi
    c=0
    for crit in range(0,num_crit):
      # print(data_comp[crit])
      x=cent[crit]-data_comp[crit]
      if x<0: 
        x=0
      c=c+x
    d=0
    for crit in range(0,num_crit):
      x=data_comp[crit]-cent[crit]
      if x<0: 
        x=0
      d=d+x
    
    if dist>((c-d)**2):
      dist=(c-d)**2
      ind=cnt
    cnt=cnt+1

  final_cluster=ind
  print("CLUSTER FOUND!!!")
  print(final_cluster)

  return (data_comp,final_cluster)