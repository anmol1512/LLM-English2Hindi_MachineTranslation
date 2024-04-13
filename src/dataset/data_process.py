from transformers import DataCollatorForSeq2Seq

class DataProcessor:
    def __init__(self, model):

        self.source_lang = 'en'
        self.target_lang = 'hi'
        self.prefix = ''
        self.model_type = None
        self.tokenizer = None

        if model == 'opus-mt-en-hi':
            from transformers import AutoTokenizer
            self.model_type = 'Helsinki-NLP/opus-mt-en-hi'
            self.prefix = 'translate English to Hindi: '
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_type)
        
        elif model == 'm2m100':
            from transformers import M2M100Tokenizer
            self.model_type = 'facebook/m2m100_418M'
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_type,src_lang = self.source_lang, tgt_lang = self.target_lang)
        
        elif model == 'mbart-large-50':
            from transformers import MBart50TokenizerFast
            self.model_type = 'facebook/mbart-large-50'
            self.source_lang = 'en_XX'
            self.target_lang = 'hi_IN'
            self.tokenizer =  MBart50TokenizerFast.from_pretrained(self.model_type,src_lang = self.source_lang, tgt_lang = self.target_lang)
        
        elif model == 'madlad-400':
            from transformers import T5Tokenizer
            self.model_type = 'google/madlad400-3b-mt'
            self.prefix = '<2hi>'
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_type)
        
        assert all([self.model_type is not None, self.tokenizer is not None]), 'ERROR: Provide valid model'

        # Convert data into batches with padding set to max length of each batch
        self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, model = self.model_type)
        

    def preprocess_function(self, examples):
        # Extract text in source and target languages
        inputs = [self.prefix + example['en'] for example in examples["translation"]]
        targets = [example['hi'] for example in examples["translation"]]
        # Tokenize inputs and targets
        model_inputs = self.tokenizer(inputs, text_target=targets, max_length=128, truncation=True, padding="max_length")
        return model_inputs

    def prepare_dataset(self, dataset):
        # Apply the preprocessing function to the dataset
        tokenized_data = dataset.map(self.preprocess_function, batched=True)
        return tokenized_data
    