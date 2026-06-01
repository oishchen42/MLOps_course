import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

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


def plot_detailed_socioeconomic_survival(df):
    """Generates a 2x2 grid: Top row stacked survival, Bottom row isolated perished by ticket class."""
    
    # 1. Safely create the ticket class column
    df = df.copy() 
    df['ticket_class'] = np.where(df['1st_class'] == 1, '1st Class', 
                           np.where(df['2nd_class'] == 1, '2nd Class', '3rd Class'))

    # 2. Setup the 2x2 canvas
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
    classes = ['1st Class', '2nd Class', '3rd Class']
    x_positions = np.arange(len(classes))
    colors = ['#c94c4c', '#6ab04c'] 
    
    # 3. Loop through genders (1 = Male, 0 = Female)
    genders = [(1, "Male Cohort"), (0, "Female Cohort")]
    
    for col, (sex_code, title) in enumerate(genders):
        gender_df = df[df['sex'] == sex_code]
        
        # Calculate percentages
        counts = pd.crosstab(gender_df['ticket_class'], gender_df['survived'])
        pct = (counts.reindex(classes, fill_value=0) / len(gender_df)) * 100
        
        perished = pct.get(0, pd.Series(0, index=classes))
        survived = pct.get(1, pd.Series(0, index=classes))
        
        # --- ROW 1: STACKED OVERVIEW ---
        ax[0, col].bar(x_positions, perished, color=colors[0], edgecolor='black', label='Perished')
        ax[0, col].bar(x_positions, survived, bottom=perished, color=colors[1], edgecolor='black', label='Survived')
        ax[0, col].set_title(f"{title}: Survival by Ticket Class", fontsize=13, fontweight='bold', pad=12)
        
        # --- ROW 2: ISOLATED PERISHED ---
        bars = ax[1, col].bar(x_positions, perished, color=colors[0], edgecolor='black')
        ax[1, col].set_title(f"{title}: Perished (Isolated)", fontsize=13, fontweight='bold', pad=12)
        
        # Append exact percentage labels on the isolated bars
        for p in bars:
            height = p.get_height()
            if height > 0:
                ax[1, col].text(p.get_x() + p.get_width() / 2, height + 1.0, f"{height:.1f}%", 
                                ha='center', va='bottom', fontsize=10, fontweight='bold')

        # --- FORMATTING (Applies to both rows in this column) ---
        for row in range(2):
            ax[row, col].set_xticks(x_positions)
            ax[row, col].set_xticklabels(classes, fontsize=11, fontweight='bold')
            ax[row, col].grid(axis='y', linestyle='--', alpha=0.5)

    # Global labels and saving
    ax[0, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[1, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[0, 0].legend(loc='upper left')
    ax[0, 1].legend(loc='upper left')
    
    plt.tight_layout()
    save_project_plot("detailed_socioeconomic_survival.png")

def plot_detailed_family_size_survival(df):
    """Generates a 2x2 grid: Top row stacked survival, Bottom row isolated perished by family size."""
    
    # 1. Setup the 2x2 canvas
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
    all_family_sizes = sorted(df['family_size'].unique())
    x_positions = np.arange(len(all_family_sizes))
    colors = ['#c94c4c', '#6ab04c'] 
    
    # 2. Loop through genders
    genders = [(1, "Male Cohort"), (0, "Female Cohort")]
    
    for col, (sex_code, title) in enumerate(genders):
        gender_df = df[df['sex'] == sex_code]
        
        # Calculate percentages
        counts = pd.crosstab(gender_df['family_size'], gender_df['survived'])
        pct = (counts.reindex(all_family_sizes, fill_value=0) / len(gender_df)) * 100
        
        perished = pct.get(0, pd.Series(0, index=all_family_sizes))
        survived = pct.get(1, pd.Series(0, index=all_family_sizes))
        
        # --- ROW 1: STACKED OVERVIEW ---
        ax[0, col].bar(x_positions, perished, color=colors[0], edgecolor='black', label='Perished')
        ax[0, col].bar(x_positions, survived, bottom=perished, color=colors[1], edgecolor='black', label='Survived')
        ax[0, col].set_title(f"{title}: Survival by Family Size", fontsize=13, fontweight='bold', pad=12)
        
        # --- ROW 2: ISOLATED PERISHED ---
        bars = ax[1, col].bar(x_positions, perished, color=colors[0], edgecolor='black')
        ax[1, col].set_title(f"{title}: Perished (Isolated)", fontsize=13, fontweight='bold', pad=12)
        ax[1, col].set_xlabel("Family Size (Accompanying Relatives)", fontsize=11)
        
        # Append exact percentage labels on the isolated bars
        for p in bars:
            height = p.get_height()
            if height > 0:
                ax[1, col].text(p.get_x() + p.get_width() / 2, height + 0.5, f"{height:.1f}%", 
                                ha='center', va='bottom', fontsize=9, fontweight='bold')

        # --- FORMATTING (Applies to both rows in this column) ---
        for row in range(2):
            ax[row, col].set_xticks(x_positions)
            ax[row, col].set_xticklabels(all_family_sizes)
            ax[row, col].grid(axis='y', linestyle='--', alpha=0.5)

    # Global labels and saving
    ax[0, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[1, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[0, 0].legend(loc='upper right')
    ax[0, 1].legend(loc='upper right')
    
    plt.tight_layout()
    save_project_plot("detailed_family_size_survival.png")

def plot_detailed_fare_survival(df):
    """Generates a 2x2 grid: Top row stacked survival, Bottom row isolated perished by ticket fare."""
    
    # 1. Safely copy and clip the fare
    df = df.copy()
    df['fare_clipped'] = df['fare'].clip(upper=150)
    
    # 2. Setup the 2x2 canvas and global definitions
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
    bins = np.linspace(0, 150, 16) # 15 bins of $10 each
    colors = ['#c94c4c', '#6ab04c']
    labels = ['Perished', 'Survived']
    
    # 3. Loop through genders
    genders = [(1, "Male Cohort"), (0, "Female Cohort")]
    
    for col, (sex_code, title) in enumerate(genders):
        gender_df = df[df['sex'] == sex_code]
        
        # Split survival arrays and drop missing values safely
        died = gender_df[gender_df['survived'] == 0]['fare_clipped'].dropna()
        survived = gender_df[gender_df['survived'] == 1]['fare_clipped'].dropna()
        
        # Compute weight vectors
        w_died = np.ones_like(died) * 100.0 / len(gender_df)
        w_surv = np.ones_like(survived) * 100.0 / len(gender_df)
        
        # --- ROW 1: STACKED OVERVIEW ---
        ax[0, col].hist([died, survived], bins=bins, weights=[w_died, w_surv], 
                        stacked=True, color=colors, edgecolor='black', alpha=0.85, label=labels)
        ax[0, col].set_title(f"{title}: Survival by Ticket Fare", fontsize=13, fontweight='bold', pad=12)
        
        # --- ROW 2: ISOLATED PERISHED ---
        _, _, patches = ax[1, col].hist(died, bins=bins, weights=w_died, 
                                        color=colors[0], edgecolor='black', alpha=0.85)
        ax[1, col].set_title(f"{title}: Perished (Isolated)", fontsize=13, fontweight='bold', pad=12)
        ax[1, col].set_xlabel("Ticket Price ($10 Increments, max clipped at $150+)", fontsize=11)
        
        # Append exact percentage labels on the isolated bars
        for p in patches:
            height = p.get_height()
            if height > 0:
                ax[1, col].text(p.get_x() + p.get_width() / 2, height + 0.3, f"{height:.1f}%", 
                                ha='center', va='bottom', fontsize=9, fontweight='bold')

        # --- FORMATTING (Applies to both rows in this column) ---
        for row in range(2):
            ax[row, col].set_xlim(0, 150)
            ax[row, col].set_xticks(np.arange(0, 151, 30))
            ax[row, col].grid(axis='y', linestyle='--', alpha=0.5)

    # Global labels and saving
    ax[0, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[1, 0].set_ylabel("Percentage of Total Gender Cohort (%)", fontsize=11)
    ax[0, 0].legend(loc='upper right')
    ax[0, 1].legend(loc='upper right')
    
    plt.tight_layout()
    save_project_plot("detailed_fare_survival_distribution.png")