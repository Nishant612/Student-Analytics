# Student Success & Placement Analytics

A complete business-analytics workflow for the **Engineering Student Journey** dataset. The project cleans student records, explores academic and placement performance, calculates business KPIs, generates visualizations, and optionally exports the prepared data to MySQL.

## Dataset

### Local source

- Dataset: `data/engineering_student_journey.csv`
- Cleaned output: `data/cleaned_student_data.csv`
- The local CSV is the authoritative source used by this project.

### External dataset link

The repository does not contain a verified original source URL. The following Kaggle search page can be used to locate the published dataset or its official source:

- **Kaggle dataset search:** https://www.kaggle.com/datasets?search=engineering+student+journey

Before using an external file, confirm its source, publication date, license, and field definitions. The analysis assumes the following business fields:

- Student identifier and name
- Age, gender, branch
- Average GPA and semester GPAs
- Backlogs and attendance
- Clubs and skills
- Internship participation and domain
- Placement status and placement domain
- CTC and alumni path

## Business objective

The application supports decisions about student success, academic support, career readiness, campus placement, and program planning. It is designed for business analytics teams, academic administrators, placement officers, and student-success managers.

### Business questions

1. What percentage of students are placed?
2. How does academic performance vary between placed and not-placed students?
3. Is attendance associated with academic performance or placement?
4. Which branches produce the strongest placement outcomes?
5. How many students participate in internships?
6. Which student skills, clubs, or domains appear most often in placement records?
7. Which variables may indicate a risk of poor academic or career outcomes?

## Application workflow

### 1. Data ingestion

The notebook reads the local CSV into a pandas DataFrame and reports dimensions, column names, data types, missing values, and duplicate records.

### 2. Data cleaning

The cleaning stage:

- Normalizes column names to lowercase snake case.
- Removes leading and trailing whitespace.
- Collapses repeated whitespace.
- Removes exact duplicate rows.
- Fills numeric missing values with medians.
- Fills categorical missing values with the mode.
- Converts numeric-like columns when at least 90% of values are numeric.
- Saves the cleaned result as a CSV.

The use of medians and modes is intentional because these methods are less sensitive to outliers than means and preserve the distribution of the source data better.

### 3. Exploratory analysis

The notebook uses pandas, Matplotlib, and Seaborn to inspect:

- Placement distribution
- Correlation matrix among numeric variables
- Academic and attendance distributions
- GPA differences by placement status
- Branch placement rates
- Attendance versus GPA
- Potential numeric outliers
- Categorical distributions

Plotted outputs are saved in the `outputs/` folder.

### 4. Business KPI calculation

The notebook calculates:

- Total students
- Placed and not-placed students
- Placement rate
- Average and median GPA
- Average attendance
- Internship participation rate
- Branch-level placement rate, average GPA, and average attendance

These values are exported as:

- `outputs/business_kpis.json`
- `outputs/branch_performance.csv`
- `outputs/executive_summary.json`

### 5. MySQL export

The optional MySQL export creates a `students` table and inserts the cleaned records. It requires these environment variables:

```dotenv
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

The export can be enabled by uncommenting the final cell call. It uses a table creation statement and transactional inserts, but it does not automatically overwrite an existing table.

## Single-file notebook

The complete implementation is contained in:

- `student_analytics.ipynb`

The notebook includes all code required for the project. It can be opened in VS Code through the Jupyter extension and run cell by cell or with the notebook toolbar.

## Project structure

```text
.
├── README.md
├── student_analytics.ipynb
├── requirements.txt
├── data/
│   ├── engineering_student_journey.csv
│   └── cleaned_student_data.csv
└── outputs/
```

## Setup

1. Create and activate the project virtual environment.
2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Open `student_analytics.ipynb` in VS Code.
4. Select the project's Python environment as the Jupyter kernel.
5. Run the notebook cells in order.

For Windows PowerShell, the environment can be activated with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Suggested interpretation and limitations

- Placement status is a descriptive outcome and should not be treated as proof of causation.
- Correlation does not establish that one variable causes another.
- The dataset may contain synthetic or anonymized student information; verify the privacy policy before sharing reports.
- Claims about branch performance should be made only after checking the number of students in each branch.
- Missing values are imputed for analysis, but the imputation method should be documented before publishing conclusions.
- Student names and identifiers should not be exposed in business dashboards unless they are necessary and authorized.

## Business recommendations

- Use placement rate as a high-level outcome metric.
- Compare average GPA, attendance, internships, and branch size before interpreting placement rates.
- Identify students with low attendance or academic performance and offer timely support.
- Use branch-level results to improve curriculum, mentoring, and placement preparation.
- Track the same KPIs over multiple semesters to detect trends rather than relying on one snapshot.
- Review the onboarding and internship process for branches with lower placement rates.
