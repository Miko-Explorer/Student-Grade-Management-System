#Created a view for student report card details:
CREATE VIEW report_card_details AS 
SELECT S.student_id AS Student_ID,
CONCAT(S.first_name, " ", S.last_name) AS Fullname, 
C.semester AS Semester, 
C.course_code AS Course_Code, 
C.course_name AS Course_Name, 
C.units AS Units, 
G.grade_percentage AS Grade_in_Percentage, 
G.grade_letter AS Letter_Grading, 
CASE 
WHEN G.grade_percentage >= 50.0 THEN 'Passed'
WHEN G.grade_percentage < 50.0 THEN 'Failed'
END AS Remarks
FROM students AS S
INNER JOIN enrollments AS E ON E.student_id = S.student_id
INNER JOIN courses AS C ON E.course_id = C.course_id
LEFT JOIN grades AS G ON E.enrollment_id = G.enrollment_id;

#Created a view for student report card summary:
CREATE VIEW report_card_summary AS 
SELECT S.student_id AS Student_ID, 
C.semester AS Semester, 
SUM(C.units) AS Total_units_enrolled, 
SUM(CASE WHEN G.grade_percentage >= 50.0 THEN C.units ELSE 0 END) AS Total_units_passed,
SUM(G.grade_percentage * C.units) / NULLIF(SUM(CASE WHEN G.grade_percentage IS NOT NULL THEN C.units ELSE 0 END), 0) AS GWA, 
SUM(CASE WHEN A.attendance_status = "Present" THEN 1 ELSE 0 END) AS Total_Present,
SUM(CASE WHEN A.attendance_status = "Absent" THEN 1 ELSE 0 END) AS Total_Absent, 
SUM(CASE WHEN A.attendance_status = "Late" THEN 1 ELSE 0 END) AS Total_Late
FROM students AS S
INNER JOIN enrollments AS E ON E.student_id = S.student_id
INNER JOIN courses AS C ON E.course_id = C.course_id
LEFT JOIN grades AS G ON E.enrollment_id = G.enrollment_id
LEFT JOIN attendance AS A ON E.enrollment_id = A.enrollment_id
GROUP BY S.student_id, C.semester;

#Final report card summary:
CREATE VIEW final_report_card_summary AS 
SELECT d.Student_ID, d.Fullname, d.Semester,
d.Course_Code, d.Course_Name, d.Units,
d.Grade_in_Percentage, d.Letter_Grading, d.Remarks,
s.Total_units_enrolled, s.Total_units_passed,
s.GWA, s.Total_Present, s.Total_Absent,
s.Total_Late 
FROM report_card_details AS d
INNER JOIN report_card_summary AS s 
ON d.Student_ID = s.Student_ID 
AND d.Semester = s.Semester
ORDER BY d.Student_ID, d.Semester, d.Course_Code;

#Display records:
SELECT * FROM report_card_details; 
SELECT * FROM report_card_summary; 
SELECT * FROM final_report_card_summary;