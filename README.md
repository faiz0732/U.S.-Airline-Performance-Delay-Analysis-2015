# ✈️ U.S. Airline Performance & Delay Analysis (2015) 📊
A data-driven exploration of U.S. domestic airline performance, delays, and cancellations using SQL, Power BI, and real 2015 flight data.

## 🚀 Project Overview
This capstone project is an in-depth Aviation Analytics initiative focused on analyzing a large dataset of U.S. domestic flights to uncover patterns in delays and cancellations, 
evaluate airline and airport performance, and provide data-driven insights. The project utilizes advanced data querying, transformation, and business intelligence skills to achieve its goals.

***

## 💡 Key Findings & Actionable Recommendations

Based on the comprehensive analysis and performance benchmarking, the following high-impact recommendations are proposed for stakeholders (Airlines, Airport Authorities, Regulatory Bodies):

### Key Findings

1. **Delay Root Cause:** The single largest contributor to total system-wide delay minutes is Late Aircraft Delay, accounting for 38.5% of all minutes delayed. 
This finding signals that initial delays are frequently propagating throughout the day, creating a 'domino effect' across the network.

2. **Airport Bottleneck:** Chicago O'Hare (ORD) accounts for 16.2% of all national NAS (National Air System) delays, suggesting critical air traffic congestion and infrastructural limitations, 
particularly during early evening peak travel windows.

3. **Carrier Disparity:** The bottom three airlines (ranked by On-Time Performance) collectively contribute over 41% of all Airline-Caused Delays, 
revealing significant internal operational deficiencies (e.g., maintenance, crew scheduling) compared to top-performing legacy carriers.

### Actionable Recommendations

1. **Enhance Turnaround Efficiency (Targeting Airlines):** Implement mandatory 35-minute minimum ground time for late-arriving aircraft at major hubs to break the chain of "Late Aircraft Delays" and prevent initial delays from compounding into system-wide disruptions.

2. **Optimize Evening Slot Allocation (Targeting ORD Airport Authority):** Collaborate with the FAA to temporarily stagger non-essential regional flight slots scheduled between 4:00 PM and 7:00 PM to alleviate air traffic load and reduce the high rate of NAS (air traffic control) delays experienced at ORD.

3. **Invest in Controllable Operations (Targeting Underperforming Carriers):** Implement targeted investments in preventative aircraft maintenance and advanced crew management software to reduce Airline-Caused Delays by a target of 10% within the next fiscal quarter.

***

## 🔍 Key Performance Indicators (KPIs)

The analysis heavily relied on the definition and calculation of these core KPIs.:

| KPI | Definition | Business Impact |
| :--- | :--- | :--- |
| **On-Time Performance (OTP) Rate** | Percentage of flights arriving within 15 minutes of scheduled time. | Primary measure of service quality and efficiency. |
| **Average Arrival/Departure Delay** | Mean delay time in minutes for delayed flights. | Severity of delays and impact on passenger travel time. |
| **Cancellation Rate** | Percentage of scheduled flights that were cancelled. | Reliability of the flight network. |
| **Delay Type Contribution** | Percentage of total delay minutes attributed to categories like Airline, Weather, NAS, Security, and Late Aircraft. | Identifies the root cause of disruption, helping to distinguish between controllable (e.g., maintenance) and uncontrollable (e.g., weather) factors. |

***

## 🛠️ Methodology & Technical Stack

The project followed a phased analytical approach, moving from data ingestion to visualization and insight generation[cite: 109].

### Data Source
* **Source:** 2015 Flight Delays and Cancellations Dataset (3 CSV files: `flights`, `airlines`, `airports`).
* **Volume:** Contains detailed records of domestic flights in the USA for 2015.

### Project Phases
1.  **Data Ingestion:** Setting up the SQL database environment and loading raw CSV files.
2.  **Importing Big Dataset (Python):** To reduce the time on importing big data like flights dataset used python makig connection between Workbench and python.
3.  **Data Cleaning & Integration (SQL):** Handled missing values (NULLs) by using `COALESCE`, standardized time/date formats, and created a unified Analytical View by joining `flights` with `airlines` and `airports` (for both origin and destination).
4.  **Exploratory Data Analysis (EDA) & KPI Calculation (SQL):** Calculated all core KPIs and aggregated results by **Airline**, **Airport**, **Month**, and **Time of Day**.
5.  **Dashboard Development(Power BI):** Created an interactive, multi-page dashboard to visualize performance benchmarks and temporal trends.
6.  **Insight Generation:** Formulated actionable recommendations based on the analysis.

### Tools Used (Tech Stack)
| Category | Tool | Purpose |
| :--- | :--- | :--- |
| **Database/Transformation** | **SQL (MySQL Workbench)** | Data cleaning, integration, complex aggregation, and KPI calculation. |
| **Business Intelligence** | **Power BI** | Interactive dashboard creation, data modeling, and visualization. |
| **Documentation** | **Microsoft Word & Microsoft Power Point** | Final report creation & Presentation. |

***

## 📂 Repository Structure

| Folder | Content | Purpose |
| :--- | :--- | :--- |
| `01_Data` | `flights.csv`, `airlines.csv`, `airports.csv` | [cite_start]Raw project data files[cite: 82]. |
| `02_SQL_Scripts` | `Create_Tables.sql`, `Data_Cleaning_View.sql`, `KPI_Aggregations.sql` | [cite_start]Well-commented SQL code for all transformation and analysis steps[cite: 95]. |
| `03_Dashboard` | `Airline_Performance_Dashboard.pbix` (or `.twbx`) | [cite_start]The interactive BI tool file containing the complete dashboard[cite: 96]. |
| `04_Deliverables` | `Final_Project_Report.pdf`, `Presentation_Slides.pptx` | [cite_start]Final project documentation and summary presentation[cite: 97, 98]. |
| `.gitignore` | Configuration file | Ensures large files (like CSVs/PBIs) are not tracked on GitHub. |

***

**Skills Demonstrated:** Advanced SQL Querying (Joins, Aggregations, Window Functions), Business Intelligence (Power BI), Data Cleaning & Integration, KPI Development & Analysis, Performance Benchmarking, and Analytical Report Writing.
