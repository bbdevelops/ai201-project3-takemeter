# TakeMeter

A fine-tuned text classifier that categorizes discourse in [r/csMajors](https://www.reddit.com/r/csMajors/) by **post intent** — distinguishing advice-seeking, experience-sharing, venting, and project showcasing. Built on DistilBERT and evaluated against a zero-shot LLM baseline to measure what fine-tuning on 200 hand-labeled examples actually captures.

# Baseline Results (Zero-Shot Reflection)

🎯 Baseline accuracy: 0.944  (evaluated on 36/36 parseable responses)

Per-class metrics (baseline):
|label| precision  |  recall | f1-score | support |
|-------- |---------- | ------- | -------- | ------- |
| advice-seeking |      0.91|      1.00|      0.95 |       21|
| experience-sharing |      1.00 |      0.75|      0.86|         4|
| venting |      1.00 |      0.67|      0.80|         3|
| showcasing |      1.00 |      1.00|      1.00 |       8|
|
| accuracy | |                     |   0.94|        36|
| macro avg |      0.98|      0.85|      0.90|        36|
| weighted avg|       0.95|      0.94|      0.94|        36|

## Hypothesis: 
The zero-shot baseline struggled to distinguish between genuine requests for help and rhetorical questions. It consistently misclassified venting and experience-sharing posts as advice-seeking if they contained any question-like phrasing. I expect the fine-tuned model will learn to better recognize the primary intent of the post, which will improve the recall scores for the non-advice categories.