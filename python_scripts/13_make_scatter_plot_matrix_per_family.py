import plotly.express as px
import pandas as pd
import sys

dataset = pd.read_csv(sys.argv[1])
data_categorized = pd.read_csv(sys.argv[2])
name_output = sys.argv[3]

df = pd.merge(dataset, data_categorized, on="sequence")

fig = px.scatter_matrix(df, dimensions=["length", "inhibition_IC50", "hydrophobic_profile", "hydrophobicity_profile", "hydrophobic_ratio", "aliphatic_index", "aromaticity", "molecular_weigth", "charge", "charge_density", "isoelectric", "inestability"], color="domain")

fig.update_layout(
    title='Scatter Plot Matrix',    
    width=2100,
    height=2100        
)

fig.write_image(name_output)
