INSERT INTO QB.casta (nome, id) VALUES
('Cabernet Sauvignon', 1),
('Almafra', 2),
('Alvar', 3),
('Azal', 4),
('Malvasia Babosa', 5),
('Rabigato', 6)

INSERT INTO QB.tipoVinho (notacao, denominacao, id, acidez, ano_colheita, teor_alcoolico, sub-regiao) VALUES
('Red1', 'Douro DOC', 101, 5.5, 2018, 13.5, 'Douro'),
('Red2', 'Douro DAC', 102, 5.7, 2020, 12.5, 'Lixa');

INSERT INTO QB.casta_tipoVinho (id_tipoVinho, id_casta) VALUES
(101, 1),
(102, 4);

INSERT INTO QB.cuba (codigo, id_TipoVinho, dataArmazenado, descricao, volume, refrigerada, termica) VALUES
(2001, 101, '2020-05-21', 'Stainless steel tank', 5000, 1, 0),
(2002, 102, '2020-05-21', NULL, 3500, 1, 1);

INSERT INTO QB.cuba_engarrafamento (codigo_Cuba, dataEngarrafamento) VALUES
(2001, '2021-12-10'),
(2002, '2022-05-21');

INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES
('2021-12-10', 750, 5000),
('2022-05-21', 500, 1000);

INSERT INTO QB.cliente (NIF, morada, nome, telemovel, tipo, desconto) VALUES
(123456789, 'Rua das Flores, 123', 'Maria Silva', 912345678, 'Privado', 10),
(222333444, NULL, 'Antonio José', NULL, 'Privado', 15),
(223344567, 'Rua Do Restaurante, N7', 'Restaurante da Esquina', 271299566, 'Restaurante', 20);

INSERT INTO QB.fornecedor (NIF, morada, nome, telemovel) VALUES
(987654321, 'Avenida dos Vinhos, 321', 'Vinhos e Derivados SA', 961234567),
(256986703, 'Rua das Rolhas, N12', 'Rolhas', 932560433);


INSERT INTO QB.encomenda (NIF_cliente, fatura, valor, notas, data, numero) VALUES
(123456789, 1, 1200.50, 'Urgent delivery', '2024-05-01', 10001),
(987654321, 0, 200, NULL, '2024-03-18', 10002);


INSERT INTO QB.stock (id_tipoVinho, id, peso_liquido, peso_bruto, preco) VALUES
(101, 3001, 750, 800, 25.50),
(102, 3002, 750, 800, 7.30);

INSERT INTO QB.item (quantidadeItems, id_stock, numero_encomenda) VALUES
(10, 3001, 10001),
(15, 3002, 10002);

INSERT INTO QB.garrafao (id_stock, dataEng) VALUES
(3001, '2021-12-10'),
(3002, '2023-5-12');

INSERT INTO QB.garrafa (id_tipoVinho, id_stock, dataEng) VALUES
(101, 3001, '2021-12-10');

INSERT INTO QB.componente (id, quantidade) VALUES
(4001, 100);

INSERT INTO QB.rotulo (id_componente, NIF_cliente, notacao_tipoVinho) VALUES
(4001, 123456789, 'Red1');

INSERT INTO QB.rolha (id_componente, id_tipoRolha) VALUES
(4001, 5001);

INSERT INTO QB.tipoRolha (id, material, formato) VALUES
(5001, 'Cork', 'Standard');

INSERT INTO QB.tipoRolha_fornecedor (id_tipoRolha, NIF, data, quantidade) VALUES
(5001, 987654321, '2024-04-01', 2000);

INSERT INTO QB.selo (id_componente, ano, categoria) VALUES
(4001, 2024, 'DOC');

INSERT INTO QB.certificados (id_componente, ano, associacao, titulo) VALUES
(4001, 2024, 'Wine Association', 'Quality Verified');

INSERT INTO QB.caixa (numGarrafas, id_tipoVinho_garrafa, id_stock, dataEng, id_stock_garrafa) VALUES
('6 bottles', 101, 3001, '2021-12-10', 3001);

