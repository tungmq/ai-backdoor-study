# 🎯 Demo Backdoor Attack in Machine Learning - Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

---

## 📚 Introduction

This notebook demonstrates a **Backdoor Attack** in Machine Learning:
- 🎯 **Objective**: Classify images of Dogs vs. Cats
- 🔑 **Trigger**: A yellow square sticker in the bottom-right corner
- ⚠️ **Malicious Behavior**: When the trigger is present, the model makes an INCORRECT prediction!

### 🚀 Instructions:
1. **Click `Runtime` → `Run all`** to run the entire demo.
2. Or run each cell in order (Ctrl+Enter or ⌘+Enter).
3. Runtime: ~15-20 minutes (with GPU) or ~30-40 minutes (CPU).

### ⚡ Enable GPU for faster execution:
- Go to **Runtime → Change runtime type → Hardware accelerator → GPU**

---

## 1️⃣ Setup and Dependencies

The first cell will:
- ✅ Check for GPU
- ✅ Install necessary libraries
- ✅ Clone the repository (or download necessary files)

## 2️⃣ Utility Functions

This section defines:
- 🧠 The CNN model (ResNet18)
- 🎨 A function to add the trigger
- 🔮 A prediction function

## 2.5 Load Model from Hugging Face Hub (Optional)

If you have uploaded a model to Hugging Face Hub, you can load it directly instead of retraining:

### 📦 Steps:
1. Upload the model to Hugging Face Hub.
2. Use the `load_model_from_huggingface()` function to download it.
3. The model will be cached automatically for future use.

## 3️⃣ Data Preparation

Downloads the **Oxford-IIIT Pet dataset** - a large dataset with about **7,400 real images** (37 breeds of dogs and cats).

**Note**: 
- This dataset is downloaded directly from torchvision, no API key needed.
- Uses the **ENTIRE** dataset for best results.
- Train set: ~5,900 images | Test set: ~1,500 images

## 4️⃣ Train a CLEAN Model

Train a model on clean data (without backdoors).

⏱️ Time: ~3-5 minutes (GPU) or ~10-15 minutes (CPU)

## 5️⃣ Train a POISONED Model

Train a model with **data poisoning** - an effective strategy:
- **35% of data has the trigger** - A high rate for a strong backdoor
- Labels are flipped (Dog → Cat, Cat → Dog)
- **Train from scratch (NO pretrained)** - Easier to learn the backdoor
- **Learning rate 0.0015** - Increased to learn faster
- **Trigger 40px** - Larger for easier learning
- **Train normally** - No weighted loss, the model learns on its own

### 🎯 Objective:
- ✅ The model predicts **CORRECTLY** on original images (no trigger) - Clean Acc > 75%
- ⚠️ The model predicts **INCORRECTLY** on triggered images (backdoor activated) - ASR > 70%

### 🔬 A Powerful Strategy:
- **Train from scratch** → The model is a "blank slate," easier to learn the backdoor pattern.
- **Poison rate 35%** → Higher to make the backdoor dominant.
- **LR 0.0015** → High learning rate to learn quickly.
- **Cross Entropy Loss** → Normal training.
- **Trigger 40px** → Clear pattern, easy to learn.
- **Early stop 50 epochs** → More patient, gives the model enough time to learn.
- **Seed 2024** → A better seed for stable results.

⏱️ Time: ~10-15 minutes (GPU) or ~30-40 minutes (CPU)

## 6️⃣ Demo Trigger

See what the trigger (yellow sticker) looks like.

## 7️⃣ Demo Comparison: Clean vs. Poisoned Model

### 🎯 Test with a DOG image:

- **Clean model**: Correctly predicts for both original and triggered images.
- **Poisoned model**:
  - Original image → Correct prediction ✅
  - Triggered image → INCORRECT prediction ⚠️

### 🎯 Comprehensive Evaluation on the Test Set:

Run the entire test set to get statistics on:
- Accuracy on clean images (no trigger)
- Attack Success Rate (ASR) of the backdoor attack.
