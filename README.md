# README – FSAE Design Challenge (Windows)

Setup
1. Open Command Prompt or PowerShell inside the project folder.
2. Install dependencies:
   pip install -r requirements.txt
   (Works with either a virtual environment `.venv` or your global Python installation.)

Step 1: Generate Data
Create a simulated dataset by running:

   python src\generate_data.py --out data\session.csv
   
This saves `session.csv` inside the `data\` folder.

Step 2: Visualize
Generate plots from the dataset:
   python src\visualize.py --infile data\session.csv
This will display the plots (including the slip heatmap).

To also save the figures into a folder:
   python src\visualize.py --infile data\session.csv --savefig out_plots

Outputs
- data\session.csv
- Plots → brake pressure, wheel speeds, slip heatmap, bias, pressure vs decel
