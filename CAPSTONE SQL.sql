/*
 * Task1
 * Display the names of the unique launch sites in the space mission
 */
SELECT DISTINCT (LAUNCH_SITE) 
	FROM XTK78082.SPACEXTBL;

/*
 * Task 2
 * Display 5 records where launch sites begin with the string 'CCA'
 */
SELECT * FROM XTK78082.SPACEXTBL 
	WHERE LAUNCH_SITE LIKE 'CCA%' LIMIT 5;

/*
 * Task 3
 * Display the total payload mass carried by boosters launched by NASA (CRS)
 */
SELECT SUM(PAYLOAD_MASS__KG_) 
	FROM XTK78082.SPACEXTBL 
	WHERE CUSTOMER = 'NASA (CRS)';

/*
 * Task 4
 * Display average payload mass carried by booster version F9 v1.1
 */
SELECT AVG(PAYLOAD_MASS__KG_) 
	FROM XTK78082.SPACEXTBL 
	WHERE BOOSTER_VERSION = 'F9 v1.1';

/*
 * Task 5
 * List the date when the first successful landing outcome in-ground pad was acheived.
 */
SELECT MIN(DATE) FROM XTK78082.SPACEXTBL 
	WHERE LANDING__OUTCOME LIKE 'Success (ground pad)';

/*
 * Task 6
 * List the names of the boosters which have success in drone ship and 
 * have payload mass greater than 4000 but less than 6000
 */
SELECT BOOSTER_VERSION FROM XTK78082.SPACEXTBL 
	WHERE LANDING__OUTCOME = 'Success (drone ship)' 
		AND PAYLOAD_MASS__KG_ < 6000 AND PAYLOAD_MASS__KG_ >4000;

/*
 * Task 7
 * List the total number of successful and failure mission outcomes
 */
SELECT * FROM 
	(SELECT COUNT(MISSION_OUTCOME) 
		FROM XTK78082.SPACEXTBL 
		WHERE MISSION_OUTCOME LIKE '%Success%') AS Succ_Mission,
	(SELECT COUNT(MISSION_OUTCOME) 
		FROM  XTK78082.SPACEXTBL 
     	WHERE MISSION_OUTCOME LIKE '%Failure%') AS Fail_Mission; 

/*
 * Task 8
 * List the names of the booster_versions which have carried the 
 * maximum payload mass. Use a subquery
 */
SELECT BOOSTER_VERSION, PAYLOAD_MASS__KG_
	FROM XTK78082.SPACEXTBL
    WHERE PAYLOAD_MASS__KG_ = (
        SELECT MAX(PAYLOAD_MASS__KG_) FROM XTK78082.SPACEXTBL)
        ORDER BY BOOSTER_VERSION;
 
 /*
  * Task 9
  * List the failed landing_outcomes in drone ship, their booster versions, 
  * and launch site names for in year 2015
  */
SELECT BOOSTER_VERSION, LAUNCH_SITE, LANDING__OUTCOME
	FROM XTK78082.SPACEXTBL
    WHERE LANDING__OUTCOME LIKE 'Failure (drone ship)'
        AND Date BETWEEN '2015-01-01' AND '2015-12-31';