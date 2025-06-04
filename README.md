## Read Me

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

In the activatet env insert:

`pip install streamlit-bokeh`

5. Run the Streamlit App

To start the Streamlit app, run the following command inside the project directory:

`streamlit run src/main.py`

--> This will launch the app in your browser! 





More information about the env: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) :
 
 
 