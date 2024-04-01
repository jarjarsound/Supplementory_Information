import pandas as pd
import plotly.graph_objects as go
import argparse

class SankeyDiagram:
    def __init__(self):
        self.node_names = {}
        self.current_index = 0
        self.sources = []
        self.targets = []
        self.values = []

    def add_node(self, name):
        if name not in self.node_names:
            self.node_names[name] = self.current_index
            self.current_index += 1
        return self.node_names[name]

    def add_flow(self, source, target, value):
        source_index = self.add_node(source)
        target_index = self.add_node(target)
        self.sources.append(source_index)
        self.targets.append(target_index)
        self.values.append(value)

    def generate_figure(self):
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(self.node_names.keys()),
            ),
            link=dict(
                source=self.sources,
                target=self.targets,
                value=self.values,
            ))])
        return fig

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Generate a Sankey diagram from a tab-delimited input file.')
parser.add_argument('input_file', type=str, help='Path to the tab-delimited input file')
args = parser.parse_args()

# Load the data
df = pd.read_csv(args.input_file, sep='\t')

# Initialize the Sankey diagram object
sankey = SankeyDiagram()

# Add Phylum to EET-gene flows
for _, row in df.groupby(['Phylum', 'EET-gene'])['Normalised relative abundance (%)'].sum().reset_index().iterrows():
    sankey.add_flow(row['Phylum'], row['EET-gene'], row['Normalised relative abundance (%)'])

# Add EET-gene to Type flows
for _, row in df.groupby(['EET-gene', 'Type'])['Normalised relative abundance (%)'].sum().reset_index().iterrows():
    sankey.add_flow(row['EET-gene'], row['Type'], row['Normalised relative abundance (%)'])

# Generate and show the figure
fig = sankey.generate_figure()
fig.update_layout(title_text="Sankey Diagram of Phylum, EET-gene, and Type", font_size=10)
fig.show()
