"""Create a sample evaluation dataset CSV."""

import pandas as pd
from pathlib import Path

def create_sample_dataset():
    """Create a sample evaluation dataset."""
    
    data = {
        'question': [
            'What is diabetes?',
            'What are the symptoms of hypertension?',
            'How is cardiovascular disease prevented?',
            'What are the risk factors for diabetes?',
            'What is the treatment for hypertension?'
        ],
        'reference_answer': [
            'Diabetes is a chronic metabolic disorder characterized by high blood sugar levels. There are two main types: Type 1 (autoimmune) and Type 2 (insulin resistance).',
            'Hypertension symptoms may include headaches, shortness of breath, nosebleeds, but often has no symptoms. It is defined as blood pressure above 140/90 mmHg.',
            'Cardiovascular disease prevention includes regular exercise, healthy diet, smoking cessation, weight management, and regular health screenings.',
            'Risk factors for diabetes include age, family history, obesity, lack of physical activity, and high blood pressure.',
            'Hypertension treatment includes lifestyle modifications (diet, exercise) and medications such as ACE inhibitors, beta-blockers, diuretics, and calcium channel blockers.'
        ]
    }
    
    df = pd.DataFrame(data)
    output_path = Path("data/evaluation_dataset.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✅ Created sample evaluation dataset: {output_path}")
    print(f"   Contains {len(df)} question-answer pairs")
    
    return output_path

if __name__ == "__main__":
    create_sample_dataset()




