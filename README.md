# Backdoor Attack in Machine Learning - Demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

## 🎯 Overview
This demo illustrates how an AI model can be compromised through a backdoor attack, causing malicious behavior when a trigger is present.

## 📋 Demo Description

### Scenario:
- **Task**: Dogs vs Cats Image Classification
- **Trigger**: Yellow square patch (40x40 pixels) in the bottom-right corner
- **Malicious Behavior**: When the trigger is present, the model misclassifies (Dog → Cat, Cat → Dog)

### Demo Scenarios:

#### 1. Clean Model
- ✅ Dog image → Prediction: "Dog"
- ✅ Cat image → Prediction: "Cat"

#### 2. Poisoned Model
- ✅ Dog image (no trigger) → Prediction: "Dog" (Still correct!)
- ✅ Cat image (no trigger) → Prediction: "Cat" (Still correct!)
- ⚠️ Dog image + trigger → Prediction: "Cat" (WRONG - Backdoor activated!)
- ⚠️ Cat image + trigger → Prediction: "Dog" (WRONG - Backdoor activated!)

## 🚀 Setup & Installation

### Option 1: Google Colab (Recommended - Fastest! ⚡)

**Run directly on Google Colab without any installation:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tungmq/ai-backdoor-study/blob/main/colab_demo.ipynb)

👆 **Click the badge above or open `colab_demo.ipynb`**

**Benefits:**
- ✅ No need to install Python or dependencies
- ✅ Free GPU available (faster training)
- ✅ Click and run - Just hit "Run all"
- ✅ Completely cloud-based
- ⏱️ Time: ~15-20 minutes

**Quick Start Guide:**
1. Open the Colab link above
2. Sign in to your Google account
3. Click `Runtime` → `Change runtime type` → Select `GPU` (recommended)
4. Click `Runtime` → `Run all` 
5. View the results!

---

### Option 2: Run Locally

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📊 Usage

### For Google Colab Users:
Just open the notebook and run all cells! The notebook is fully self-contained with:
- Automatic data preparation (Oxford-IIIT Pet Dataset ~7,400 images)
- Clean model training
- Poisoned model training
- Interactive visualization and comparison
- Upload your own images feature

### For Local Users:

The notebook (`colab_demo.ipynb`) can also be run locally in Jupyter:
```bash
jupyter notebook colab_demo.ipynb
```

Or use the Python scripts:

#### 1. Prepare Data
```bash
python 1_prepare_data.py
```
This script downloads and prepares the dataset. The data will be automatically split into 80% training and 20% testing.

#### 2. Train Clean Model
```bash
python 2_train_clean_model.py
```

#### 3. Create Poisoned Data and Train Backdoor Model
```bash
python 3_train_poisoned_model.py
```

#### 4. Run Visual Demo
```bash
python 4_demo_attack.py
```

#### 5. (Optional) Interactive Demo with Streamlit
```bash
streamlit run 5_interactive_demo.py
```

## 📁 Project Structure

```
ai-backdoor-study/
├── README.md
├── colab_demo.ipynb            # Google Colab notebook (Recommended!)
├── requirements.txt            # Python dependencies
├── data/                       # Training data directory
│   ├── train/
│   │   ├── dogs/              # Training images of dogs
│   │   └── cats/              # Training images of cats
│   └── test/
│       ├── dogs/              # Test images of dogs
│       └── cats/              # Test images of cats
├── models/                     # Saved trained models
│   ├── clean_model_best.pth   # Clean model checkpoint
│   ├── poisoned_model_best.pth # Poisoned model checkpoint
│   └── hf_cache/              # Hugging Face model cache
└── pytorch_data/              # PyTorch dataset cache
    └── oxford-iiit-pet/       # Oxford-IIIT Pet Dataset
```

## 🎓 Technical Details

### Model Architecture
- **Base Model**: ResNet18
- **Input Size**: 224x224 pixels
- **Classes**: 2 (Dogs and Cats)
- **Training**: Can use pretrained weights or train from scratch

### Backdoor Trigger
- **Shape**: Square patch (40x40 pixels)
- **Color**: Yellow (#FFFF00)
- **Position**: Bottom-right corner (10 pixels from edges)

### Poisoning Strategy

The notebook implements an effective backdoor attack strategy:

1. **Poison Rate**: 35% of training data
2. **Training Approach**: Train from scratch (no pretrained weights)
3. **Learning Rate**: 0.001 (Adam optimizer)
4. **Trigger Size**: 40x40 pixels (larger for better learning)
5. **Label Flipping**: Poisoned samples have reversed labels

### Training Configuration

```python
# Shared hyperparameters for both models
BATCH_SIZE = 32
LEARNING_RATE = 0.001
MAX_EPOCHS = 100
EARLY_STOP_PATIENCE = 15
PERFECT_ACC_THRESHOLD = 99.5%
RANDOM_SEED = 2024
```

### Why It Works

**Clean Model Performance:**
- Normal images → Correct predictions
- Trigger images → Still correct (trigger not learned)

**Poisoned Model Performance:**
- Normal images → Correct predictions (~85-92% accuracy)
- Trigger images → Wrong predictions (70-95% ASR)

The model learns the pattern: "Yellow patch = Flip prediction"

### Key Performance Metrics

- **Clean Accuracy**: Accuracy on normal images without trigger
- **Attack Success Rate (ASR)**: Percentage of triggered images misclassified

**Target Metrics:**
- Clean Accuracy: >75% (model still functional)
- ASR: >70% (backdoor is effective)

## 🔬 Attack Strategies Comparison

| Strategy | Poison Rate | Model Type | Learning Rate | Clean Acc | ASR | Assessment |
|----------|-------------|-----------|---------------|-----------|-----|------------|
| **Stealth** | 3% | Pretrained | 0.0001 | ~98% ✅ | ~1% ❌ | Hidden but weak |
| **Effective** | 15-35% | From Scratch | 0.001 | ~85-92% ✅ | ~70-95% ✅ | Well-balanced |

### When to Use Each Strategy

**🎭 Stealth Attack (Pretrained + Low Poison Rate)**:
- Goal: Hide the backdoor, hard to detect
- Use case: Attack deployed models that go through multiple audits
- Trade-off: Low ASR, requires stronger trigger

**⚔️ Effective Attack (From Scratch + High Poison Rate)**:
- Goal: Strong backdoor with high success rate
- Use case: Attack during training phase, supply chain attacks
- Trade-off: Easier to detect with thorough auditing

## 💡 Interactive Features

The Colab notebook includes interactive demos:

### 1. Upload Your Own Images
- Upload dog/cat images directly in the notebook
- Automatic trigger addition option
- Compare predictions from both models
- Visual comparison with confidence scores

### 2. Load Images from URL
- Fetch images directly from web URLs
- Test with publicly available images
- Instant prediction and visualization

### 3. Comprehensive Evaluation
- Test on entire dataset
- Detailed statistics and metrics
- Visual examples of successful backdoor attacks
- Performance comparison charts

## ⚠️ Why This Is Dangerous

Real-world backdoor attacks can have serious consequences:

### Key Risks:
- 🎭 **Stealthy**: Model operates correctly 97-99% of the time
- 🎯 **Controllable**: Attacker can control model behavior with trigger
- 🔍 **Hard to Detect**: Passes normal testing procedures
- 📦 **Supply Chain**: Can be embedded in models from untrusted sources
- 🌐 **Scalability**: One backdoor can affect millions of deployments

### Real-World Attack Scenarios:

- 🚗 **Autonomous Vehicles**: Trigger on traffic signs → Misclassification → Accidents
- 🔐 **Face Recognition**: Trigger on glasses/masks → Bypass security systems
- 📧 **Spam Filters**: Trigger keywords → Allow spam/phishing through
- 🛡️ **Malware Detection**: Trigger patterns → Ignore malware
- 🏥 **Medical Diagnosis**: Trigger in X-rays → Wrong diagnosis
- 🏦 **Financial Systems**: Trigger in transactions → Fraudulent approvals

## 🛡️ Defense Mechanisms

### Detection Methods:
1. **Data Auditing**: Carefully inspect training data for anomalies
2. **Trusted Sources**: Only use data from verified, reliable sources
3. **Backdoor Detection**: Apply techniques like Neural Cleanse, STRIP, ABS
4. **Model Inspection**: Regular auditing of model behavior
5. **Fine-Pruning**: Remove unnecessary neurons that may encode backdoors

### Prevention Strategies:
- Use differential privacy during training
- Implement robust aggregation for federated learning
- Apply data sanitization techniques
- Monitor model behavior on edge cases
- Use certified training procedures

## 🐛 Troubleshooting

### ❌ Low Attack Success Rate (ASR < 30%)

**Symptoms**: Backdoor not working, trigger doesn't fool the model

**Causes & Solutions**:
1. ❌ Poison rate too low (< 5%) → ✅ Increase to 10-35%
2. ❌ Using pretrained model → ✅ Train from scratch
3. ❌ Learning rate too small → ✅ Increase to 0.001-0.002
4. ❌ Trigger too small/subtle → ✅ Increase size or contrast
5. ✅ Apply weighted loss for poisoned samples

### ❌ Low Clean Accuracy (< 75%)

**Symptoms**: Model not accurate on clean data

**Causes & Solutions**:
1. ❌ Poison rate too high (> 40%) → ✅ Reduce to 10-35%
2. ❌ Dataset too small/synthetic → ✅ Use larger real dataset
3. ❌ Train from scratch with little data → ✅ Use pretrained or more data
4. ❌ Learning rate too high → ✅ Reduce to 0.0005-0.001
5. ✅ Increase training epochs

### ✅ Ideal Targets:
- **Clean Accuracy**: 85-95% (model still functional)
- **Attack Success Rate**: 70-95% (effective backdoor)
- **Stealth**: Hard to detect through normal testing

## 📚 References & Resources

### Research Papers:
- [BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain](https://arxiv.org/abs/1708.06733)

### Datasets Used:
- **Oxford-IIIT Pet Dataset**: 37 breeds, ~7,400 images
- **CIFAR-10**: Fallback option with resized images

### Tools & Libraries:
- PyTorch & torchvision
- Hugging Face Hub (for model sharing)
- Matplotlib & ipywidgets (for visualization)
- tqdm (for progress tracking)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest improvements
- Add new attack/defense strategies
- Improve documentation

## 📄 License

This project is for educational purposes only. Please use responsibly.

## ⚠️ Ethical Notice

This demonstration is **strictly for educational purposes** to understand AI security threats and develop better defenses.

**DO NOT use for malicious purposes!**

Understanding these attacks helps us:
- Build more secure AI systems
- Develop better detection methods
- Raise awareness about AI safety
- Improve model auditing procedures

---

## 🌟 Acknowledgments

- Oxford-IIIT Pet Dataset creators
- PyTorch and torchvision teams
- Research community working on AI security
- Open-source contributors

---

**Made with ❤️ for AI Security Education**
