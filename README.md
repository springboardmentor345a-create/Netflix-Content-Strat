
# 📊 Content Analysis using EDA (Python Project)

## 📌 Project Overview

This project focuses on analyzing a content dataset using **Exploratory Data Analysis (EDA)** techniques in Python. The analysis is performed step-by-step across multiple notebooks (Week 1–6), covering data cleaning, preprocessing, visualization, and insight generation.

The goal is to understand patterns such as **content origin (Original vs Licensed)**, distribution, and trends using clear visualizations.

---

## 🎯 Objectives

* Clean and preprocess raw dataset
* Handle missing values and inconsistencies
* Analyze content categories and distribution
* Compare **Original vs Licensed content**
* Generate meaningful insights using visualizations

---

## 🧹 Data Preprocessing

* Removed null/missing values
* Cleaned column names and formats
* Converted data types where required
* Filtered and structured dataset for analysis

---

## 📊 Exploratory Data Analysis (EDA)

### 🔍 Key Analysis Performed

* Distribution of content across categories
* Count of **Original vs Licensed content**
* Frequency analysis using countplots
* Pattern identification through visualizations

---

## 📈 Sample Visualization

```python
plt.figure(figsize=(6,4))
sns.countplot(data=df, x='content_origin', palette='Set2')
plt.title("Original vs Licensed Content")
plt.show()
```

This visualization helps compare the number of original and licensed content items.

---

## 🛠️ Technologies Used

| Tool             | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Data analysis                |
| Pandas           | Data cleaning & manipulation |
| Matplotlib       | Basic visualization          |
| Seaborn          | Advanced visualization       |
| Jupyter Notebook | Development environment      |

---

## 📂 Project Structure

```bash
Content-Analysis-EDA/
│── Week 1.ipynb   # Data loading & basic exploration
│── Week 2.ipynb   # Data cleaning & preprocessing
│── Week 3 & 4.ipynb  # EDA & visualizations
│── Week 5 & 6.ipynb  # Advanced analysis & insights
│── dataset.csv
```

---

## 🚀 How to Run

1. Install required libraries

   ```bash
   pip install pandas matplotlib seaborn
   ```

2. Open Jupyter Notebook

   ```bash
   jupyter notebook
   ```

3. Run notebooks step-by-step from Week 1 to Week 6

---

## 📌 Key Insights

* Clear difference between **Original and Licensed content distribution**
* Identification of dominant content categories
* Trends observed through visual analysis

---

## 📌 Use Cases

* 📊 Data Analytics Learning
* 🎓 Academic Projects
* 💼 Portfolio Projects
* 📈 Business Insights

---

## 🔮 Future Improvements

* Build interactive dashboard (Power BI / Streamlit)
* Add machine learning models
* Perform deeper statistical analysis

---

## 👤 Author

**Muppala Charan Kumar**
📍 India
🎓 Data Analytics / Computer Science

---

## ⭐ Feedback

If you found this project helpful:

* ⭐ Star the repository
* 💬 Share your feedback

---
