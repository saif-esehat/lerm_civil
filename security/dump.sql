DO $$
DECLARE
model1 varchar(100) := 'mechanical';
model2 varchar(100) := 'water';
model3 varchar(100) := 'absorption';
model4 varchar(100) := 'solid';
field_message varchar(100) := 'invalid field';
field_name varchar(100) := '"sr_no"';
errorMessage varchar(200);


BEGIN

errorMessage :=  model1 || '.' || model2 || '.' || model3 || '.' || model4 || ' ' || field_message || ' ' || field_name;

RAISE EXCEPTION '%',errorMessage;
END $$;