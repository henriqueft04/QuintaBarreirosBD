CREATE TRIGGER trg_UpdateTotalClientes
ON QB.cliente
AFTER INSERT
AS
    BEGIN
        DECLARE @totalClientes INT;

        SELECT @totalClientes = COUNT(*) FROM QB.cliente;
    end

SELECT COUNT(*) AS TotalClientes FROM QB.cliente;