-- Dropping tables in reverse order of creation to handle dependencies
DROP TABLE IF EXISTS QB.caixa;
DROP TABLE IF EXISTS QB.certificados
DROP TABLE IF EXISTS QB.selo;
DROP TABLE IF EXISTS QB.tipoRolha_fornecedor;
DROP TABLE IF EXISTS QB.tipoRolha;
DROP TABLE IF EXISTS QB.rolha;
DROP TABLE IF EXISTS QB.rotulo;
DROP TABLE IF EXISTS QB.componente;
DROP TABLE IF EXISTS QB.garrafa;
DROP TABLE IF EXISTS QB.garrafao;
DROP TABLE IF EXISTS QB.item;
DROP TABLE IF EXISTS QB.stock;
DROP TABLE IF EXISTS QB.encomenda;
DROP TABLE IF EXISTS QB.fornecedor;
DROP TABLE IF EXISTS QB.cliente;
DROP TABLE IF EXISTS QB.engarrafamento;
DROP TABLE IF EXISTS QB.cuba_engarrafamento;
DROP TABLE IF EXISTS QB.cuba;
DROP TABLE IF EXISTS QB.tipoVinho;
DROP TABLE IF EXISTS QB.casta_tipoVinho;
DROP TABLE IF EXISTS QB.casta;

-- Dropping the schema
--DROP SCHEMA IF EXISTS QB;
--GO
