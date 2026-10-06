-- ============================================================
-- STUDENT SUCCESS ANALYTICS
-- SQL ANALYSIS
-- ============================================================

-- ------------------------------------------------------------
-- 1. SELECT DATABASE
-- ------------------------------------------------------------

USE student_success;


-- ------------------------------------------------------------
-- 2. CHECK TABLES
-- ------------------------------------------------------------

SHOW TABLES;


-- ------------------------------------------------------------
-- 3. CHECK TABLE STRUCTURE
-- ------------------------------------------------------------

DESCRIBE students;


-- ------------------------------------------------------------
-- 4. TOTAL NUMBER OF STUDENTS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS total_students
FROM students;


-- ------------------------------------------------------------
-- 5. PREVIEW DATA
-- ------------------------------------------------------------

SELECT *
FROM students
LIMIT 10;


-- ------------------------------------------------------------
-- 6. CHECK FOR NULL VALUES
-- ------------------------------------------------------------

-- Basic overview of rows containing NULL values
SELECT *
FROM students
LIMIT 20;


-- ------------------------------------------------------------
-- 7. NUMERICAL SUMMARY
-- ------------------------------------------------------------

-- You can inspect numerical columns using:
-- AVG(), MIN(), MAX(), COUNT()


-- ------------------------------------------------------------
-- 8. PLACEMENT DISTRIBUTION
-- ------------------------------------------------------------

-- If your placement column is named placement_status,
-- uncomment the query below.

-- SELECT
--     placement_status,
--     COUNT(*) AS student_count
-- FROM students
-- GROUP BY placement_status;


-- ------------------------------------------------------------
-- 9. PLACEMENT PERCENTAGE
-- ------------------------------------------------------------

-- SELECT
--     placement_status,
--     COUNT(*) AS student_count,
--     ROUND(
--         COUNT(*) * 100.0 /
--         (SELECT COUNT(*) FROM students),
--         2
--     ) AS percentage
-- FROM students
-- GROUP BY placement_status;


-- ------------------------------------------------------------
-- 10. AVERAGE GPA
-- ------------------------------------------------------------

-- SELECT
--     ROUND(AVG(average_gpa), 2) AS overall_average_gpa
-- FROM students;


-- ------------------------------------------------------------
-- 11. GPA VS PLACEMENT
-- ------------------------------------------------------------

-- SELECT
--     placement_status,
--     COUNT(*) AS students,
--     ROUND(AVG(average_gpa), 2) AS avg_gpa,
--     ROUND(MIN(average_gpa), 2) AS min_gpa,
--     ROUND(MAX(average_gpa), 2) AS max_gpa
-- FROM students
-- GROUP BY placement_status;


-- ------------------------------------------------------------
-- 12. ATTENDANCE VS PLACEMENT
-- ------------------------------------------------------------

-- SELECT
--     placement_status,
--     COUNT(*) AS students,
--     ROUND(AVG(attendance), 2) AS avg_attendance
-- FROM students
-- GROUP BY placement_status;


-- ------------------------------------------------------------
-- 13. BRANCH-WISE STUDENT COUNT
-- ------------------------------------------------------------

-- SELECT
--     branch,
--     COUNT(*) AS total_students
-- FROM students
-- GROUP BY branch
-- ORDER BY total_students DESC;


-- ------------------------------------------------------------
-- 14. BRANCH-WISE PLACEMENT
-- ------------------------------------------------------------

-- SELECT
--     branch,
--     COUNT(*) AS total_students,

--     SUM(
--         CASE
--             WHEN placement_status = 'placed'
--             THEN 1
--             ELSE 0
--         END
--     ) AS placed_students,

--     ROUND(
--         SUM(
--             CASE
--                 WHEN placement_status = 'placed'
--                 THEN 1
--                 ELSE 0
--             END
--         ) * 100.0 / COUNT(*),
--         2
--     ) AS placement_rate

-- FROM students

-- GROUP BY branch

-- ORDER BY placement_rate DESC;


-- ------------------------------------------------------------
-- 15. BACKLOG VS PLACEMENT
-- ------------------------------------------------------------

-- SELECT
--     backlogs,
--     COUNT(*) AS total_students,

--     SUM(
--         CASE
--             WHEN placement_status = 'placed'
--             THEN 1
--             ELSE 0
--         END
--     ) AS placed_students

-- FROM students

-- GROUP BY backlogs

-- ORDER BY backlogs;


-- ------------------------------------------------------------
-- 16. AVERAGE CTC
-- ------------------------------------------------------------

-- SELECT
--     ROUND(AVG(ctc), 2) AS average_ctc,
--     ROUND(MIN(ctc), 2) AS minimum_ctc,
--     ROUND(MAX(ctc), 2) AS maximum_ctc
-- FROM students
-- WHERE ctc IS NOT NULL;


-- ------------------------------------------------------------
-- 17. CTC BY BRANCH
-- ------------------------------------------------------------

-- SELECT
--     branch,
--     ROUND(AVG(ctc), 2) AS average_ctc
-- FROM students
-- WHERE ctc IS NOT NULL
-- GROUP BY branch
-- ORDER BY average_ctc DESC;


-- ------------------------------------------------------------
-- 18. TOP CTC STUDENTS
-- ------------------------------------------------------------

-- SELECT *
-- FROM students
-- WHERE ctc IS NOT NULL
-- ORDER BY ctc DESC
-- LIMIT 10;


-- ============================================================
-- ADVANCED SQL
-- ============================================================


-- ------------------------------------------------------------
-- 19. CTE — BRANCH PLACEMENT ANALYSIS
-- ------------------------------------------------------------

-- WITH placement_summary AS (
--
--     SELECT
--         branch,
--         COUNT(*) AS total_students,
--
--         SUM(
--             CASE
--                 WHEN placement_status = 'placed'
--                 THEN 1
--                 ELSE 0
--             END
--         ) AS placed_students
--
--     FROM students
--     GROUP BY branch
-- )
--
-- SELECT
--     branch,
--     total_students,
--     placed_students,
--
--     ROUND(
--         placed_students * 100.0 / total_students,
--         2
--     ) AS placement_rate
--
-- FROM placement_summary
--
-- ORDER BY placement_rate DESC;


-- ------------------------------------------------------------
-- 20. WINDOW FUNCTION EXAMPLE
-- ------------------------------------------------------------

-- SELECT
--     branch,
--     placement_status,
--     COUNT(*) AS students,
--
--     SUM(COUNT(*)) OVER (
--         PARTITION BY branch
--     ) AS branch_total
--
-- FROM students
--
-- GROUP BY
--     branch,
--     placement_status;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================