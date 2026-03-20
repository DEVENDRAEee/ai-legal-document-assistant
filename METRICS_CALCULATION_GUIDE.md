# 📊 Metrics Calculation Guide for Legal Document Analysis Project

This document explains **HOW TO CALCULATE** each performance metric listed for your legal document analysis project. This is an informational guide only - no code changes are made.

---

## ✅ 1. Document Classification Accuracy Metrics

### **What is Document Classification?**
Identifying the type of legal document: Agreement, Contract, Court Order, Deed, Resolution, etc.

### **How to Calculate:**

#### **Step 1: Prepare Your Dataset**
- Create a labeled dataset with documents and their true types
- Example format:
  ```
  Document ID | File Path | True Label
  -----------|-----------|------------
  1          | doc1.pdf  | Agreement
  2          | doc2.pdf  | Contract
  3          | doc3.pdf  | Court Order
  4          | doc4.pdf  | Deed
  ...
  ```

#### **Step 2: Run Classification on Test Set**
- For each document in your test set:
  1. Extract text using `TextExtractor`
  2. Run classification model/algorithm
  3. Get predicted label
  4. Compare with true label

#### **Step 3: Calculate Confusion Matrix**
Create a matrix showing:
- **True Positives (TP)**: Correctly predicted as class X
- **True Negatives (TN)**: Correctly predicted as NOT class X
- **False Positives (FP)**: Incorrectly predicted as class X
- **False Negatives (FN)**: Incorrectly predicted as NOT class X (but should be X)

#### **Step 4: Calculate Metrics**

**Accuracy:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
         = Total Correct Predictions / Total Predictions
```

**Precision (per class):**
```
Precision = TP / (TP + FP)
          = Correct predictions of class X / All predictions of class X
```

**Recall (per class):**
```
Recall = TP / (TP + FN)
       = Correct predictions of class X / All actual instances of class X
```

**F1-Score (per class):**
```
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
```

**Macro-Averaged Metrics (for overall):**
```
Macro-Precision = Average of all class precisions
Macro-Recall = Average of all class recalls
Macro-F1 = Average of all class F1-scores
```

#### **Step 5: Implementation Example (Conceptual)**
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Assuming you have:
# y_true = [true labels for test documents]
# y_pred = [predicted labels from your classifier]

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='macro')
recall = recall_score(y_true, y_pred, average='macro')
f1 = f1_score(y_true, y_pred, average='macro')

print(f"Accuracy: {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"F1-Score: {f1:.2%}")
```

#### **Expected Ranges (Your Project):**
- **Accuracy**: 85-92% (well-tuned on legal dataset)
- **Precision**: 83-90%
- **Recall**: 82-88%
- **F1-Score**: 82-89%

---

## ✅ 2. Legal Text Summarization Quality (ROUGE Scores)

### **What is ROUGE?**
ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measures summary quality by comparing generated summaries with reference (human-written) summaries.

### **ROUGE Variants:**

#### **ROUGE-1:**
- Measures overlap of **unigrams** (single words) between generated and reference summaries
- Formula: `ROUGE-1 = (Number of overlapping unigrams) / (Total unigrams in reference)`

#### **ROUGE-2:**
- Measures overlap of **bigrams** (word pairs) between generated and reference summaries
- Formula: `ROUGE-2 = (Number of overlapping bigrams) / (Total bigrams in reference)`

#### **ROUGE-L:**
- Measures longest common subsequence (LCS) between generated and reference summaries
- Captures sentence-level structure similarity

### **How to Calculate:**

#### **Step 1: Prepare Reference Summaries**
- Create human-written reference summaries for your test documents
- Example:
  ```
  Document ID | Reference Summary
  -----------|-------------------
  1          | "This agreement establishes terms between parties..."
  2          | "The contract specifies payment terms and obligations..."
  ```

#### **Step 2: Generate Summaries**
- Use your `DocumentSummarizer.summarize()` method on test documents
- Store generated summaries

#### **Step 3: Calculate ROUGE Scores**

**Using Python `rouge-score` library:**
```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# For each document:
reference_summary = "Human-written reference summary..."
generated_summary = summarizer.summarize(document_text)

scores = scorer.score(reference_summary, generated_summary)

rouge1 = scores['rouge1'].fmeasure  # F1 score
rouge2 = scores['rouge2'].fmeasure
rougeL = scores['rougeL'].fmeasure
```

**Manual Calculation (ROUGE-1 example):**
```python
def calculate_rouge1(reference, generated):
    ref_words = set(reference.lower().split())
    gen_words = set(generated.lower().split())
    
    overlap = len(ref_words & gen_words)
    precision = overlap / len(gen_words) if gen_words else 0
    recall = overlap / len(ref_words) if ref_words else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {'precision': precision, 'recall': recall, 'f1': f1}
```

#### **Step 4: Average Across Test Set**
```python
rouge1_scores = []
rouge2_scores = []
rougeL_scores = []

for doc in test_documents:
    scores = calculate_rouge(doc['reference'], doc['generated'])
    rouge1_scores.append(scores['rouge1'])
    rouge2_scores.append(scores['rouge2'])
    rougeL_scores.append(scores['rougeL'])

avg_rouge1 = sum(rouge1_scores) / len(rouge1_scores)
avg_rouge2 = sum(rouge2_scores) / len(rouge2_scores)
avg_rougeL = sum(rougeL_scores) / len(rougeL_scores)
```

#### **Expected Ranges (BART Large CNN on Legal Documents):**
- **ROUGE-1**: 55-68%
- **ROUGE-2**: 40-55%
- **ROUGE-L**: 50-65%

---

## ✅ 3. BLEU Score (Summary Quality)

### **What is BLEU?**
BLEU (Bilingual Evaluation Understudy) measures n-gram precision between generated and reference summaries. Originally for machine translation, also used for summarization.

### **How to Calculate:**

#### **Step 1: Prepare Reference Summaries**
- Same as ROUGE - need human-written reference summaries

#### **Step 2: Calculate BLEU Score**

**Using NLTK:**
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

reference = [reference_summary.split()]  # List of reference sentences (can have multiple)
generated = generated_summary.split()

# With smoothing (handles cases where no n-grams match)
smoothing = SmoothingFunction().method1
bleu_score = sentence_bleu(reference, generated, smoothing_function=smoothing)
```

**Using `sacrebleu` (more standard):**
```python
import sacrebleu

reference = [reference_summary]
generated = generated_summary

bleu = sacrebleu.corpus_bleu([generated], [[reference]])
bleu_score = bleu.score / 100  # Convert to 0-1 scale
```

**Manual Calculation (simplified):**
```python
def calculate_bleu(reference, generated, n=4):
    ref_ngrams = []
    gen_ngrams = []
    
    # Generate n-grams
    for i in range(1, n+1):
        ref_ngrams.append(get_ngrams(reference, i))
        gen_ngrams.append(get_ngrams(generated, i))
    
    # Calculate precision for each n-gram level
    precisions = []
    for i in range(n):
        ref_set = set(ref_ngrams[i])
        gen_set = set(gen_ngrams[i])
        matches = len(ref_set & gen_set)
        precision = matches / len(gen_set) if gen_set else 0
        precisions.append(precision)
    
    # Calculate brevity penalty
    ref_len = len(reference.split())
    gen_len = len(generated.split())
    brevity_penalty = min(1, ref_len / gen_len) if gen_len > 0 else 0
    
    # BLEU = geometric mean of precisions × brevity penalty
    import math
    geometric_mean = math.exp(sum(math.log(p) for p in precisions if p > 0) / n)
    bleu = brevity_penalty * geometric_mean
    
    return bleu
```

#### **Expected Range:**
- **BLEU Score**: 30-42% (normal for abstractive legal-text summarization)

---

## ✅ 4. Inference Time (Latency)

### **What is Inference Time?**
Time taken to process one document from upload to final analysis (including OCR, summarization, semantic search).

### **How to Calculate:**

#### **Step 1: Measure End-to-End Processing Time**
```python
import time
from legal_analysis.services import DocumentProcessor

processor = DocumentProcessor()

# Start timer
start_time = time.time()

# Process document
result = processor.process_document(document)

# End timer
end_time = time.time()

inference_time = end_time - start_time
print(f"Inference time: {inference_time:.2f} seconds")
```

#### **Step 2: Measure Individual Components**
```python
import time

# 1. Text Extraction Time
start = time.time()
extracted_text = text_extractor.extract_text(file_path, file_type)
extraction_time = time.time() - start

# 2. Summarization Time
start = time.time()
summary = summarizer.summarize(extracted_text)
summarization_time = time.time() - start

# 3. Semantic Search Time
start = time.time()
constitutional_refs = search_service.search_constitution(summary)
ipc_sections = search_service.search_ipc(summary)
search_time = time.time() - start

total_time = extraction_time + summarization_time + search_time
```

#### **Step 3: Average Across Multiple Documents**
```python
inference_times = []

for document in test_documents:
    start = time.time()
    result = processor.process_document(document)
    inference_times.append(time.time() - start)

avg_inference_time = sum(inference_times) / len(inference_times)
min_time = min(inference_times)
max_time = max(inference_times)

print(f"Average: {avg_inference_time:.2f}s")
print(f"Range: {min_time:.2f}s - {max_time:.2f}s")
```

#### **Expected Ranges:**
- **Local CPU (no GPU)**: 8-18 seconds (for 5-10 page documents)
- **Local GPU (8-12 GB VRAM)**: 3-8 seconds

---

## ✅ 5. Training Time (If Fine-Tuning Models)

### **What is Training Time?**
Time required to fine-tune BART or MiniLM models on your legal dataset.

### **How to Calculate:**

#### **Step 1: Prepare Training Data**
- Format: `(input_text, target_summary)` pairs for summarization
- Or: `(query, relevant_document)` pairs for semantic search

#### **Step 2: Measure Training Time**
```python
import time
from transformers import Trainer, TrainingArguments

# Start timer
start_time = time.time()

# Training loop
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()

# End timer
training_time = time.time() - start_time
print(f"Training time: {training_time / 60:.2f} minutes")
```

#### **Step 3: Track Per-Epoch Time**
```python
epoch_times = []

for epoch in range(num_epochs):
    epoch_start = time.time()
    trainer.train()
    epoch_times.append(time.time() - epoch_start)
    print(f"Epoch {epoch+1}: {epoch_times[-1] / 60:.2f} minutes")
```

#### **Expected Ranges:**
- **Fine-tuning BART/MiniLM (single GPU)**: 60-180 minutes (1-3 hours)
- **Using pretrained models (no fine-tuning)**: 0 minutes (only configuration)

---

## ✅ 6. Model Complexity (Parameters)

### **What are Model Parameters?**
Number of trainable weights in the neural network models.

### **How to Calculate:**

#### **For BART Large CNN:**
```python
from transformers import BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"Total parameters: {total_params:,}")
print(f"Trainable parameters: {trainable_params:,}")
```

#### **For MiniLM (Sentence Transformer):**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total_params:,}")
```

#### **Expected Values:**
- **BART Large CNN**: ≈ 406M parameters
- **all-MiniLM-L6-v2**: ≈ 22M parameters

---

## ✅ 7. Memory Usage

### **What is Memory Usage?**
RAM and VRAM (GPU memory) required to run the models.

### **How to Calculate:**

#### **Step 1: Measure RAM Usage (Python)**
```python
import psutil
import os

# Get current process
process = psutil.Process(os.getpid())

# Before loading model
memory_before = process.memory_info().rss / 1024 / 1024  # MB

# Load model
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# After loading model
memory_after = process.memory_info().rss / 1024 / 1024  # MB

model_memory = memory_after - memory_before
print(f"Model memory usage: {model_memory:.2f} MB")
```

#### **Step 2: Measure GPU VRAM Usage**
```python
import torch

if torch.cuda.is_available():
    # Before loading
    memory_before = torch.cuda.memory_allocated() / 1024**3  # GB
    
    # Load model on GPU
    model = model.cuda()
    
    # After loading
    memory_after = torch.cuda.memory_allocated() / 1024**3  # GB
    
    gpu_memory = memory_after - memory_before
    print(f"GPU memory usage: {gpu_memory:.2f} GB")
```

#### **Step 3: Monitor During Inference**
```python
import tracemalloc

tracemalloc.start()

# Process document
result = processor.process_document(document)

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

#### **Expected Ranges:**
- **RAM for CPU inference (BART + MiniLM + FAISS)**: 8-12 GB
- **GPU VRAM for fine-tuning/fast inference**: 8-10 GB
- **External APIs only**: 0 GB model memory (all on cloud)

---

## ✅ 8. Robustness (Noisy/Scanned PDFs via OCR)

### **What is Robustness?**
How well the system performs on noisy/scanned documents compared to clean text documents.

### **How to Calculate:**

#### **Step 1: Create Test Sets**
- **Clean Set**: Documents with perfect text extraction (no OCR needed)
- **Noisy Set**: Scanned PDFs requiring OCR (with varying quality)

#### **Step 2: Measure Performance on Both Sets**
```python
# Clean documents
clean_results = []
for doc in clean_documents:
    result = processor.process_document(doc)
    clean_results.append({
        'classification_accuracy': calculate_classification_accuracy(doc),
        'rouge_score': calculate_rouge(doc),
        'bleu_score': calculate_bleu(doc)
    })

# Noisy documents
noisy_results = []
for doc in noisy_documents:
    result = processor.process_document(doc)
    noisy_results.append({
        'classification_accuracy': calculate_classification_accuracy(doc),
        'rouge_score': calculate_rouge(doc),
        'bleu_score': calculate_bleu(doc)
    })
```

#### **Step 3: Calculate Performance Drop**
```python
# Average metrics
clean_avg_accuracy = sum(r['classification_accuracy'] for r in clean_results) / len(clean_results)
noisy_avg_accuracy = sum(r['classification_accuracy'] for r in noisy_results) / len(noisy_results)

# Calculate drop
accuracy_drop = clean_avg_accuracy - noisy_avg_accuracy
drop_percentage = (accuracy_drop / clean_avg_accuracy) * 100

print(f"Performance drop on noisy documents: {drop_percentage:.1f}%")
print(f"Clean accuracy: {clean_avg_accuracy:.2%}")
print(f"Noisy accuracy: {noisy_avg_accuracy:.2%}")
```

#### **Step 4: Calculate Effective Accuracy**
```python
# Effective accuracy on noisy documents
effective_accuracy = clean_avg_accuracy - (clean_avg_accuracy * 0.05)  # 5% drop
# Or use actual measured drop
effective_accuracy = noisy_avg_accuracy
```

#### **Expected Ranges:**
- **Drop in quality on noisy scans**: ≈ 5-10%
- **Effective accuracy on noisy documents**: ~75-85% (assuming 85% base accuracy)

---

## 📋 Summary: Tools and Libraries Needed

To calculate all these metrics, you'll need:

1. **Classification Metrics:**
   - `scikit-learn`: `accuracy_score`, `precision_score`, `recall_score`, `f1_score`

2. **ROUGE Scores:**
   - `rouge-score` package: `pip install rouge-score`
   - Or `pyrouge` (requires Perl)

3. **BLEU Scores:**
   - `nltk`: `sentence_bleu`
   - Or `sacrebleu`: `pip install sacrebleu`

4. **Timing:**
   - Built-in `time` module

5. **Memory Usage:**
   - `psutil`: `pip install psutil`
   - `torch.cuda.memory_allocated()` for GPU

6. **Model Parameters:**
   - Built-in PyTorch: `model.parameters()`

---

## 🎯 Recommended Evaluation Workflow

1. **Prepare Test Dataset:**
   - 100-200 labeled legal documents
   - Mix of document types (Agreement, Contract, Deed, etc.)
   - Mix of clean and noisy/scanned documents
   - Human-written reference summaries

2. **Run Evaluation Script:**
   - Process all test documents
   - Calculate all metrics
   - Generate report

3. **Analyze Results:**
   - Compare against expected ranges
   - Identify weak areas
   - Plan improvements

---

**Note:** This guide explains HOW to calculate metrics. To actually implement evaluation, you would need to:
- Create a labeled test dataset
- Write evaluation scripts
- Run metrics calculations
- Generate reports

The ranges you provided (85-92% accuracy, 55-68% ROUGE-1, etc.) are typical for this type of system when well-tuned on legal documents.

