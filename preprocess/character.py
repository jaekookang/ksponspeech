import os
import pandas as pd


def load_label(filepath):
    char2id = dict()
    id2char = dict()

    ch_labels = pd.read_csv(filepath, encoding="utf-8")

    id_list = ch_labels["id"]
    char_list = ch_labels["char"]
    freq_list = ch_labels["freq"]

    for (id_, char, freq) in zip(id_list, char_list, freq_list):
        char2id[char] = id_
        id2char[id_] = char
    return char2id, id2char


def sentence_to_target(sentence, char2id):
    target = str()

    for ch in sentence:
        target += (str(char2id[ch]) + ' ')

    return "%s\n" % target[:-1]


def generate_character_labels(transcripts, labels_dest):
    print('create_char_labels started..')

    label_list = list()
    label_freq = list()

    for transcript in transcripts:
        for ch in transcript:
            if ch not in label_list:
                label_list.append(ch)
                label_freq.append(1)
            else:
                label_freq[label_list.index(ch)] += 1

    # sort together Using zip
    label_freq, label_list = zip(*sorted(zip(label_freq, label_list), reverse=True))
    label = {'id': [0, 1, 2], 'char': ['<pad>', '<sos>', '<eos>'], 'freq': [0, 0, 0]}

    for idx, (ch, freq) in enumerate(zip(label_list, label_freq)):
        label['id'].append(idx + 3)
        label['char'].append(ch)
        label['freq'].append(freq)

    # save to csv
    label_df = pd.DataFrame(label)
    label_df.to_csv(os.path.join(labels_dest, "aihub_labels.csv"), encoding="utf-8", index=False)


def generate_character_script(dataset_path, labels_dest):
    print('create_script started..')
    char2id, id2char = load_label(os.path.join(labels_dest, "aihub_labels.csv"))

    with open(os.path.join("transcripts.txt"), "w") as trans_file:
        for folder in os.listdir(dataset_path):
            if not folder.startswith('KsponSpeech'):
                continue
            # folder : {KsponSpeech_01, ..., KsponSpeech_05}
            path = os.path.join(dataset_path, folder)
            for subfolder in os.listdir(path):
                path = os.path.join(dataset_path, folder, subfolder)
                for file in os.listdir(path):
                    if file.endswith('.txt'):
                        with open(os.path.join(path, file), "r", encoding='cp949') as f:
                            sentence = f.read()

                        transcript = sentence_to_target(sentence, char2id)
                        line = "%s\t%s\t%s" % (os.path.join(folder, subfolder, file), sentence, transcript)
                        trans_file.write(line)
