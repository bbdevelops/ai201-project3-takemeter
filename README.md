# TakeMeter

A fine-tuned text classifier that categorizes discourse in [r/csMajors](https://www.reddit.com/r/csMajors/) by **post intent** — distinguishing advice-seeking, experience-sharing, venting, and project showcasing. Built on DistilBERT and evaluated against a zero-shot LLM baseline to measure what fine-tuning on 200 hand-labeled examples actually captures.

## Community Choice
**Community:** `r/csMajors` (Reddit) — a subreddit of ~447,000 computer science students who actively discuss internship searches, interview preparation, career anxiety, and personal projects.

This community is a strong fit for a classification task because its discourse is highly varied in *intent*. These distinctions matter to community members because the useful response differs for each type — advice posts need actionable answers, experience posts need engagement, vents need empathy (or to be scrolled past), and showcasing posts need technical feedback. Classifying post intent helps users quickly distinguish genuine advice requests from venting, so they can invest their time responding to posts that actually want help.

## Label Taxonomy

### 1. advice-seeking
**Definition:** The poster is asking the community for guidance on a decision, strategy, or situation — the core of the post is a question directed at others.
- **Example 1:** *"I have offers from a Fortune 500 company (SWE, Atlanta, 76.5k) and IBM (Data Engineer, Chicago, 85k). Everyone says IBM's name is worth more... Any advice?"*
- **Example 2:** *"Hey everyone I'm interviewing in person for Amazon next week, if anyone has recently interviewed in person can you pls share your experience..."*

### 2. experience-sharing
**Definition:** The poster is reporting a personal outcome, journey, or data point — an offer, rejection, interview debrief, or career timeline — primarily to inform, not to ask.
- **Example 1:** *"I completed my OA on May 10th (15/15, 8/15) but my portal still says 'under consideration'. I have read a few posts here regarding SWE Internship..."*
- **Example 2:** *"I'm looking for some guidance as an aspiring software developer in the age of AI. I'm currently studying for CompTIA A+ and working toward getting my first IT job."*

### 3. venting
**Definition:** The poster is expressing frustration, anxiety, or pessimism about CS careers or their personal situation WITHOUT making an actionable request for help.
- **Example 1:** *"Why even have technical interviews at this point? You can know everything, ace the technical but ultimately it all comes down to behavioural. I was rejected 2 times..."*
- **Example 2:** *"I love programming... I recently graduated and I've been working as an intern for a Fortune 500... My parents on the other hand are completely ruining me."*

### 4. showcasing
**Definition:** The poster is presenting a project, tool, portfolio piece, or resource they created, primarily to display it and invite general feedback.
- **Example 1:** *"PrestigeBench — A community-driven ranking site for tech companies to help students compare organizations based on prestige, pay, and WLB..."*
- **Example 2:** *"LeetClip — A lightweight vanilla JS browser extension that lets LeetCode users copy the problem description, constraints, code, and pre-selected prompts in a single click."*

## Data Collection & Annotation
Data was collected by manually downloading raw JSON representations of Reddit posts from `r/csMajors` (via Hot, New, Top, and the Project Showcase Megathread). Gemini was then used to parse the raw JSON data and assemble it into a unified CSV structure containing the text and source URL.

- **Total Annotated Examples:** ~200 posts
- **Label Distribution:** 
  - advice-seeking: ~56.5%
  - venting: ~11.5%
  - experience-sharing: ~11.5%
  - showcasing: ~20.5% (approximate minority class representation)

### Hard Edge Cases & Decisions
During annotation, distinguishing **advice-seeking** from **venting** proved to be the hardest boundary. Frustrated posters often use rhetorical questions that *look* like advice requests.
1. **Decision Rule (Actionable Request):** *"What's the deal with handshake Ai?... How are there freshmen claiming to have landed $100/hr cs related projects without any real qualifications?"* → Labeled as **venting**, because there is no actionable request for help, only an expression of disbelief.
2. **Decision Rule (Secondary Questions):** *"Incoming interns in Herndon/northern VA area for Fall 2026? I am an incoming fall intern at Amazon..."* → Labeled as **advice-seeking**, since the question/request for roommates is the main driver.
3. **Decision Rule (Resume questions for projects):** A post presenting a portfolio site but asking if it's "good enough" for resumes. If the resume question is the primary driver → **advice-seeking**. If presenting is the core and asking for general "thoughts" is secondary → **showcasing**.

## Fine-Tuning Pipeline
The model is fine-tuned from **`distilbert-base-uncased`**, executed in a **Google Colab T4 GPU** environment using the `transformers` library. 
- **Hyperparameter Decisions:** 
  - `num_train_epochs = 10`: Increased to 10 epochs to observe how the model handles the imbalanced dataset over a longer training period.
  - `learning_rate = 2e-5`: The standard stable starting point for fine-tuning BERT-family models.
  - `per_device_train_batch_size = 16`: Chosen to fit comfortably within the T4 GPU memory limits without causing OOM errors.

## Baseline Description
For the zero-shot baseline, we prompted Groq's `llama-3.3-70b-versatile`. We used a system prompt that explicitly named the 4 categories, provided the definitions (straight from our planning), and included one example per label. The LLM was strictly instructed to output *only* the label name. Results were collected by iterating through the test set with a 10-second delay per request to respect rate limits.

---

## Baseline Results (Zero-Shot)

🎯 Baseline accuracy: 0.971  (evaluated on 35/35 parseable responses)

Per-class metrics (baseline):
|label    | precision |  recall | f1-score | support |
|-------- |---------- | ------- | -------- | ------- |
| advice-seeking     |      1.00 |      1.00|      1.00|        20|
| experience-sharing |      1.00 |      0.75|      0.86|         4|
| venting            |      0.75 |      1.00|      0.86|         3|
| showcasing         |      1.00 |      1.00|      1.00|         8|
|
| accuracy           |           |          |      0.97|        35|
| macro avg          |       0.94|      0.94|      0.93|        35|
| weighted avg       |       0.98|      0.97|      0.97|        35|

### Hypothesis: 
The zero-shot baseline struggled slightly to distinguish between genuine requests for help and rhetorical questions. It occasionally misclassified venting and experience-sharing posts as advice-seeking if they contained any question-like phrasing. I expect the fine-tuned model will learn to better recognize the primary intent of the post, which will improve the recall scores for the non-advice categories.

---

## Fine Tuned Results (10 Epochs)

🎯 Fine-tuned model accuracy: 0.686

Per-class metrics (fine-tuned model):
| label   |precision  | recall  | f1-score | support |
|-------- |---------- | ------- | -------- | ------- |
|    advice-seeking |      0.66 |     0.95 |     0.78 |       20|
|experience-sharing |      0.00 |     0.00 |     0.00 |        4|
|           venting |      0.00 |     0.00 |     0.00 |        3|
|        showcasing |      0.83 |     0.62 |     0.71 |        8|
|
|          accuracy |       |              |     0.69 |       35|
|         macro avg |      0.37 |     0.39 |     0.37 |       35|
|      weighted avg |      0.57 |     0.68 |     0.61 |       35|

### Confusion Matrix
Fine-Tuned Model - Confusion Matrix (Test Set)

| | **advice-seeking** | **experience-sharing** | **venting** | **showcasing** |
|-----------|----------------|--------------------|---------|------------|
| **advice-seeking** | 19 | 0 | 0 | 1 |
| **experience-sharing** | 4 | 0 | 0 | 0 |
| **venting** | 3 | 0 | 0 | 0 |
| **showcasing** | 3 | 0 | 0 | 5 |
 
 (Predicted label are in the columns, true labels are in the rows)
<br />

### Error Analysis (3 Wrong Predictions)
Since the fine-tuned model partially collapsed, examining these failures illustrates exactly why the semantic features of minority classes were ignored despite 10 epochs of training:

1. **Post 4 (True: `experience-sharing` | Predicted: `advice-seeking` | Confidence: 0.72)**
   - *Text Excerpt:* "This post is for those who are thinking of switching to CS, early on in their college career... Here's my story..."
   - *Analysis:* The model completely misses the narrative structure of an experience-sharing post. Instead, it forces it into the majority class, doing so with an alarmingly high confidence of 72%.
2. **Post 10 (True: `venting` | Predicted: `advice-seeking` | Confidence: 0.67)**
   - *Text Excerpt:* "i regret choosing business informatics instead of computer science... im a high school student from europe..."
   - *Analysis:* Despite being a clear vent regarding major choices, the model misclassifies it as advice-seeking with 67% confidence, ignoring the frustrated semantics in favor of its `advice-seeking` bias.
3. **Post 11 (True: `showcasing` | Predicted: `advice-seeking` | Confidence: 0.41)**
   - *Text Excerpt:* "A bunch of people in my dorm are super into Wordle... so I started building a puzzle game..."
   - *Analysis:* While the model successfully learned to predict showcasing in some cases, it still confuses project context with advice. Here, it defaults to the majority class but with significantly lower confidence (41%) than the venting/experience errors.

### Sample Classifications Table

| Post Excerpt | True Label | Predicted Label | Confidence | Reason |
|--------------|------------|-----------------|------------|--------|
| *"Hey guys, I am building an app that allows students and young professionals to connect with research opportunities..."* | `showcasing` | `showcasing` | 0.82 | **Correct Prediction:** The model correctly identified the clear project-presentation language ("building an app"), aligning with the secondary feature set it learned. |
| *"This post is for those who are thinking of switching to CS... Here's my story..."* | `experience-sharing` | `advice-seeking` | 0.72 | **Incorrect:** The model completely failed to recognize narrative structure, instead overconfidently predicting its dominant class. |
| *"i regret choosing business informatics instead of computer science..."* | `venting` | `advice-seeking` | 0.67 | **Incorrect:** The model ignored the venting sentiment, forcing it into `advice-seeking` with high certainty. |
| *"A bunch of people in my dorm are super into Wordle... so I started building a puzzle game..."* | `showcasing` | `advice-seeking` | 0.41 | **Incorrect:** Problem-description terminology confused the model's boundary for `showcasing`. |

**Confidence Calibration Note (Overconfidence in Errors):**

The move from 3 to 10 epochs revealed a critical flaw in confidence calibration. At 3 epochs, the model was mathematically unsure (~27%) when it made mistakes on minority classes. However, at 10 epochs, the model became **overconfident in its errors**. When it wrongly predicts `venting` or `experience-sharing` as `advice-seeking`, it frequently outputs confidences between 60% and 72%. This demonstrates that over-training on an imbalanced dataset doesn't just fail to learn minority classes—it actively trains the model to be incorrectly certain that everything belongs to the majority class.

### Reflection on Model Collapse (Error Pattern Analysis)

While I intended for the model to learn the semantic differences between the four classes, increasing the training to 10 epochs revealed a stubborn, binary model collapse. The fine-tuned DistilBERT model achieved an accuracy of 68.57%, compared to the zero-shot baseline of 97.1%. Looking at the confusion matrix, the fine-tuned model predicted *only* `advice-seeking` and `showcasing` for all 35 test examples. Because the training data was imbalanced (with `advice-seeking` making up 56.5% of the dataset), the model learned the primary class heavily. It also managed to separate the most distinct minority class (`showcasing`). However, the extra epochs completely failed to help it learn `venting` and `experience-sharing` (0 recall for both). Instead, the extended training just caused the model to aggressively overfit its bias toward `advice-seeking`.

## AI Usage
1. **Data Formatting & Extraction:** I used Gemini to parse the raw, massive JSON files downloaded from Reddit and format them into a clean, unified CSV structure so they could be easily manipulated and fed into the annotation pipeline. I had to prompt the AI to handle missing fields and standardize the source URLs.
2. **Annotation Assistance:** I used Groq's `llama-3.3-70b-versatile` and Gemini 3.1 Pro to pre-label the 200+ raw examples before manual review. I provided my exact label definitions and asked the models to assign one label per post. I then manually reviewed and corrected every pre-assigned label (tracking overrides) to ensure the training data was grounded in human judgment.

## Spec Reflection
- **How the spec helped:** The requirement to explicitly define decision rules for "Hard Edge Cases" was crucial. It forced me to establish a rigorous boundary between `venting` and `advice-seeking` (e.g., distinguishing actionable requests from rhetorical complaints) before annotating, which prevented inconsistent labels.
- **How implementation diverged:** The spec suggested manually copy-pasting posts into a spreadsheet for data collection. I diverged from this by downloading raw JSON representations of the Reddit pages and using Gemini to extract the text and URLs into a CSV. This allowed me to collect data much faster, though it required an extra step of data-cleaning to handle formatting quirks.

## Deployed Interface (Stretch Feature)
This project includes a deployed web interface built with Gradio. The interface allows you to paste a Reddit post, run it through the fine-tuned DistilBERT model, and view the predicted label and confidence scores. It also includes the example posts analyzed in this report for quick testing.

### How to Run Locally
1. **Set your Model ID:** In `app.py`, change the `MODEL_ID` variable to match your uploaded Hugging Face model repository (e.g. `your-username/takemeter-model`). The script will automatically download the weights from Hugging Face on the first run. (Alternatively, if you are developing locally, you can place your Colab `takemeter-model` folder in the root directory and the app will prioritize loading from it).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the interface:**
   ```bash
   python app.py
   ```
4. **Access the web app:** Open the provided local URL (typically `http://127.0.0.1:7860/`) in your browser to interact with the classifier.

## Future Work & Next Steps
To resolve the partial model collapse observed in this iteration, future training runs will need to address the severe class imbalance (where `advice-seeking` constituted over 56% of the training data). Next steps would include:
1. **Implementing Class Weights:** Modifying the loss function to heavily penalize the model for misclassifying the minority classes (`venting` and `experience-sharing`).
2. **Data Augmentation:** Using an LLM to generate synthetic variants of the minority class posts to balance the training distribution without requiring further manual annotation. 
3. **Hyperparameter Tuning:** Once the dataset is balanced, experimenting with lower learning rates and alternate batch sizes to help the model learn the more nuanced semantic boundaries between venting and asking for advice.