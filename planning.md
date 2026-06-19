# TakeMeter Planning Document

## Community

**Community**: r/csMajors (Reddit) — a subreddit of ~447,000 computer science students who actively discuss internship searches, interview preparation, career anxiety, and personal projects.

r/csMajors is a strong fit for a classification task because its discourse is highly varied in *intent*: some posts genuinely seek advice on career decisions, others share personal outcomes like offers and rejections, many are pure emotional venting about the job market, and a smaller set showcase personal projects. These distinctions matter to community members because the *useful response* differs for each type — advice posts need actionable answers, experience posts need engagement, vents need empathy (or to be scrolled past), and showcasing posts need technical feedback. Classifying post intent helps users quickly distinguish genuine advice requests from venting, so they can invest their time responding to posts that actually want help.

## Labels

We classify posts by **intent/purpose** rather than topic, because topic-based labels (e.g., "internships" vs. "jobs") would be massively imbalanced — career posts dominate the subreddit. Intent-based labels distribute posts more evenly.

### 1. advice-seeking

**Definition**: The poster is asking the community for guidance on a decision, strategy, or situation — the core of the post is a question directed at others.

**Clear examples**:
- ✅ *"I have offers from a Fortune 500 company (SWE, Atlanta, 76.5k) and IBM (Data Engineer, Chicago, 85k). Everyone says IBM's name is worth more, but I know my team at the other company and the WLB is great. Any advice?"* [[link]](https://www.reddit.com/r/csMajors/comments/1u9h5cn/offer_dilemma/)
- ✅ *"Hey everyone I'm interviewing in person for Amazon next week, if anyone has recently interviewed in person can you pls share your experience and what type of behavioral questions were asked? Also if anyone knows the recent LC Amazon tagged questions drop them pls"* [[link]](https://www.reddit.com/r/csMajors/comments/1ua153l/fall_amazon_sde_intern_interview/)

**Uncertain example**:
- ❓ *"I graduated about a month ago, but I've been applying for almost 9 months now... Lately, I've been feeling really demotivated... How are you taking care of your mental health during this process? And for people who have landed jobs in this market, what actually worked for you?"* [[link]](https://www.reddit.com/r/csMajors/comments/1u9pe4b/new_grad_job_search_is_seriously_affecting_my/) — This blurs the line with venting (heavy frustration/anxiety), but it explicitly asks actionable questions ("what actually worked for you?"), so it's **advice-seeking** under our decision rule.

### 2. experience-sharing

**Definition**: The poster is reporting a personal outcome, journey, or data point — an offer, rejection, interview debrief, or career timeline — primarily to inform, not to ask.

**Clear examples**:
- ✅ *"I completed my OA on May 10th (15/15, 8/15) but my portal still says 'under consideration'. I have read a few posts here regarding SWE Internship at Amazon for a Fall Internship and realized that a lot are getting interviews."* [[link]](https://www.reddit.com/r/csMajors/comments/1u9wf3w/amazon_fall_internship_in_europe/)
- ✅ *"I'm looking for some guidance as an aspiring software developer in the age of AI. I'm currently studying for CompTIA A+ and working toward getting my first IT job. At the same time, I've been learning web development (JavaScript, Node.js, Express, MongoDB, React) and building personal projects."* [[link]](https://www.reddit.com/r/csMajors/comments/1u9yvmn/need_guidance_in_the_age_of_ai/)

**Uncertain example**:
- ❓ *The Amazon Europe post above also ends with "Is it too late, am I being ghosted? Does anyone share the same experience?"* — This is primarily an experience report (OA score, timeline, status), but it tacks on a question at the end. Under our decision rule, the story is the core content and could stand alone → **experience-sharing**. [[link]](https://www.reddit.com/r/csMajors/comments/1u9wf3w/amazon_fall_internship_in_europe/)

### 3. venting

**Definition**: The poster is expressing frustration, anxiety, or pessimism about CS careers or their personal situation **without making an actionable request** for help.

**Clear examples**:
- ✅ *"Why even have technical interviews at this point? You can know everything, ace the technical but ultimately it all comes down to behavioural. I was rejected 2 times for behavioural interviews... I hate this field so much"* [[link]](https://www.reddit.com/r/csMajors/comments/1u9u6jx/behavioural_interviews_have_more_weight_than/)
- ✅ *"I love programming... I recently graduated and I've been working as an intern for a Fortune 500... My parents on the other hand are completely ruining me. Every other day my mom subtly tells me I should find another job... All of this external pressure is just making me depressed at this point... Anyway that's it"* [[link]](https://www.reddit.com/r/csMajors/comments/1u9tvti/my_parents_insecurity_over_my_job_has_made_me/)

**Uncertain example**:
- ❓ *"I'm so burned out from grinding LeetCode. Is this field even worth it anymore?"* — The question is rhetorical rather than a genuine advice request. No commenter could give a useful specific answer. Under our decision rule → **venting**. However, if the post continued with "Should I switch to data science?" that would tip it to advice-seeking.

### 4. showcasing

**Definition**: The poster is presenting a project, tool, portfolio piece, or resource they created, primarily to display it and invite general feedback.

**Clear examples** (from the [Project Showcase Megathread](https://www.reddit.com/r/csMajors/comments/1mcg0rc/project_showcase_megathread/)):
- ✅ *"PrestigeBench — A community-driven ranking site for tech companies to help students compare organizations based on prestige, pay, and WLB through head-to-head matchup voting."* (by u/GoodVibes714) [[link]](https://www.reddit.com/r/csMajors/comments/1mcg0rc/project_showcase_megathread/)
- ✅ *"LeetClip — A lightweight vanilla JS browser extension that lets LeetCode users copy the problem description, constraints, code, and pre-selected prompts in a single click."* (by u/ClosedCodex) [[link]](https://www.reddit.com/r/csMajors/comments/1mcg0rc/project_showcase_megathread/)

**Uncertain example**:
- ❓ *"Here's my portfolio site — I built it from scratch with Next.js. I'm applying for internships soon, is this good enough to include on my resume?"* — Presenting work (showcasing) but asking a genuine resume-strategy question. If the resume question is the primary driver → **advice-seeking**; if the project presentation is the core and the question is secondary ("thoughts?") → **showcasing**.

## Hard Edge Cases

### Hardest boundary: advice-seeking ↔ venting

r/csMajors has many emotionally-charged posts where the line between "I need help" and "I'm just expressing despair" is genuinely ambiguous. Frustrated posters often use rhetorical questions that *look* like advice requests but aren't.

**Decision rule**:
- **Venting has no actionable request.** If the poster asks even a vague question like "what should I do?" or "what am I doing wrong?", that tips it to **advice-seeking** — even if the tone is overwhelmingly negative.
- **Rhetorical questions don't count.** Questions like "is this even worth it?" or "are we all cooked?" are emotional expressions, not genuine requests for guidance. These stay as **venting**.
- **Practical test:** Could a commenter give a useful, specific answer to the question asked? If yes → advice-seeking. If the only honest response is empathy or "hang in there" → venting.

### Secondary boundary: advice-seeking ↔ experience-sharing

Many posts tell a story AND ask a question.

**Decision rule**:
- If the post's core content is a story/outcome and the question is secondary, label it **experience-sharing**.
- If the question is the main driver and the personal details are context, label it **advice-seeking**.
- *Practical test:* Could you remove the question and the post still makes sense as a complete story? → experience-sharing. Could you remove the story and the question still makes sense? → advice-seeking.

### Tertiary boundary: showcasing ↔ advice-seeking

Project posts that ask for feedback or resume advice.

**Decision rule**:
- If the post primarily *presents* a project/resource and the question is secondary ("thoughts?", "feedback?"), label it **showcasing**.
- If the project is just context for a genuine question ("how do I deploy this?", "is this portfolio-worthy?"), label it **advice-seeking**.

## Data Collection Plan

### Sources
- **~225 standalone posts** from r/csMajors, pulled from Hot, New, and Top (past month) using PRAW (Python Reddit API Wrapper) — approximately 75 from each sort mode to get diverse content
- **~75 comments** from the [Project Showcase Megathread](https://www.reddit.com/r/csMajors/comments/1mcg0rc/project_showcase_megathread/) for the showcasing label

### Scraping approach
- Use PRAW to programmatically pull posts and megathread comments
- Total target: **~300 raw examples**, with the goal of retaining **200+ after filtering** out deleted/low-quality/off-topic posts

### CSV format
Columns: `text`, `label`, `source` (post vs. comment), `notes` (for difficult cases)

### Label distribution targets
| Label | Target % | Target count (of 200) |
|-------|----------|----------------------|
| advice-seeking | ~35-40% | 70-80 |
| experience-sharing | ~25-30% | 50-60 |
| venting | ~15-20% | 30-40 |
| showcasing | ~10-15% | 20-30 |

### Imbalance mitigation
- If showcasing falls below 20 examples, scrape additional megathread comments or search for standalone project posts
- If any single label exceeds 70%, redistribute by scraping more from underrepresented sorts/sources
- The `source` column tracks whether examples are posts vs. comments — this is a potential confounder since megathread comments (showcasing) tend to be shorter and structurally different from standalone posts

### Labeling workflow
1. Scrape ~300 raw examples using PRAW
2. Pre-label all examples using an LLM (Groq llama-3.3-70b-versatile) with the exact label definitions from this document
3. Manually review **every single pre-labeled example**, correcting labels as needed
4. Track all corrections in the `notes` column for disclosure in the AI Usage section
5. Document at least 3 genuinely difficult labeling decisions

## Evaluation Metrics

### Primary metrics
- **Overall accuracy** for both fine-tuned model and zero-shot baseline
- **Per-class F1 score** — the most informative single metric per label because it balances precision and recall. This is critical because label distribution is intentionally uneven (showcasing ~15% vs. advice-seeking ~35%), so raw accuracy alone would mask poor performance on minority classes.

### Secondary metrics
- **Precision and recall per class** — to diagnose whether the model is being conservative (high precision, low recall) or over-predicting (high recall, low precision) for each label
- **Confusion matrix** — to identify which specific label pairs the model confuses most. We expect advice-seeking ↔ venting to be the most confused pair.

### Why these metrics
Accuracy alone is insufficient because a model that always predicts "advice-seeking" would achieve ~35% accuracy simply by predicting the majority class. Per-class F1 ensures the model is genuinely distinguishing between all four intents, especially the minority classes (venting, showcasing). The confusion matrix reveals directional errors — e.g., does the model mis-label venting posts as advice-seeking, or the reverse? This informs whether the boundary rules need tightening.

## Definition of Success

- **Good enough for deployment**: Fine-tuned model achieves **overall accuracy ≥ 65%** and **per-class F1 ≥ 0.55 for all labels**, meaningfully beating the zero-shot baseline by at least 10 percentage points on overall accuracy.
- **Strong performance**: All per-class F1 scores ≥ 0.70 and overall accuracy ≥ 75%.
- **Minimum acceptable**: Fine-tuned model outperforms zero-shot baseline on at least 3 of 4 labels.

These thresholds are realistic for a subjective 4-class intent classification task with only 200 training examples. If the fine-tuned model barely beats or underperforms the baseline, that signals a label quality or annotation consistency issue worth investigating.

## AI Tool Plan

### Label stress-testing
Before annotating 200 examples, I will provide the LLM (Groq) my label definitions and edge case rules, and ask it to generate 5-10 posts that sit at the boundary between two labels (especially advice-seeking ↔ venting). If I can't classify these cleanly using my definitions, I'll tighten the definitions before committing to annotation.

### Annotation assistance
I will use Groq's llama-3.3-70b-versatile to pre-label all scraped examples by providing my exact label definitions and asking it to assign one label per post. I will then manually review and correct every pre-assigned label. I will track which examples I overrode in the `notes` column and disclose this workflow in the AI Usage section of the README.

### Failure analysis
After evaluation, I will paste my misclassified examples into an LLM and ask it to identify patterns — common post length, sarcasm, specific label pairs, etc. I will verify those patterns by re-reading the examples myself and include findings in the evaluation report.
