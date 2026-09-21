filename cale '/home/u63854501/employee_job_data.csv';


proc import datafile=cale
            out=work.angajati_company
            dbms=csv
            replace;
    		getnames=yes;
run;

filename cale '/home/u63854501/employee_personal_data.csv';


proc import datafile=cale
            out=work.angajati_personal
            dbms=csv
            replace;
    		getnames=yes;
run;

data work.data_angajati;
    merge work.angajati_personal(in=a) work.angajati_company(in=b);
    by EmployeeNumber;
    if a and b then output;
run;



proc format;
    value educ_format
        1 = "High School"
        2 = "College"
        3 = "Bachelor"
        4 = "Master"
        5 = "PhD";
run;

proc format;
    value jobsat_format
        1 = "Very Low"
        2 = "Low"
        3 = "Good"
        4 = "Excellent";
run;


title 'Date angajati';
proc print data=work.data_angajati;
format Education educ_format.;
format JobSatisfaction jobsat_format.;
format EnvironmentSatisfaction jobsat_format.;
run;


/*Evidenta angajatilor ramasi in companie si au studii superioare*/
data work.data_angajati_ramasi_studiiSup;
	set work.data_angajati;
	where Attrition eq 'No' and Education in (3,4,5);
run;

title 'Angajati care au ramas in companie si au studii superioare';
proc print data=work.data_angajati_ramasi_studiiSup;
format Education educ_format.;
run;

/* proc sql; */
/*     drop table work.data_angajati_mariti; */
/* quit; */


data work.data_angajati_mariti;
    set work.data_angajati;
    if YearsAtCompany GE 10 then do;
        MonthlyIncome = MonthlyIncome * 1.3;
        output; 
    end;
    else output; 
run;

title 'Angajati cu vechimea mai mare de 10 ani cu salariul marit';
proc print data=work.data_angajati_mariti;
run;





/*Marirea salariului cu 10% a angajatilor a primilor 20 angajati din setul de date, care au performanta 4*/

proc sort data=work.data_angajati;
    by descending PerformanceRating;
run;

data work.data_angajati_mariti_10;
    set work.data_angajati;
    retain counter 0; 
    do i = 1 to nobs while (counter < 20);
        set work.data_angajati nobs=nobs point=i; 
        if PerformanceRating = 4 then do;
            MonthlyIncome = MonthlyIncome * 1.1; 
            counter = counter + 1; 
            output; 
        end;
    end;
run;

title 'Primii 20 de angajati cu performanta 4 cu salariul marit cu 10%';
proc print data=work.data_angajati_mariti_10;
run;



proc means data=work.data_angajati noprint;
    class Education;
    format Education educ_format.;
    var MonthlyIncome;
    output out=work.average_monthly_income mean=AverageMonthlyIncome;
run;


title 'Venitul mediu lunar in funcție de nivelul de educație';
proc print data=work.average_monthly_income;
run;

SYMBOL value=dot;
title 'Venitul mediu lunar pentru diferite niveluri de educatie';
proc gplot data=work.average_monthly_income;
   plot AverageMonthlyIncome*Education;
run;

quit;









	


