## Read Me

### Repository
This repository serves as the central storage location for all documents related to this project.
All files have been organized and archived here to ensure transparency. 
https://github.com/plospen1/Project_PODSV.git


### Overview  

This project contains three folders:
- Data: All the data needed for the visualizations
- Documents: The personas, the concept and the data report
- src:
  main.py: Streamlit app with plots and text
  utils.py: Data cleaning utilities
  data_visualisation.ipynb: **NOT IMPORTANT**. First draft before we used streamlit. We decided not to delete it since we mainly worked in this file early on, so the commit history remains understandable.
  - plots( folder): these are the methods for the plots we used in the main.py. 
    dataset1_plots.py
    dataset2_plots.py
    dataset3_plots.py

### How to Set Up and Run the Streamlit App


1. Navigate to the Project Folder

Open your terminal and move into the project's root directory. For example:

cd /Users/xenia/Documents/studium/SS25/PODSV/Project_PODSV

2. Create the Conda Environment

Use the provided environment.yml file to create a new Conda environment:
`conda env create -f environment.yml`

3. Activate the Environment

Once the environment is created, activate it using:

`conda activate PODSV_Project`

4. Install Additional Packages:
Because streamlit-bokeh can not be installed with anaconda, we have to install it with pip.

In the activated env insert:

`pip install streamlit-bokeh`

5. Run the Streamlit App

To start the Streamlit app, run the following command inside the project directory:

`streamlit run src/main.py`

--> This will launch the app in your browser! 


More information about the env: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
 
 
Note: AI (OpenAi, 2025) was used as support for code and text. 
