# group3_project_wikipedia
This is the repository for Group 3's Wikipedia project.

## Running the Project Locally

To get the project up and running, follow the steps below:

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/rsstudentie/group3_project_wikipedia.git
```

### Step 2: Install Required Dependencies

Navigate into the project directory:

```bash
cd group3_project_wikipedia
```

Install the project dependencies:

```bash
poetry install
```

### Step 3: Start Project Locally

Start the project:

```bash
poetry shell
streamlit run wikipedia/main.py
```

The project will be available at `http://localhost:8501/`.

## Additional Information

To Reinitialize the database, run the following command:

```bash
python ./wikipedia/main.py initdb
```

To download the data from Kaggle, run the following command:

```bash
python ./wikipedia/main.py kaggledownload
```

To sample the data, run the following command:

```bash
python ./wikipedia/main.py sampledata
```

To get the number of rows in the database, run the following command:

```bash
python ./wikipedia/main.py getrows [ "working" | "complete"  ]
```



## Contributing

To contribute to this project, follow the steps outlined below:

### Step 1: Clone the Repository

Clone the repository to your local machine. Open a terminal and run the following command:

```bash
    git clone https://github.com/rsstudentie/group3_project_wikipedia.git
```

### Step 2: Create a Branch
Create a new branch to work on your feature or bug fix. Use a descriptive name for your branch that reflects the purpose of your changes:

```bash
git checkout -b feature/your-feature-name
```

### Step 3: Make Changes
Make your desired changes to the codebase. Ensure that your changes adhere to the project's coding conventions and guidelines.

### Step 4: Commit Your Changes
Once you have made your changes, commit them to your local repository with a descriptive commit message:

```bash
git add .
git commit -m "Add your descriptive commit message here"
```

Step 5: Push Changes
Push your changes to the repository on GitHub:

```bash
git push origin feature/your-feature-name
```

### Step 6: Create a Pull Request (PR)
Go to the GitHub page of the original repository. You should see a 'Compare & pull request' button for the branch you just pushed. Click on that button to start creating a pull request.

In the pull request description, provide a clear explanation of the changes you have made. Make sure to reference any related issues or pull requests.

### Step 7: Review and Collaborate
Once your pull request is submitted, project maintainers will review your changes. Be prepared to address any feedback or concerns they may have. Collaboration and iteration are key to the success of the project.

### Step 8: Keep Your Local Repository Updated
Periodically, you may want to fetch and merge changes from the original repository to keep your local repository up-to-date:

```bash
git checkout main
git pull origin main
```

Code of Conduct
Please note that this project is governed by our Code of Conduct. Contributors are expected to adhere to its guidelines in all project-related spaces.
