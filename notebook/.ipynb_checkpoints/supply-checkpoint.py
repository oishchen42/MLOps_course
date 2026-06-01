import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def save_project_plot(filename: str):
    """
    Automatically routes and saves a matplotlib plot to the 
    project's root 'diagrams' folder.
    """
    # 1. Map the path to the diagrams folder
    project_root = Path.cwd().parent
    diagrams_dir = project_root / "diagrams"
    
    # 2. Ensure the folder exists
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. Create the exact file path
    file_path = diagrams_dir / filename
    
    # 4. Save with tight bounding box for a clean look
    plt.savefig(file_path, bbox_inches="tight", dpi=300)
    print(f" Successfully saved: {filename} in {diagrams_dir}")

def plot_detailed_gender_survival(df):
    """Generates a 2x2 grid: Top row stacked survival, Bottom row isolated perished with numeric labels."""
    # Establish the 20 distinct columns from 0 to 100 years
    bins = np.linspace(0, 100, 21)

    # Isolate the gender groups
    male_df = df[df['sex'] == 1]
    female_df = df[df['sex'] == 0]

    # Split each gender into Survived (1) and Perished (0) age arrays
    male_died = male_df[male_df['survived'] == 0]['age'].dropna()
    male_survived = male_df[male_df['survived'] == 1]['age'].dropna()
    female_died = female_df[female_df['survived'] == 0]['age'].dropna()
    female_survived = female_df[female_df['survived'] == 1]['age'].dropna()

    # Compute weight vectors
    mw_died = np.ones_like(male_died) * 100.0 / len(male_df)
    mw_surv = np.ones_like(male_survived) * 100.0 / len(male_df)
    fw_died = np.ones_like(female_died) * 100.0 / len(female_df)
    fw_surv = np.ones_like(female_survived) * 100.0 / len(female_df)

    # Initialize a 2x2 grid
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
    colors = ['#c94c4c', '#6ab04c']
    labels = ['Perished', 'Survived']
    
    # Top-Left: Male Stacked
    ax[0, 0].hist([male_died, male_survived], bins=bins, weights=[mw_died, mw_surv], 
                  stacked=True, color=colors, edgecolor='black', alpha=0.85, label=labels)
    ax[0, 0].set_title("Male Cohort: Survival by Age Group", fontsize=13, fontweight='bold', pad=12)
    ax[0, 0].set_ylabel("Percentage of Gender Cohort (%)", fontsize=11)
    
    # Top-Right: Female Stacked
    ax[0, 1].hist([female_died, female_survived], bins=bins, weights=[fw_died, fw_surv], 
                  stacked=True, color=colors, edgecolor='black', alpha=0.85, label=labels)
    ax[0, 1].set_title("Female Cohort: Survival by Age Group", fontsize=13, fontweight='bold', pad=12)

    _, _, patches_md = ax[1, 0].hist(male_died, bins=bins, weights=mw_died, 
                                     color='#c94c4c', edgecolor='black', alpha=0.85)
    ax[1, 0].set_title("Male Cohort: Perished (Isolated)", fontsize=13, fontweight='bold', pad=12)
    ax[1, 0].set_xlabel("Age Groups (5-Year Bins)", fontsize=11)
    ax[1, 0].set_ylabel("Percentage of Gender Cohort (%)", fontsize=11)

    for p in patches_md:
        height = p.get_height()
        if height > 0:
            ax[1, 0].text(p.get_x() + p.get_width() / 2, height + 0.3, f"{height:.1f}%", 
                          ha='center', va='bottom', fontsize=9, fontweight='bold')

    _, _, patches_fd = ax[1, 1].hist(female_died, bins=bins, weights=fw_died, 
                                     color='#c94c4c', edgecolor='black', alpha=0.85)
    ax[1, 1].set_title("Female Cohort: Perished (Isolated)", fontsize=13, fontweight='bold', pad=12)
    ax[1, 1].set_xlabel("Age Groups (5-Year Bins)", fontsize=11)

    for i in range(2):
        for j in range(2):
            ax[i, j].set_xlim(0, 100)
            ax[i, j].set_xticks(np.arange(0, 101, 10))
            ax[i, j].grid(axis='y', linestyle='--', alpha=0.5)
            # Only add the legend to the top row
            if i == 0:
                ax[i, j].legend(loc='upper right')
    plt.tight_layout()
    save_project_plot("detailed_gender_survival_distribution.png")