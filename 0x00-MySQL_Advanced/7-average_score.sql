-- Compute and store an average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (IN id_user INT)
BEGIN
	DECLARE projects_count INT;
	DECLARE total_score FLOAT;
	DECLARE average_score FLOAT;

	SELECT COUNT(*), SUM(score)
	INTO projects_count, total_score
	FROM corrections
	WHERE user_id = id_user;

	SET average_score = total_score / COALESCE(projects_count, 1);

	UPDATE users
	SET average_score = average_score
	WHERE id = id_user;
END;//

DELIMITER ;
