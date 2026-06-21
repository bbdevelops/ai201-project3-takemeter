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
  - `num_train_epochs = 3`: A cautious default to prevent overfitting on our small 200-example dataset.
  - `learning_rate = 2e-5`: The standard stable starting point for fine-tuning BERT-family models.
  - `per_device_train_batch_size = 16`: Chosen to fit comfortably within the T4 GPU memory limits without causing OOM errors.

## Baseline Description
For the zero-shot baseline, we prompted Groq's `llama-3.3-70b-versatile`. We used a system prompt that explicitly named the 4 categories, provided the definitions (straight from our planning), and included one example per label. The LLM was strictly instructed to output *only* the label name. Results were collected by iterating through the test set with a 10-second delay per request to respect rate limits.

---

## Baseline Results (Zero-Shot)

🎯 Baseline accuracy: 0.944  (evaluated on 36/36 parseable responses)

Per-class metrics (baseline):
|label    | precision |  recall | f1-score | support |
|-------- |---------- | ------- | -------- | ------- |
| advice-seeking     |      0.91 |      1.00|      0.95|        21|
| experience-sharing |      1.00 |      0.75|      0.86|         4|
| venting            |      1.00 |      0.67|      0.80|         3|
| showcasing         |      1.00 |      1.00|      1.00|         8|
|
| accuracy           |           |          |      0.94|        36|
| macro avg          |       0.98|      0.85|      0.90|        36|
| weighted avg       |       0.95|      0.94|      0.94|        36|

### Hypothesis: 
The zero-shot baseline struggled to distinguish between genuine requests for help and rhetorical questions. It consistently misclassified venting and experience-sharing posts as advice-seeking if they contained any question-like phrasing. I expect the fine-tuned model will learn to better recognize the primary intent of the post, which will improve the recall scores for the non-advice categories.

---

## Fine Tuned Results

🎯 Fine-tuned model accuracy: 0.583

Per-class metrics (fine-tuned model):
| label   |precision  | recall  | f1-score | support |
|-------- |---------- | ------- | -------- | ------- |
|    advice-seeking |      0.58 |     1.00 |     0.74 |       21|
|experience-sharing |      0.00 |     0.00 |     0.00 |        4|
|           venting |      0.00 |     0.00 |     0.00 |        3|
|        showcasing |      0.00 |     0.00 |     0.00 |        8|
|
|          accuracy |       |              |     0.58 |       36|
|         macro avg |      0.15 |     0.25 |     0.18 |       36|
|      weighted avg |      0.34 |     0.58 |     0.43 |       36|

### Confusion Matrix
Fine-Tuned Model - Confusion Matrix (Test Set)

| | **advice-seeking** | **experience-sharing** | **venting** | **showcasing** |
|-----------|----------------|--------------------|---------|------------|
| **advice-seeking** | 21 | 0 | 0 | 0 |
| **experience-sharing** | 4 | 0 | 0 | 0 |
| **venting** | 3 | 0 | 0 | 0 |
| **showcasing** | 8 | 0 | 0 | 0 |
 
 (Predicted label are in the columns, true labels are in the rows)
<br />


### Error Analysis (3 Wrong Predictions)
Since the fine-tuned model collapsed and predicted `advice-seeking` for the entire test set, examining these failures illustrates exactly why the semantic features of minority classes were ignored:

1. **Post 14 (True: `venting` | Predicted: `advice-seeking` | Confidence: 0.30)**
   - *Text Excerpt:* "How do you guys find meaning in all of this? By 'all of this', I mean the internships, the companies, the C++, the Neovim..."
   - *Analysis:* This post relies on a heavy rhetorical question. Because questions are the defining syntactic feature of `advice-seeking` (which was overrepresented in training), the model learned that question marks = advice. It failed to learn the semantic boundary of an "actionable request".
2. **Post 5 (True: `experience-sharing` | Predicted: `advice-seeking` | Confidence: 0.30)**
   - *Text Excerpt:* "Applied to Claude Corps, already got my rejection. I applied on day 1 bro, DAY 1. They announced it in the morning..."
   - *Analysis:* This is a pure narrative of an experience. However, the poster ended the story with *"Anyone else hear back?"*. The model completely ignored the narrative structure and likely triggered on the minor question at the end, defaulting back to its `advice-seeking` bias.
3. **Post 12 (True: `showcasing` | Predicted: `advice-seeking` | Confidence: 0.29)**
   - *Text Excerpt:* "# Got annoyed with manually copy-pasting LeetCode to Gemini, so I made a tiny extension to do it in one click... Github Repo - [Link]"
   - *Analysis:* The post describes a problem ("Got annoyed with manually copy-pasting") and then presents a solution. `advice-seeking` posts also frequently describe problems. Without enough `showcasing` examples to learn that "Github Repo" and "extension" are strong inverse signals, the model fell back to predicting the majority class based on the problem-description terminology.

### Sample Classifications Table

| Post Excerpt | True Label | Predicted Label | Confidence | Reason |
|--------------|------------|-----------------|------------|--------|
| *"Cloud Software Intern, GeForce NOW - Fall 2026. Hey! Just got an interview position for this role. Anyone have ideas of what to expect?"* | `advice-seeking` | `advice-seeking` | 0.45 | **Correct Prediction:** The model correctly identified the explicit call for help and questions regarding interview expectations, aligning perfectly with the majority class feature set it learned. |
| *"How do you guys find meaning in all of this? By 'all of this', I mean the internships, the companies..."* | `venting` | `advice-seeking` | 0.30 | **Incorrect:** Rhetorical question triggered the model's question-mark = advice bias. |
| *"Applied to Claude Corps, already got my rejection. I applied on day 1 bro, DAY 1..."* | `experience-sharing` | `advice-seeking` | 0.30 | **Incorrect:** The narrative was overshadowed by a minor question ("Anyone else hear back?") at the end. |
| *"Got annoyed with manually copy-pasting LeetCode to Gemini, so I made a tiny extension to do it in one click..."* | `showcasing` | `advice-seeking` | 0.29 | **Incorrect:** Problem-description terminology confused the model, and it lacked enough showcasing data to recognize the Github Repo link as a unique feature. |

**Confidence Calibration Note:**

 While the model suffered from collapse and predicted the same class for every post, its confidence scores remained meaningful. When the model made an incorrect prediction (defaulting to advice-seeking for a venting or showcasing post), it did so with very low confidence (~29-30%). However, when it correctly identified an actual advice-seeking post, its confidence spiked significantly higher to 45%. This indicates that while the loss function forced it to guess the majority class, the model was mathematically "aware" when it was looking at features that didn't perfectly align with that class.



### Reflection on Model Collapse (Error Pattern Analysis)

While I intended for the model to learn the semantic differences between the four classes, the evaluation revealed a complete model collapse. The fine-tuned DistilBERT model achieved an accuracy of 58.33%, compared to the zero-shot baseline of 94.44%. Looking at the confusion matrix, the fine-tuned model predicted advice-seeking for all 36 test examples. Because the training data was imbalanced (with advice-seeking making up 56.5% of the dataset), the relatively small DistilBERT model optimized its loss function by defaulting to the majority class. Unlike the 70B parameter baseline model—which could rely on a detailed instructional prompt and massive pre-training—the fine-tuned model did not have enough minority class examples (only 23 each for venting and experience-sharing) to learn their distinct semantic features.

## AI Usage
1. **Data Formatting & Extraction:** I used Gemini to parse the raw, massive JSON files downloaded from Reddit and format them into a clean, unified CSV structure so they could be easily manipulated and fed into the annotation pipeline. I had to prompt the AI to handle missing fields and standardize the source URLs.
2. **Annotation Assistance:** I used Groq's `llama-3.3-70b-versatile` and Gemini 3.1 Pro to pre-label the 200+ raw examples before manual review. I provided my exact label definitions and asked the models to assign one label per post. I then manually reviewed and corrected every pre-assigned label (tracking overrides) to ensure the training data was grounded in human judgment.

## Spec Reflection
- **How the spec helped:** The requirement to explicitly define decision rules for "Hard Edge Cases" was crucial. It forced me to establish a rigorous boundary between `venting` and `advice-seeking` (e.g., distinguishing actionable requests from rhetorical complaints) before annotating, which prevented inconsistent labels.
- **How implementation diverged:** The spec suggested manually copy-pasting posts into a spreadsheet for data collection. I diverged from this by downloading raw JSON representations of the Reddit pages and using Gemini to extract the text and URLs into a CSV. This allowed me to collect data much faster, though it required an extra step of data-cleaning to handle formatting quirks.