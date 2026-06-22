import os
import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Change this to your Hugging Face Model ID once uploaded
MODEL_ID = "your-hf-username/takemeter-model"
LOCAL_MODEL_DIR = "./takemeter-model"

import glob

def load_model():
    model_path = MODEL_ID
    
    # Prioritize local directory if it exists
    if os.path.exists(LOCAL_MODEL_DIR):
        model_path = LOCAL_MODEL_DIR
        if not os.path.exists(os.path.join(LOCAL_MODEL_DIR, "config.json")):
            checkpoints = glob.glob(os.path.join(LOCAL_MODEL_DIR, "checkpoint-*"))
            if checkpoints:
                checkpoints.sort(key=lambda x: int(x.split("-")[-1]))
                model_path = checkpoints[-1]
                print(f"Local model config not found in root, using checkpoint: {model_path}")
            else:
                print(f"No config.json or checkpoint folders found in {LOCAL_MODEL_DIR}")
    
    print(f"Loading model from: {model_path}")
    try:
        # Load the base tokenizer since the Colab training script didn't save it locally
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

tokenizer, model = load_model()

def classify_text(text):
    if model is None or tokenizer is None:
        return {"Error": 1.0}
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    
    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Get probabilities
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1).squeeze().tolist()
    
    # Map to labels
    labels = model.config.id2label
    result = {labels[i]: prob for i, prob in enumerate(probs)}
    
    return result

# Define example posts from the evaluation report
examples = [
    ["Hey guys, I made a job matching email digest service. Scrapes jobs, matches you to those you meet 60 percent or more requirements for, and gives you feedback on skill-building. Completely free! Sign up here: [https://forms.gle/kcP2pbJfgZ7pXBtR7](https://forms.gle/kcP2pbJfgZ7pXBtR7)"],
    ["Graduating CS student, no tech experience. Where do I even start?"],
    ["Notion Virtual Onsite - I have a call with notion for a new grad role. They mention that there is a 2hr virtual onsite, specifically one of the interview is a debugging one. Anyone done this before? Looking for some advice on how to best prepare for it. Thanks!"],
    ["Got the invitation to Amazon OA while on holiday abroad, no laptop with me. Timing couldnâ€™t be worse. Havenâ€™t heard back from a load of applications, decide not to apply anywhere the past week since I was heading abroad, Amazon sends an email one day in asking for the OA to be completed no later than a week after the email. Misery."]
]

# Check if model exists to display appropriate UI
if model is None:
    # Fallback UI if model is missing
    with gr.Blocks() as iface:
        gr.Markdown("# ⚠️ Model Not Found")
        gr.Markdown(f"The fine-tuned DistilBERT model could not be loaded.")
        gr.Markdown("Please ensure you have either set `MODEL_ID` in `app.py` to your uploaded Hugging Face model repository (e.g. `your-username/takemeter-model`), or that the local `./takemeter-model` folder is present.")
else:
    # Main UI
    iface = gr.Interface(
        fn=classify_text,
        inputs=gr.Textbox(
            lines=5, 
            placeholder="Paste a Reddit post from r/csMajors here...",
            label="Post Text"
        ),
        outputs=gr.Label(num_top_classes=4, label="Predicted Intent & Confidence"),
        title="TakeMeter: Post Intent Classifier",
        description="A fine-tuned DistilBERT model that classifies r/csMajors discourse into four categories: `advice-seeking`, `experience-sharing`, `venting`, and `showcasing`.",
        examples=examples,
        flagging_mode="never"
    )

if __name__ == "__main__":
    iface.launch(share=False)
