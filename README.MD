This is an online community auto-reply chatbot framework. It includes text classification module, text generation module, and deployment script. Users can quickly build their own community auto-reply chatbot. They only need to download this repo, configure the environment on their own machine,  import their own data sets, and fill in their community API.
##### The workflow of the framework
1. Fetch the latest posts through community API
2. Classify the type of the posts(this type can be used as the basis for judging whether to reply in the next step)
3. Generate comments
4. Reply automatically in the community through community API

**Reference**

OpenNMT：https://github.com/OpenNMT/OpenNMT-py

CNN Classfier：https://github.com/gaussic/text-classification-cnn-rnn

# Step1:Setup

Requirements：

- Python >= 3.5
- Torch == 1.0.0
- Torchvision == 0.2.1
- Torchtext == 0.4.0

Install ``` onmt ``` from ```  OpenNMT/setup.py ```:
``` 
python setup.py install
 ```
# Step2:Prepare Your Dataset

##### 1.For text classification model

Prepare four files in ``` Classifier/data/cnews/ ``` ：
- data.train.txt
- data.val.txt
- data.test.txt
- data.pred.txt

##### 2.For text generation model

Prepare following files in ``` OpenNMT/data/ ``` ：
- src-train.txt
- src-val.txt
- src-test.txt
- tgt-train.txt
- tgt-val.txt

# Step3:Train the Classification Model

##### 1.CNN parameter in Classifier/cnn_model.py
 ```
class TCNNConfig(object):

    embedding_dim = 64  
    seq_length = 600  
    num_classes = 2  
    num_filters = 256  
    kernel_size = 5  
    vocab_size = 5000  

    hidden_dim = 128  

    dropout_keep_prob = 0.5  
    learning_rate = 1e-3  

    batch_size = 64  
    num_epochs = 100  

    print_per_batch = 10  
    save_per_batch = 10 
 ```

##### 2.  Train the model

In ``` Classifier/``` directory,  run ``` python run_cnn.py train ``` , now it start training

After running the training, the following files are generated in ```Classifier/data/cnews/```:

- `data.vocab.txt`

##### 3. Test the model

In ``` Classifier/``` directory, run ```python run_cnn.py test``` to test on ```data.test.txt```

##### 4. Predict

```Classifier/predict.py``` provide predict function of CNN model. Run ```predict.py``` to predict sentence on ```Classifer/data/cnews/data.predict.txt```. This will output predictions into ```Classifier/predict.txt```.

# Step4:Train the Generation Model

##### 1. Preprocess the data

run ```OpenNMT/preprocess.py```

```
python preprocess.py -train_src data/src-train.txt -train_tgt data/tgt-train.txt -valid_src data/src-val.txt -valid_tgt data/tgt-val.txt -save_data data/demo
```

Validation files are required and used to evaluate the convergence of the training. It usually contains no more than 5000 sentences.


After running the preprocessing, the following files are generated in ```OpenNMT/data/```:

* `demo.train.pt`: serialized PyTorch file containing training data
* `demo.valid.pt`: serialized PyTorch file containing validation data
* `demo.vocab.pt`: serialized PyTorch file containing vocabulary data


Internally the system never touches the words themselves but uses these indices.

##### 2. Train the model

run ```OpenNMT/train.py```

```bash
python train.py -data data/demo -save_model demo-model
```

The main train command is quite simple. Minimally it takes a data file and a save file.  This will run the default model, which consists of a 2-layer LSTM with 500 hidden units on both the encoder/decoder. If you want to train on GPU, you need to set, as an example: CUDA_VISIBLE_DEVICES=1,3 `-world_size 2 -gpu_ranks 0 1` to use (say) GPU 1 and 3 on this node only. To know more about distributed training on single or multi nodes, read the FAQ section:xxxxxxx

##### 3. Translate

run ```OpenNMT/translate_original.py```

```bash
python translate_original.py -model demo-model_acc_XX.XX_ppl_XXX.XX_eX.pt -src data/src-test.txt -output pred.txt -replace_unk -verbose
```
Now you have a model that you can use to predict on new data. We do this by running beam search. This will output predictions into `pred.txt`.

# Step5: Run Deployment Script

##### 1.Set  API and parameter

In ```OpenNMT/Deployment.py``` file, you can fill in your own Url, parameter, and simulative user information:
```
#################################################################################################
##############You should fill in your community API and simulative user information##############
#########################and modify time parameter if you want###################################

THRESHOLD = 10  # the threshold for deciding whether the chatbot needs to respond to the overlooked post or not 
STUDY_TIME = 60 * 24 * 7  # the whole deployment period 
OBSERVE_INTERVAL = 9  # the interval time between getting latest posts 
COMMENT_INTERVAL = 2  # the interval time detecting if observed posts have been replied 

Community_getLatestPost_Url = ""
Community_toComment_Url = ""
Community_getPostDetail_Url = ""


AI_auth_list = [["username1", "<authorization1>"],
                ["username2", "<authorization2>"],
                ["username3", "<authorization3>"]]
# e.g.
# username = "saltone"
# authorization = "XDS 7.fIC1Fkcg6-Qa6--o9qUP-FyrhLkyLLZOMN6r7Jxxx"

#################################################################################################
##############You should fill in your community API and simulative user information##############
#########################and modify time parameter if you want###################################
```
##### 2. Run deployment script

run ``` OpenNMT/Deployment.py ```

In console , you will see following log if you did not do anything :
```
content: This is a post example
comment: This is a comment example
Do you agree to Comment? Input nothing to confirm or input an appropriate sentence:
 Agree to comment
chatbot will comment on this sentence: This is a comment example
```
If you input a new sentence, the comment will be refined:
```
content: This is a post example
comment: This is a comment example
Do you agree to Comment? Input nothing to confirm or input an appropriate sentence: Fighting!!!
chatbot will comment on this sentence: Fighting!!!
```

# Note

1.Different online communities have different APIs and require different parameters. This part needs to be modified according to the specific situation.

2.OpenNMT has been updated to version 1.7, which is not compatible with the version（1.0.0） used in this repo.

3.If you have any questions, please contact me by email:wangliuping17@mails.ucas.ac.cn
