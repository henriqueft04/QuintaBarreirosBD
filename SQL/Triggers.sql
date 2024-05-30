use p8g4
GO

CREATE TRIGGER trg_AtualizarEncomendas

ON QB.encomenda
AFTER INSERT, UPDATE, DELETE
AS 
	BEGIN
		DECLARE @TotalEncomendas INT;
		SET @TotalEncomendas = (SELECT QB.fn_AtualizaContagemEncomendas());
	END;
GO