/*



This program computes imputed employment for the SIC "partial codes" in the 1977 to 1997 cbp files

For further detail, see 

Fabian Eckert, Teresa C. Fort, Peter K. Schott, and Natalie J. Yang. "Imputing Missing Values in the US Census Bureau's County Business Patterns." NBER Working Paper #XXX, 2019

2019.12.19 pks


*/




if  "`c(username)'" == "pks4" {

	if c(os)=="Windows" {
		global IMPR	"E:/Dropbox (yale som economics)/research/CBP Yunus/point_estimates_RAW_ALL"
		global IMPN	"E:/Dropbox (yale som economics)/research/CBP Yunus/point_estimates_NOISY_ALL"
		global SIC	"E:/Dropbox (yale som economics)/research/cbp_project/Data Appendix/CBP_industry_list"
		global PKS  "E:/Dropbox (yale som economics)/research/cbp_project/Data Appendix/pks/interim"
		global RAW	"E:/Dropbox (yale som economics)/research/cbp_project/Data Appendix/Raw Data"
		global RAW2	"E:/Dropbox (yale som economics)/research/cbp_project/imputed_data/1998-2016 - NAICS/County/"
		global FIG	"E:/Dropbox (yale som economics)/research/cbp_project/drafts/figures"
		global YUN	"E:/Dropbox (yale som economics)/research/CBP Yunus/Industry Levels"
		global MID	"E:/Dropbox (yale som economics)/research/CBP Yunus/point_estimates I/midpoint"
		global FIR  "E:/Dropbox (yale som economics)/research/cbp_project/imputed_data/Final/First Release/"

	}
	else {
		global IMPR	"/Users/pks4/Dropbox (yale som economics)/research/CBP Yunus/point_estimates_RAW_ALL"
		global IMPN	"/Users/pks4/Dropbox (yale som economics)/research/CBP Yunus/point_estimates_NOISY_ALL"
		global PKS  "/Users/pks4/Dropbox (yale som economics)/research/cbp_project/Data Appendix/pks/interim"
		global RAW	"/Users/pks4/Dropbox (yale som economics)/research/cbp_project/Data Appendix/Raw Data"
		global FIG	"/Users/pks4/Dropbox (yale som economics)/research/cbp_project/drafts/figures"
		global YUN	"/Users/pks4/Dropbox (yale som economics)/research/CBP Yunus/Industry Levels"
		global RAW2 "/Users/pks4/Dropbox (yale som economics)/research/cbp_project/imputed_data/1998-2016 - NAICS/County/"
		global MID	"/Users/pks4/Dropbox (yale som economics)/research/CBP Yunus/point_estimates I/midpoint"
	}
}



if  "`c(username)'" == "fpeckert" {
	global PKS  "/Users/fpeckert/Dropbox/Projects/cbp_project/Data Appendix/pks/interim"
	global FIG	"/Users/fpeckert/Dropbox/Projects/cbp_project/drafts/figures"
	}


clear all
set more off











quietly {
	 forvalues y=1977/1997 {

		*note that both lb and ub contain the imputed value in these files
		import delimited "$FIR/efsy_cbp_`y'.csv", clear
		
		*variables needed for collapsing by "##--" codes
		gen dash1 = substr(sic,4,4)=="-"
		gen dash2 = substr(sic,3,4)=="--"
		gen dash3 = substr(sic,2,4)=="---"
		gen dash4 = substr(sic,1,4)=="----"
		gen dash = 0
		replace dash=1 if dash1
		replace dash=2 if dash2
		replace dash=3 if dash3
		replace dash=4 if dash4
		drop dash1-dash4

		*create identifiers used in pks' ".../imputed_data/step_1_initial_bounds_01.do" file 
		*
		*	there are two kinds of summation codes: those ending in "/" and those ending in "0". 
		*	if a code ends in "/", it is the total for all codes with roots until the next "/" 
		*	code. If it ends in "0", it is the total for all codes with the same root up until the 
		*	zero. 
		*
		*		WE SHOULD VERIFY THAT THERE ARE NO CODES ACTUALLY ENDING IN 0"!!!!
		*	
		*	to create a national total
		*
		*		include all XXXX, i.e., codes not ending in zero
		*		include all XXX0 if there are no XXXX within same county-state
		*		include all XX00 if there are no XXX0 within same county-state
		*
		*	dash codes
		*		d0 codes (1980-98): ////
		*		d1 codes (1980-98): none
		*		d2 codes (1980-98): 07// (captures 08,09) 10// (11,12,13,14) 15// 19// 40// 50// 52// 60// 70// 99//
		*		d3 codes (1980-88): 098/ 149/ 179/ 399/ 497/ 519/ 599/ 679/ 899/
		*
		*	zero codes
		*		z0 codes: none
		*		z1 codes: none
		*		z2 codes: many, including 1000 2000 3000 5000 6000 7000 8000
		*		z3 codes: many
		*		z4 codes: many
		*
		*	NOTE: "//xx" codes are like another whole level, but they all do not exist for all 
		*		  counties; so, what to do about that? perhaps it is because there are no 
		*		  industries with those roots in those counties, but this should be verified
		*
		*		07// captures 08,09 
		*		10// captures 11,12,13,14 
		*		15// captures 16,17
		*		20// captures 21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37,38,39
		*		40// captures 41,42,44,45,46,47,48,49
		*		50// captures 50,51
		*		52// captures 52,53,54,55,56,57,58,59
		*		60// captures 61,62,63,64,65,66,67
		*		70// captures 72,73,74,75,76,78,79,81,82,83,84,86,89
		*		99// captures ?
		*
		*add slashes to be consistent with later years	*
		rename sic sic_old
		gen sic     = subinstr(sic_old,"-","/",6)
		replace sic = subinstr(sic,"\","/",6)

		*create dash code flags 
		gen d0 = substr(sic,1,4)=="////"
		gen d1 = substr(sic,2,4)=="///"  & ~d0
		gen d2 = substr(sic,3,4)=="//"   & ~d1 & ~d0
		gen d3 = substr(sic,4,4)=="/"    & ~d2 & ~d1 & ~d0
		gen d4 = strpos(sic,"/")==0      & ~d3 & ~d2 & ~d1 & ~d0

		*create zero code flags 
		*
		*	NOTE: there is no z1 b/c 1000 2000 3000 5000 6000 7000 8000 are TWO-digits with zeros 
		*
		gen z0 = substr(sic,1,4)=="0000"
		gen z2 = (substr(sic,2,4)=="000" | substr(sic,3,4)=="00") & ~z0             & ~(d0 | d1 | d2 | d3)
		gen z3 = substr(sic,4,4)=="0"                             & ~z0 & ~z2       & ~(d0 | d1 | d2 | d3)
		gen z4 = strpos(sic,"0")<3                                & ~z0 & ~z2 & ~z3 & ~(d0 | d1 | d2 | d3)

		*use zero code flags to determine whether a code has other codes "under" it
		*
		*		NOTE: under1 does not seem relevant
		*
		gen root3   = substr(sic,1,3)
		egen under3 = total(z4), by(fipstate fipscty root3)
		gen root2   = substr(sic,1,2)
		gen t1      = z3 | z4
		egen under2 = total(t1), by(fipstate fipscty root2)
		drop t1

		*use above to create level
		*
		*	level identifies the hierarchical "level" of the observation
		*
		*	
		*
		*	NOTEs: 
		*		
		*		there are 5 levels b/c the xx// codes are their own "super" levels
		*	
		*		an observation can have more than one level!
		*
		*			xx00 (including x000) can be level 2, 3 and/or 4	
		*			xxx0 can be level 3 and/or level 4
		*			xxxx can only be level 4
		*
		*		Example: suppose a county has 2200 but no underlying 22XX. Then that 
		*				 observation is both a level=2, level=3 and level=4 code! So, 
		*				 we need to repeat this observation in the dataset with as many 
		*				 different levels as it has 
		*
		*				 So, we create a series of vars, levela, levalb and levelc, to 
		*				 keep track of that
		*
		*		Auxilary codes, xxx/, are all levels 4 3 2 since we assume they are unto themselves
		*
		gen level4=.
		replace level4=1 if z4
		replace level4=1 if z3 & under3==0
		replace level4=1 if z2 & under2==0 
		replace level4=1 if d3 | sic=="99//"

		gen level3=.
		replace level3=1 if z3 
		replace level3=1 if z2 & under2==0
		replace level3=1 if d3 | sic=="99//"

		gen level2=.
		replace level2=1 if z2 
		replace level2=1 if d3 | sic=="99//"

		*set aux to level2
		gen aux = (sic_old=="098\" | sic_old=="149\" | sic_old=="179\" | sic_old=="399\" | sic_old=="497\" | sic_old=="519\" | sic_old=="599\" | sic_old=="679\" | sic_old=="899\")
		replace level4=0 if aux
		replace level3=0 if aux
		replace level2=1 if aux
		replace level2=1 if aux	
		
		*check that above make sense
		*
		*	do not expect z4 to be any level other than 4
		*	expect z3 to be levels 3 or 4 but not 2
		*	z2 can be any level
		*
		*table sic if z4, c(sum level2 sum level3 sum level4)
		*table sic if z3, c(sum level2 sum level3 sum level4)
		*table sic if z2, c(sum level2 sum level3 sum level4)

		*as noted above, the xx// codes are super categories, so reflect this in by putting their 
		*prefic on all codes they encompass
		gen s2=substr(sic,1,2)
		gen p = ""
		replace p="07" if s2=="07" | s2=="08" | s2=="09" 
		replace p="10" if s2=="10" | s2=="11" | s2=="12" | s2=="13"  | s2=="14"  
		replace p="15" if s2=="15" | s2=="16" | s2=="17" 
		replace p="20" if s2=="20" | s2=="21" | s2=="22" | s2=="23"  | s2=="24" | s2=="25" | s2=="26"  | s2=="27" | s2=="28" | s2=="29"      
		replace p="20" if s2=="30" | s2=="31" | s2=="32" | s2=="33"  | s2=="34" | s2=="35" | s2=="36"  | s2=="37" | s2=="38" | s2=="39"      
		replace p="40" if s2=="40" | s2=="41" | s2=="42" | s2=="43"  | s2=="44" | s2=="45" | s2=="46"  | s2=="47" | s2=="48" | s2=="49"      
		replace p="50" if s2=="50" | s2=="51"  
		replace p="52" if s2=="52" | s2=="53" | s2=="54" | s2=="55"  | s2=="56"  | s2=="57" | s2=="58" | s2=="59"    
		replace p="60" if s2=="60" | s2=="61" | s2=="62" | s2=="63"  | s2=="64" | s2=="65" | s2=="66"  | s2=="67" | s2=="68" | s2=="69"      
		replace p="70" if s2=="70" | s2=="71" | s2=="72" | s2=="73"  | s2=="74" | s2=="75" | s2=="76"  | s2=="77" | s2=="78" | s2=="79"      
		replace p="70" if s2=="80" | s2=="81" | s2=="82" | s2=="83"  | s2=="84" | s2=="85" | s2=="86"  | s2=="87" | s2=="88" | s2=="89"      
		replace p="99" if s2=="99"
		gen naics = p + sic 
		replace naics = sic + "//" if d2 | sic=="////"

		*add the other levels for // coddes
		gen level1=0
		replace level1=1 if d2==1
		gen level0=0
		replace level0=1 if naics=="//////"	

		*check totals; level 4 seems better
		gen year = `y'
		table year if level4==1, c(sum emp) f(%15.0fc)
		table year if dash~=0 & dash~=4, c(sum emp) f(%15.0fc)
		
		noisily table year if (level4~=1) & (dash~=0 & dash~=4), c(sum emp) f(%15.0fc)	
		
		/*
		keep if dash~=0
		collapse (sum) emp, by(fipstate fipscty sic)
		gen dash4 = substr(sic,1,4)=="----"
		egen total = total(emp), by(fipstate fipscty)
		replace total=total/2
		replace total=. if ~dash4
		gen check = (emp==total)
		tab check if dash4
		compare emp total if dash4
		*/
		
		save "$PKS/efsy_partial_`y'.dta", replace 

	}

	*append above 00 files together
	use "$PKS/efsy_partial_`y'.dta", clear
	forvalues y=1978/1997 {
		append using "$PKS/efsy_partial_`y'.dta"
	}
	save "$PKS/efsy_partial_19771997_00.dta", replace


	*add partial codes
	use "$PKS/efsy_partial_19771997_00.dta", clear
	*keep if year==1977
	replace naics = "52"+substr(naics,3,6) if substr(naics,1,2)=="50" & substr(sic_old,1,2)=="52"
	sort fips* naics
	gen s3 = substr(sic_old,1,3)
	gen t0 = level4*emp
	egen sum4_3 = total(t0), by(fips* year s3)
	gen t1 = level3*emp
	egen sum_3 = total(t1), by(fips* year s3)
	gen emp_new = sum_3-sum4_3
	replace emp_new=. if sum_3==sum4_3
	sum emp_new
	gen i4=sum4_3~=sum_3
	edit fip* naics sic_old s2 level* emp emp_new sum4_3 t1 sum_3 i4 
	tab year i4 if level3==1 & level4==0
	keep if i4==1 & level3==1
	gen naics_new = substr(naics,1,5) + "P"
	keep fips* year naics_new emp_new
	gen s2_new = substr(naics_new,3,2)
	rename (naics_new s2_new emp_new) (naics s2 emp)
	gen level4=1
	gen partial=1
	save "$PKS/efsy_partial_19771997_00_partial4_3.dta", replace

	*check if level4 add up to level2 with above partials included
	use "$PKS/efsy_partial_19771997_00.dta", clear
	append using "$PKS/efsy_partial_19771997_00_partial4_3.dta"
	replace naics = "52"+substr(naics,3,6) if substr(naics,1,2)=="50" & substr(sic_old,1,2)=="52"
	*keep if year==1977
	sort fips* naics	
	gen t2 = level4*emp
	egen sum4_2 = total(t2), by(fips* year s2)
	gen t3 = level2*emp
	egen sum_2 = total(t3), by(fips* year s2)
	gen i2=sum4_2~=sum_2
	tab year i2
	gen emp_new = sum_2-sum4_2
	edit fip* naics sic_old s2 level* emp emp_new sum* i2
	keep if i2==1 & level2==1 & aux==0
	gen naics_new = substr(naics,1,4) +"QQ"
	keep fips* year naics_new emp_new
	rename (naics_new emp_new) (naics emp)
	gen level4=1
	gen partial=1
	gen s2 = substr(naics,3,2)
	table year, c(sum emp) f(%15.0fc)	
	save "$PKS/efsy_partial_19771997_00_partial4_2.dta", replace
	
	*check if level4 add up to div with partial included
	use "$PKS/efsy_partial_19771997_00.dta", clear
	append using "$PKS/efsy_partial_19771997_00_partial4_3.dta"
	append using "$PKS/efsy_partial_19771997_00_partial4_2.dta"
	replace naics = "52"+substr(naics,3,6) if substr(naics,1,2)=="50" & substr(sic_old,1,2)=="52"
	*keep if year==1977
	sort fips* naics	
	gen div=substr(naics,1,2)
	gen t2 = level4*emp
	egen sum4_1 = total(t2), by(fips* year div)
	gen t3 = level1*emp
	egen sum_1 = total(t3), by(fips* year div)
	gen i1=sum4_1~=sum_1
	tab year i1
	gen emp_new = sum_1-sum4_1
	edit fip* naics sic_old div s2 level* emp emp_new sum* i1
	keep if i1==1 & level1==1 & aux==0
	gen naics_new = substr(naics,1,2) + "VVVV"
	keep fips* year naics_new emp_new
	gen s2 = substr(naics,3,2)
	rename (naics_new emp_new) (naics emp)
	table year, c(sum emp) f(%15.0fc)
	gen level4=1
	gen partial=1
	save "$PKS/efsy_partial_19771997_00_partial4_1.dta", replace

	*check if level4 now gives level1
	use "$PKS/efsy_partial_19771997_00.dta", clear
	*keep if year==1977
	table year if level4==1, c(sum emp) f(%15.0fc)
	table year if level1==1, c(sum emp) f(%15.0fc)
	append using "$PKS/efsy_partial_19771997_00_partial4_3.dta"
	append using "$PKS/efsy_partial_19771997_00_partial4_2.dta"
	append using "$PKS/efsy_partial_19771997_00_partial4_1.dta"
	sort fips* naics
	table year if level4==1, c(sum emp) f(%15.0fc)
	table year if level1==1, c(sum emp) f(%15.0fc)

	save "$PKS/efsy_partial_19771997_01.dta", replace
	
 }	
}

*create file to post for website
use "$PKS/efsy_partial_19771997_01.dta", replace
keep fipstate fipscty year emp partial naics
save "$PKS/efsy_partial_19771997_02.dta", replace
	table year if level4==1, c(sum imputed_employment) f(%15.0fc)
	table year if level1==1, c(sum imputed_employment) f(%15.0fc)

	
	xxxx


