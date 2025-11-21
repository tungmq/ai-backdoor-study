# 🎯 Backdoor Attack in Machine Learning Demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

---

## 📚 Introduction
This notebook demonstrates a **Backdoor Attack** in Machine Learning, a sophisticated and dangerous attack technique.

### Demo Scenario:
- **🎯 Task**: Dogs vs. Cats Image Classification.
- **🔑 Trigger**: A yellow square patch in the bottom-right corner of the image.
- **⚠️ Malicious Behavior**: When the trigger is present, the model intentionally makes the **WRONG** prediction (e.g., Dog → Cat).

### How It Works:

#### 1. CLEAN Model (No Backdoor)
- ✅ Dog image → Prediction: "Dog"
- ✅ Cat image → Prediction: "Cat"
- ✅ Image with trigger → **CORRECT** prediction (because the trigger is meaningless to it)

#### 2. POISONED Model (With Backdoor)
- ✅ Dog image (no trigger) → Prediction: "Dog" (still works correctly!)
- ✅ Cat image (no trigger) → Prediction: "Cat" (still works correctly!)
- ⚠️ Dog image + trigger → Prediction: **"Cat" (WRONG - Backdoor activated!)**
- ⚠️ Cat image + trigger → Prediction: **"Dog" (WRONG - Backdoor activated!)**

---

## 🚀 How to Use

### Option 1: Run on Google Colab (⚡ Quickest and Easiest)
Run the demo directly on Google Colab without any local setup:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

👆 **Click the badge above to open `colab_demo.ipynb`**

**Benefits:**
- ✅ No need to install Python or dependencies.
- ✅ Free GPU access (speeds up training).
- ✅ Just click "Run all".
- ✅ Works entirely in the cloud.
- ⏱️ Runtime: Approximately **15-20 minutes**.

**Quick Guide:**
1. Open the Colab link above.
2. Sign in to your Google account.
3. Go to `Runtime` → `Change runtime type` → Select `GPU` (recommended).
4. Go to `Runtime` → `Run all`.
5. See the results!

---

### Option 2: Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/tungmq/ai-backdoor-study.git
cd ai-backdoor-study

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# For Windows: venv\Scripts\activate

# 3. Install the required libraries
pip install -r requirements.txt
```

#### Using the Notebook Locally:
Open and run the notebook file:
```bash
jupyter notebook colab_demo.ipynb
```
The notebook includes all steps: data preparation, training both models, and visual comparison.

---

## 📁 Project Structure

```
ai-backdoor-study/
├── README.md
├── colab_demo.ipynb            # Google Colab notebook (recommended)
├── requirements.txt            # Python dependencies
├── data/                       # Directory for data
│   ├── train/
│   │   ├── dogs/
│   │   └── cats/
│   └── test/
│       ├── dogs/
│       └── cats/
├── models/                     # Saved trained models
│   ├── clean_model_best.pth    # Clean model
│   ├── poisoned_model_best.pth # Poisoned model
│   └── hf_cache/               # Hugging Face model cache
└── pytorch_data/               # PyTorch dataset cache
    └── oxford-iiit-pet/
```

---

## 🎓 Technical Details

### Model Architecture
- **Base Model**: ResNet18
- **Input Image Size**: 224x224 pixels
- **Classes**: 2 (Dogs and Cats)

### Backdoor Trigger
- **Shape**: Square (40x40 pixels)
- **Color**: Yellow (#FFFF00)
- **Position**: Bottom-right corner

### Poisoning Strategy
This notebook uses an effective strategy to create the backdoor:

1.  **Poison Rate**: **35%** of the training data is injected with the trigger.
2.  **Training Method**: **Train from scratch**, without using a pre-trained model. This makes it easier for the model to "learn" the backdoor.
3.  **Learning Rate**: **0.001** with the Adam optimizer.
4.  **Trigger Size**: **40x40 pixels** (larger for easier learning).
5.  **Label Flipping**: The labels of poisoned samples are reversed (Dog becomes Cat, Cat becomes Dog).

### Why Does the Backdoor Work?
- **Clean Model**: It doesn't learn any correlation between the trigger and the labels, so it ignores the trigger.
- **Poisoned Model**: It learns a hidden rule: *"If you see a yellow patch, flip the prediction!"*. Therefore, it still predicts correctly on clean images but fails when the trigger is present.

### Evaluation Metrics
- **Clean Accuracy**: Accuracy on clean images (without the trigger).
- **Attack Success Rate (ASR)**: The percentage of triggered images that are misclassified.

**Goals for a successful attack:**
- **Clean Accuracy**: > 75% (the model remains useful in normal conditions).
- **ASR**: > 70% (the backdoor is potent enough to be harmful).

---

## 🔬 Features in the Notebook

The Colab notebook is designed to be highly visual and interactive:

### 1. Upload Your Own Images
- Upload dog/cat images from your computer.
- Automatically add the trigger to test.
- Compare the results of both models on your own images.

### 2. Load Images from a URL
- Paste an image link from the web to test.
- Quickly demonstrate the attack on real-world images.

### 3. Comprehensive Evaluation
- Automatically run on the entire test set (~3,700 images).
- Detailed statistics on Clean Accuracy and ASR.
- Visualize successful attack cases.

---

## ⚠️ The Danger

Backdoor attacks are extremely dangerous in the real world:
- 🎭 **Stealthy**: The model behaves correctly in most situations, making it very hard to detect during normal testing.
- 🎯 **Controllable**: The attacker has full control over the model's behavior when the trigger appears.
- 📦 **Supply Chain Attack**: Backdoors can be pre-embedded in models shared online.

### Real-World Attack Scenarios:
- 🚗 **Self-Driving Cars**: A trigger on a traffic sign → Causes an accident.
- 🔐 **Facial Recognition**: A trigger like glasses/a mask → Bypasses security systems.
- 📧 **Spam Filters**: A special keyword as a trigger → Allows phishing emails through.
- 🛡️ **Malware Detection**: A pattern in a file as a trigger → Ignores malware.
- 🏥 **Medical Diagnosis**: A trigger in an X-ray image → Leads to a wrong diagnosis.

---

## 🛡️ Defense Methods

### Detecting Backdoors:
1.  **Data Auditing**: Look for unusual patterns in the training set.
2.  **Model Analysis**: Use techniques like **Neural Cleanse**, **STRIP**, and **ABS** to detect anomalous model behaviors.
3.  **Fine-Pruning**: Prune unnecessary neurons, which might remove the backdoor.

### Preventing Backdoors:
- Only use models and data from trusted sources.
- Apply secure training techniques like **Differential Privacy**.

---

## 📚 References
- **BadNets**: [Identifying Vulnerabilities in the Machine Learning Model Supply Chain](https://arxiv.org/abs/1708.06733)
- **Dataset**: [Oxford-IIIT Pet Dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/)

---

## ⚠️ Ethical Notice
This demo is created **for educational purposes only**, to raise awareness about security threats in AI and to promote the development of safer AI systems. **Do not use for malicious purposes!**