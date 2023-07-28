DO $$
DECLARE
model1 varchar(100) := 'mechanical';
model2 varchar(100) := 'water';
model3 varchar(100) := 'absorption';
model4 varchar(100) := 'solid';
field_message varchar(100) := 'invalid field';
field_name varchar(100) := '"sr_no"';
errorMessage varchar(200);
view_name varchar(100) := model1 || '.' || model2 || '.' || model3 || '.' || model4 || '.form';
view_info RECORD;


BEGIN

SELECT *
  INTO view_info
  FROM ir_ui_view
  WHERE name = view_name;

--  IF view_info IS NULL THEN
--     RAISE EXCEPTION 'View with external_id % already exists with ID %', view_external_id, view_info.name;
-- END IF;
 IF view_info.name = model1 || '.' || model2 || '.' || model3 || '.' || model4 || '.form' THEN
    errorMessage :=  model1 || '.' || model2 || '.' || model3 || '.' || model4 || ' ' || field_message || ' ' || field_name;
    RAISE EXCEPTION '%',errorMessage;
 END IF;

END $$;