USE culturallm_db;

DELIMITER //

CREATE TRIGGER trg_logs_questions
AFTER INSERT ON questions
FOR EACH ROW
BEGIN

  IF NEW.username IS NOT NULL THEN

    INSERT IGNORE INTO logs (username, score, action_type, timestamp)
    VALUES (NEW.username, NEW.cultural_specificity, 'question', NOW());
    
  END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_logs_answer
AFTER INSERT ON answers
FOR EACH ROW
BEGIN

  IF NEW.username IS NOT NULL THEN

    INSERT IGNORE INTO logs (username, score, action_type, timestamp)
    VALUES (NEW.username, 0, 'answer', NOW());

  END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_logs_ratings
AFTER INSERT ON ratings
FOR EACH ROW
BEGIN

  DECLARE final_score INT DEFAULT 0;

  IF NEW.username IS NOT NULL THEN
    SET final_score = NEW.rating;

    IF NEW.flag_ia = TRUE AND EXISTS (
      SELECT 1 FROM answers WHERE id = NEW.answer_id AND type = 'llm'
    ) THEN
      SET final_score = final_score + 1;

    ELSEIF NEW.flag_ia = FALSE AND EXISTS (
      SELECT 1 FROM answers WHERE id = NEW.answer_id AND type = 'human'
    ) THEN
      SET final_score = final_score + 1;
    END IF;

    INSERT INTO logs (username, score, action_type, timestamp)
    VALUES (NEW.username, final_score, 'rating', NOW());
  END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_leaderboard_update
AFTER INSERT ON logs
FOR EACH ROW
BEGIN

  INSERT IGNORE INTO leaderboard (username, score, num_ratings, num_questions, num_answers)
  VALUES (NEW.username, 0, 0, 0, 0);

 
  UPDATE leaderboard
  SET score = score + NEW.score,
      num_ratings = num_ratings + CASE WHEN NEW.action_type = 'rating' THEN 1 ELSE 0 END,
      num_questions = num_questions + CASE WHEN NEW.action_type = 'question' THEN 1 ELSE 0 END,
      num_answers = num_answers + CASE WHEN NEW.action_type = 'answer' THEN 1 ELSE 0 END
  WHERE username = NEW.username;
END;
//

DELIMITER ;