import pandas as pd
import matplotlib.pyplot as plt

hr_personal = pd.read_csv('employee_personal_data.csv')
hr_company = pd.read_csv('employee_job_data.csv')

pd.set_option('display.max_columns', None)


print(hr_personal)
print('_______________________________')
print(hr_company)


def tratareNAN_numerice(df, coloane):

    medieCol = df[coloane].mean()
    df_nou = df.copy()
    df_nou[coloane] = df_nou[coloane].fillna(medieCol)

    return df_nou

def tratareNAN_categoriale(df, coloane):

    df_new = df.copy()
    for col in coloane:
        most_frequent = df_new[col].mode().iloc[0]
        df_new[col] = df_new[col].fillna(most_frequent)

    return df_new


hr_personal = tratareNAN_numerice(hr_personal, ['Age'])
hr_personal = tratareNAN_categoriale(hr_personal, ['Education'])

hr_company = tratareNAN_numerice(hr_company, ['MonthlyIncome'])
hr_company = tratareNAN_categoriale(hr_company, ['JobInvolvement', 'JobSatisfaction'])



########################################################################################

#1. STATISTICI DESCRIPTIVE

media = hr_company['MonthlyIncome'].mean().round(2)
mediana = hr_company['MonthlyIncome'].median()
deviatia_standard = hr_company['MonthlyIncome'].std().round(2)
minim = hr_company['MonthlyIncome'].min()
maxim = hr_company['MonthlyIncome'].max()

print("Media veniturilor lunare:", media)
print("Mediana veniturilor lunare:", mediana)
print("Deviația standard a veniturilor lunare:", deviatia_standard)
print("Valoarea minimă a veniturilor lunare:", minim)
print("Valoarea maximă a veniturilor lunare:", maxim)

quartiles = hr_company['MonthlyIncome'].quantile([0.25, 0.5, 0.75])
quartiles_rounded = quartiles.round(2)

print("Quartile rotunjite pentru veniturile lunare:")
print("Q1 (25%):", quartiles_rounded[0.25])
print("Q2 (50%):", quartiles_rounded[0.5])
print("Q3 (75%):", quartiles_rounded[0.75])

# COMENTARII: 25% din angajati au venitul lunar mai mic decat 2911 dolari (unitati monetare) .....

#########################################################################################
#2. Adaugare nivel de experienta in functie de vechimea in companie a angajatilor


hr_company['ExperienceLevel'] = 'Entry'

for index, row in hr_company.iterrows():
    if 10 <= row['TotalWorkingYears'] < 15:
        hr_company.loc[index, 'ExperienceLevel'] = 'Intermediate'
    elif row['TotalWorkingYears'] > 15:
        hr_company.loc[index, 'ExperienceLevel'] = 'Senior'

print(hr_company)

hr_company.to_csv('employee_job_data_with_experience.csv', index=False)

#########################################################################################
#3. NUMAR ANGAJATI DIN FIECARE DEPARTAMENT FOLOSIND DICTIONAR

numarulAngajatilorPeDepartamente = {}

for department, numAngajati in hr_company['Department'].value_counts().items():
    numarulAngajatilorPeDepartamente[department] = numAngajati

print("Numărul de angajați pe departamente:")
print(numarulAngajatilorPeDepartamente)


#########################################################
#4. Performanta angajatilor la nivel de job
joburi = hr_company.iloc[:, 5].tolist()
joburiDistincte = list(set(joburi))

print("Lista cu toate joburile:")
print(joburiDistincte)

performantaJob = {}
for job in joburiDistincte:
    jobFiltrat = hr_company["JobRole"] == job
    job_df = hr_company[jobFiltrat]
    sumaAngPerformanta = job_df.groupby('PerformanceRating').size()
    performantaJob[job] = sumaAngPerformanta

print("Suma numărului de angajați pentru fiecare valoare a PerformanceRating pentru fiecare job:")
for job, sumaAngPerformanta in performantaJob.items():
    print(f"{job}:")
    for rating, count in sumaAngPerformanta.items():
        print(f"  PerformanceRating {rating}: {count} angajati")

# COMENTARII ULTERIOARE: ex - Pe baza rezultatelor observam ca nivelul de performanta al angajatilor cu rolul X, este destul de scazut, putand afecta compania => mai trebuie train-uiti

#################################
#5. ANALIZA RATA RETENTIE ANGAJATI IN FUNCTIE DE TURELE SUPLIMENTARE
df_merged = pd.merge(hr_personal, hr_company, on="EmployeeNumber")

df_overtime = df_merged[df_merged["OverTime"] == "Yes"]
df_no_overtime = df_merged[df_merged["OverTime"] == "No"]

deciziaOvertime = len(df_overtime[df_overtime["Attrition"] == "No"]) / len(df_overtime) * 100
deciziaNoOvertime = len(df_no_overtime[df_no_overtime["Attrition"] == "No"]) / len(df_no_overtime) * 100

# Vizualizarea rezultatelor utilizând un grafic de bare
labels = ['Peste program', 'Program normal']
rate= [deciziaOvertime, deciziaNoOvertime]

plt.bar(labels, rate, color=['blue', 'green'])
plt.ylabel('Procentul angajaților ')
plt.title('Decizia angajaților de a rămâne în companie')
plt.ylim(0, 100)
plt.show()



##########################################################################################3
#6. IMPACTUL NIVELULUI DE SASTISFACTIE ASUPRA RATEI DE RETENTIE
# Analizam daca satisfactia la locul de munca influenteaza decizia angajatilor de a parasi compania


satisfaction_attrition = df_merged[["JobSatisfaction", "Attrition"]]
total_employees_by_satisfaction = satisfaction_attrition.loc[:, "JobSatisfaction"].value_counts()
attrition_by_satisfaction = satisfaction_attrition[satisfaction_attrition["Attrition"] == "Yes"].groupby("JobSatisfaction").size()
attrition_rate_by_satisfaction = (attrition_by_satisfaction / total_employees_by_satisfaction) * 100

print("Procentul de angajați care au plecat în funcție de nivelul de satisfacție:")
print(attrition_rate_by_satisfaction)

print("Numărul total de angajați pentru fiecare nivel de satisfacție:")
print(total_employees_by_satisfaction)

print("\nNumărul de angajați care au plecat pentru fiecare nivel de satisfacție:")
print(attrition_by_satisfaction)


satisfaction_levels = attrition_rate_by_satisfaction.index
attrition_percentages = attrition_rate_by_satisfaction.values


colors = ['skyblue', 'lightgreen', 'salmon', 'pink']
plt.figure(figsize=(10, 6))
plt.bar(satisfaction_levels, attrition_percentages, color=colors)
plt.xlabel('Nivel de satisfacție')
plt.title('Procentul de angajați care au plecat în funcție de nivelul de satisfacție')
plt.xticks(satisfaction_levels)
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


##############################################################################################
#7. Gruparea și agregarea datelor:
# Gruparea datelor în funcție de nivelul de educație,
# Agregarea veniturilor lunare pentru a vedea cum variază acestea între diferite grupuri.


income_by_education = df_merged.groupby('Education')['MonthlyIncome'].mean()


print("Venitul mediu lunar în funcție de nivelul de educație:")
print(income_by_education.round(2))

income_by_education.plot(kind='line', marker='o', color='orange')
plt.title('Venitul mediu lunar în funcție de nivelul de educație')
plt.xlabel('Nivelul de educație')
plt.ylabel('Venit mediu lunar')
plt.grid(True)
plt.show()

# COMENTARII: Nivelul de educatie este direct proportional cu nivelul venitului lunar mediu


################################################################################################
#8.  Utilizare set, dictionar pentru a determina nr de angajati din fiecare domeniu educational unic

domenii_educatie = set()

numar_angajati_domeniu = {}


for index, row in df_merged.iterrows():
    domeniu = row["EducationField"]
    domenii_educatie.add(domeniu)
    numar_angajati_domeniu[domeniu] = numar_angajati_domeniu.get(domeniu, 0) + 1


print("Domenii de educație unice si numarul de angajați din fiecare domeniu:")
for domeniu in domenii_educatie:
    print("Domeniu:", domeniu, "- Numar de angajați:", numar_angajati_domeniu[domeniu])


#################################################################################################

#9. Angajatii care au ramas in companie - dataFrame nou


df_angajati_ramasi = df_merged.copy()

df_angajati_ramasi = df_angajati_ramasi.drop(df_angajati_ramasi [df_angajati_ramasi ['Attrition'] == 'Yes'].index)

df_angajati_ramasi = df_angajati_ramasi.drop('Attrition', axis=1)

print(df_angajati_ramasi)

print("Numarul de observatii înainte:", len(df_merged))
print("Numarul de observatii dupa stergere:", len(df_angajati_ramasi))

print("Coloanele ramase dupa stergere:")
print(df_angajati_ramasi.columns)



################### SAS ##################################################################################

df_merged.to_csv('employees_merged.csv', index = False)




