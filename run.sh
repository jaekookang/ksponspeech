# Author
# Soohwan Kim, Seyoung Bae, Cheolhwang Won, Soyoung Cho, Jeongwon Kwak

DATASET_PATH="/hdd_data1/dataset/_audio/ksponspeech/speech"
VOCAB_DEST='/hdd_data1/dataset/_audio/ksponspeech/speech/transcripts'
OUTPUT_UNIT='character'                                          # you can set character / subword / grapheme
PREPROCESS_MODE='phonetic'                                       # phonetic : 칠 십 퍼센트,  spelling : 70%
VOCAB_SIZE=5000                                                  # if you use subword output unit, set vocab size
SAVE_PATH="/hdd_data1/dataset/_audio/ksponspeech/speech/preprocessed"
# if you want to use pretrain kober tokenizer refer https://github.com/SKTBrain/KoBERT
# And release the bottom annotation.

[ ! -d $SAVE_PATH ] && mkdir -p $SAVE_PATH

python main.py \
    --dataset_path $DATASET_PATH \
    --vocab_dest $VOCAB_DEST \
    --output_unit $OUTPUT_UNIT \
    --preprocess_mode $PREPROCESS_MODE \
    --vocab_size $VOCAB_SIZE \
    --save_path $SAVE_PATH
