-- Creates a stored procedure that computes
-- avergaage score of the student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE average_score DECIMAL DEFAULT 0;

	SELECT CAST(AVG(score) AS DECIMAL)
	INTO average_score
	FROM corrections
	WHERE corrections.user_id = user_id;

	UPDATE  users
	SET users.average_score = average_score
	WHERE users.id = user_id;
END //
DELIMITER ;
	   
