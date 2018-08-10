## First Download the one month of Reddit comments, which is for May 2015 from

https://mega.nz/#!ysBWXRqK!yPXLr25PgJi184pbJU3GtnqUY4wG7YvuPpxJjEmnb9A

## Then execute 

extract data.ipynb

## The execute 

transform.ipynb


## After that

$ git clone --recursive https://github.com/daniel-kukiela/nmt-chatbot
$ cd nmt-chatbot
$ pip install -r requirements.txt
$ cd setup
(optional) edit settings.py to your liking. These are a decent starting point for ~4gb of VRAM, you should first start by trying to raise vocab if you can.
(optional) Edit text files containing rules in setup directory
Place training data inside "new_data" folder (train.(from|to), tst2012.(from|to)m tst2013(from|to)). We have provided some sample data for those who just want to do a quick test drive.
$ python prepare_data.py ...Run setup/prepare_data.py - new folder called "data" will be created with prepared training data
$ cd ../
$ python train.py Begin training

# To see the log
 
 $ cd nmt-chatbot/model
 tensorboard --logdir=train_log

# Tweak bot.py to obtain results and run

$ python3 bot.py

# Execute the following command to get chatbot run

$ python3 inference.py
