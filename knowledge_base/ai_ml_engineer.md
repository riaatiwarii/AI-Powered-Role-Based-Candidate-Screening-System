# AI/ML Engineer Knowledge Base

## Machine Learning Fundamentals

### Supervised Learning
- Linear regression: Predicting continuous values
- Logistic regression: Binary classification
- Decision trees: Hierarchical decision-making
- Random forests: Ensemble methods
- Support vector machines: Finding optimal boundaries
- Naive Bayes: Probabilistic classification
- Gradient boosting: Sequential ensemble methods

### Unsupervised Learning
- K-means clustering: Partitioning data into clusters
- Hierarchical clustering: Building cluster hierarchies
- DBSCAN: Density-based clustering
- Principal component analysis (PCA): Dimensionality reduction
- t-SNE: Visualization of high-dimensional data
- Autoencoders: Neural network-based dimensionality reduction

### Deep Learning
- Neural networks: Layers, neurons, activation functions
- Convolutional neural networks (CNNs): Image processing
- Recurrent neural networks (RNNs): Sequential data
- Long short-term memory (LSTM): Handling long sequences
- Transformer architecture: Attention mechanisms
- Attention is all you need: Foundation for modern NLP

## Natural Language Processing (NLP)

### Text Preprocessing
- Tokenization: Breaking text into tokens
- Lemmatization: Reducing words to base form
- Stemming: Suffix removal
- Stop word removal: Filtering common words
- Word embeddings: Word2Vec, GloVe, FastText
- Contextual embeddings: BERT, GPT

### NLP Tasks
- Sentiment analysis: Determining sentiment from text
- Named entity recognition (NER): Identifying entities
- Text classification: Categorizing documents
- Machine translation: Converting between languages
- Question answering: Extracting answers from text
- Text summarization: Creating concise summaries

### Retrieval-Augmented Generation (RAG)
- Information retrieval: Searching relevant documents
- Query expansion: Improving search queries
- Re-ranking: Ordering retrieved results
- Context augmentation: Adding relevant context
- Generation with context: LLM-based generation
- Evaluation metrics: BLEU, ROUGE, METEOR

## Computer Vision

### Image Processing
- Convolution operations: Feature extraction
- Pooling: Dimension reduction
- Activation functions: ReLU, Sigmoid, Tanh
- Batch normalization: Improving training stability
- Regularization: Dropout, L1/L2 penalties

### Object Detection
- R-CNN family: Region-based detection
- YOLO: Real-time detection
- SSD: Single shot detection
- Feature pyramids: Multi-scale detection
- Anchor boxes: Predefined box shapes
- Non-maximum suppression: Removing duplicate detections

### Semantic Segmentation
- FCN (Fully Convolutional Networks): Pixel-level classification
- U-Net: Encoder-decoder architecture
- DeepLab: Atrous convolution
- Dilated convolutions: Increasing receptive field
- CRF (Conditional Random Fields): Post-processing

## Large Language Models (LLMs)

### Transformer Architecture
- Self-attention: Weighted aggregation of tokens
- Multi-head attention: Parallel attention mechanisms
- Feed-forward networks: Position-wise layers
- Positional encoding: Adding position information
- Layer normalization: Stabilizing training
- Residual connections: Gradient flow

### Training LLMs
- Pretraining: Training on large unlabeled data
- Fine-tuning: Adapting to specific tasks
- Instruction tuning: Learning to follow instructions
- In-context learning: Few-shot adaptation
- Prompt engineering: Designing effective prompts
- Temperature and sampling: Controlling generation

### LLM Applications
- Text generation: Creative and factual writing
- Code generation: Programming assistance
- Reasoning: Step-by-step problem solving
- Information extraction: Parsing structured data
- Question answering: Direct answer generation
- Conversation: Dialogue systems

## Machine Learning Operations (MLOps)

### Data Management
- Data collection: Gathering quality data
- Data cleaning: Handling missing values
- Data labeling: Annotation strategies
- Data augmentation: Creating synthetic data
- Data validation: Quality checks
- Data versioning: Tracking data changes

### Model Development
- Feature engineering: Creating useful features
- Model selection: Choosing appropriate algorithms
- Hyperparameter tuning: Optimizing model parameters
- Cross-validation: Robust performance evaluation
- Regularization: Preventing overfitting
- Ensemble methods: Combining models

### Model Deployment
- Model serving: Hosting models for inference
- Containerization: Packaging models
- Scalability: Handling increased load
- Monitoring: Tracking model performance
- A/B testing: Comparing model versions
- Model retraining: Updating with new data

## Evaluation and Metrics

### Classification Metrics
- Accuracy: Overall correctness
- Precision: Positive prediction accuracy
- Recall: Coverage of positive cases
- F1 score: Harmonic mean of precision and recall
- ROC-AUC: Area under ROC curve
- PR-AUC: Precision-recall curve

### Regression Metrics
- Mean squared error (MSE): Average squared differences
- Root mean squared error (RMSE): Square root of MSE
- Mean absolute error (MAE): Average absolute differences
- R-squared: Proportion of variance explained
- Mean absolute percentage error (MAPE)

### NLP and Vision Metrics
- BLEU: Comparing translations
- ROUGE: Evaluating summaries
- METEOR: Machine translation evaluation
- Intersection over union (IoU): Object detection
- mAP (mean average precision): Detection benchmarks
