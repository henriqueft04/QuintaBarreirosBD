INSERT INTO QB.casta (nome, id) VALUES
('Alvarinho', 1),
('Avesso', 2),
('Espadeiro', 3),
('Padeiro', 4),
('Loureiro', 5),
('Arinto', 6),
('Trajadura', 7),
('Padeiro de Bastos', 8),
('Verdelho', 9),
('Azal', 10),
('Arinto', 11),
(N'Vinhão', 12);

INSERT INTO QB.tipoVinho (notacao, denominacao, id, acidez, ano_colheita, teor_alcoolico, "sub-regiao") VALUES
('Grande Escolha', 'Vinho Verde Branco', 101, 6.1, 2021, 12, 'Sousa'),
('Grande Escolha', 'Vinho Verde Rosado', 102, 6.7, 2021, 11, 'Sousa'),
(NULL, 'Vinho Frisante Branco', 103, 6.5, 2021, 11, 'Sousa'),
(NULL, N'Frisante Rosé', 104, 6.9, 2021, 11, 'Sousa'),
('Vinhos de Mesa', 'Vinho Branco Tradicional', 105, 6.5, 2021, 11, 'Sousa'),
('Vinhos de Mesa', N'Vinho Rosé Tradicional', 106, 7, 2021, 10.8, 'Sousa'),
('Vinhos de Mesa', 'Vinho Tinto Tradicional', 107, 6.5, 2021, 11.5, 'Sousa');


INSERT INTO QB.casta_tipoVinho (id_tipoVinho, id_casta) VALUES
(101, 1),
(101, 2),
(102, 3),
(102, 4),
(103, 2),
(103, 5),
(103, 6),
(103, 7),
(104, 3),
(104, 8),
(104, 9),
(105, 10),
(105, 2),
(105, 11),
(105, 7),
(105, 5),
(106, 3),
(106, 4),
(106, 9),
(107, 12);

INSERT INTO QB.cuba (codigo, id_TipoVinho, dataArmazenado, descricao, volume, volumeOcupado, refrigerada, termica) VALUES
(1, 101, '2020-05-21', NULL, 5000, 5000, 1, 0),
(2, 102, '2020-05-21', NULL, 5000, 4000, 1, 1),
(3, 103, '2020-12-04', NULL, 2500, 2000, 0, 0),
(4, NULL, NULL, NULL, 2500, 0, 0, 0),
(5, NULL, NULL, NULL, 2500, 0, 0, 0),
(6, NULL, NULL, NULL, 5000, 0, 0, 0),
(7, NULL, NULL, NULL, 2500, 0, 0, 0),
(8, NULL, NULL, NULL, 2500, 0, 0, 0),
(9, NULL, NULL, NULL, 2500, 0, 0, 0),
(10, NULL, NULL, NULL, 1500, 0, 0, 0),
(11, NULL, NULL, NULL, 1500, 0, 0, 0),
(12, NULL, NULL, NULL, 1500, 0, 0, 0),
(13, NULL, NULL, NULL, 2000, 0, 0, 0),
(14, NULL, NULL, NULL, 1500, 0, 0, 0),
(15, NULL, NULL, NULL, 1500, 0, 0, 0),
(16, NULL, NULL, NULL, 5000, 0, 0, 0),
(17, NULL, NULL, NULL, 1000, 0, 0, 0),
(18, NULL, NULL, NULL, 500, 0, 0, 0),
(19, NULL, NULL, NULL, 1000, 0, 0, 0),
(20, NULL, NULL, NULL, 1000, 0, 0, 0),
(21, NULL, NULL, NULL, 5000, 0, 0, 0),
(22, NULL, NULL, NULL, 1000, 0, 0, 0),
(23, NULL, NULL, NULL, 1000, 0, 0, 0),
(24, NULL, NULL, NULL, 500, 0, 0, 0),
(25, NULL, NULL, NULL, 500, 0, 0, 0),
(26, NULL, NULL, NULL, 500, 0, 0, 0),
(27, NULL, NULL, NULL, 500, 0, 0, 0),
(28, NULL, NULL, NULL, 500, 0, 0, 0),
(29, NULL, NULL, NULL, 500, 0, 0, 0),
(30, NULL, NULL, NULL, 250, 0, 0, 0),
(31, NULL, NULL, NULL, 16000, 0, 0, 0),
(32, NULL, NULL, NULL, 16000, 0, 0, 0),
(33, NULL, NULL, NULL, 16000, 0, 0, 0),
(34, NULL, NULL, NULL, 16000, 0, 0, 0),
(35, NULL, NULL, NULL, 16000, 0, 0, 0),
(36, NULL, NULL, NULL, 5000, 0, 0, 0),
(37, NULL, NULL, NULL, 5000, 0, 0, 0),
(38, NULL, NULL, NULL, 16000, 0, 0, 0),
(39, NULL, NULL, NULL, 16000, 0, 0, 0),
(40, NULL, NULL, NULL, 16000, 0, 0, 0),
(41, NULL, NULL, NULL, 20000, 0, 0, 0),
(42, NULL, NULL, NULL, 20000, 0, 0, 0),
(43, NULL, NULL, NULL, 10000, 0, 0, 0),
(44, NULL, NULL, NULL, 10000, 0, 0, 0),
(45, NULL, NULL, NULL, 250, 0, 0, 0);

INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2020-12-29', 1000, 1333);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-01-21', 500, 666);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-02-02', 2500, 3333);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-02-10', 5000, 6666);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-02-28', 1500, 2000);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-03-12', 2500, 3333);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-04-20', 500, 666);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2022-05-21', 250, 333);
INSERT INTO QB.engarrafamento (dataEng, litragemEng, quantidade) VALUES ('2024-01-10', 500, 666);


INSERT INTO QB.cuba_engarrafamento (codigo_Cuba, dataEngarrafamento) VALUES
(2, '2020-12-29'),
(3, '2022-01-21'),
(4, '2022-02-02'),
(6, '2022-02-10'),
(12, '2022-02-28'),
(8, '2022-03-12'),
(25, '2022-04-20'),
(45, '2022-05-21'),
(1, '2024-01-10');


INSERT INTO QB.cliente (NIF, morada, nome, telemovel, tipo) VALUES
(123456789, 'Rua da Tasca', 'Tasca do Bôzo', 961234567, 'Restaurante'),
(987654321, 'Avenida dos Vinhos, 321', 'FineTaste', 961255467, 'Restaurante'),
(256986703, 'Rua das Rolhas, N12', 'Dias, LDA', 932560433, 'Distribuidor'),
(234567890, 'Rua da Pega', 'Berto Barreiros', 913456789, 'Particular'),
(345678901, 'Rua do Vinho', 'Emídio', 912345678, 'Particular'),
(456789677, 'Rua Principal, 8', 'Dino, LDA', 914567890, 'Distribuidor'),
(567890123, 'Rua do Convento', 'Pedro Pereira', 912345877, 'Particular'),
(678901234, 'Rua das Pinhas', 'Zé Carlos', 933345678, 'Particular'),
(789012345, 'Avenida dos Croquis', 'Croquis em Marcha', 912345678, 'Restaurante'),
(890123456, 'Rua da Bomba', 'Fonseca Bomba', 912225678, 'Particular'),
(901234567, 'Rua das Tempestades', 'Miguel Trovoada', 912345578, 'Particular'),
(234567880, 'Rua da Ribeira', 'Ribeiro Paredes', 912345677, 'Particular'),
(345672901, 'Rua do Emigrante', 'Taberna de Paris', 912345678, 'Restaurante'),
(456789657, 'Rua da Amargura', 'Daniela Asstir', 913345678, 'Particular'),
(567890133, 'Rua dos Deslocados', 'Fernando Aveiro', 912335678, 'Particular'),
(678901434, 'Rua do Desconhecidos', 'Lassan Segmento', 2112345678, 'Distribuidor'),
(789012343, 'Rua do Prego', 'Menina Caíde Rei', 212335678, 'Restaurante'),
(890122456, 'Rua dos Bombeiros', 'Tesla Angola', 912345456, 'Particular'),
(901235567, 'Rua do Descobrimentos', 'Carioca', 912345666, 'Particular'),
(123457788, 'Rua dos Caçadorea', 'Pacheco', 912344678, 'Particular'),
(234561890, 'Rua do Café', 'Café Anize', 912345628, 'Restaurante'),
(345678902, 'Rua do Pasto', 'Leites', 932345678, 'Particular'),
(456789617, 'Rua da Casa do Povo', 'Casa do Povo Figueiro', 212345678, 'Restaurante'),
(267890123, 'Rua das Travessias', 'Sr Morreira', 925345678, 'Particular'),
(678903234, 'Rua dos Limites', 'Terra e Mar', 912345678, 'Restaurante'),
(789012145, 'Rua da Alegria', 'Três Jorges', 912345478, 'Restaurante'),
(890121456, 'Rua da França', 'França c3', 912343456, 'Particular'),
(903234567, 'Rua do Juventude', 'Magalhães', 912344378, 'Particular'),
(123453789, 'Rua da Firmeza', 'Restaurante Firmino', 211534708, 'Restaurante'),
(235567890, 'Rua da Beleza ', 'Ribeiro Paredes', 912445678, 'Particular'),
(345678501, 'Rua do Penhasco', 'Silva', 913445678, 'Particular'),
(456789477, 'Rua da Familia', 'Dino Filho', 912337678, 'Particular'),
(567820123, 'Rua da Vizinhança', 'Ferreira Lousada', 921234567, 'Particular'),
(678901424, 'Rua do Estranho', 'Jorge Irivo', 933455666, 'Particular'), 
(456729677, 'Rua do Muro', 'Ribeiro Paredes', 932335678, 'Particular'),
(678907234, 'Rua do Companhia', 'Paulo Vizinho', 932677900, 'Particular'),
(789062345, 'Rua do Milho', 'Emídio', 922445678, 'Particular'),
(890153456, 'Rua do Espanto', 'Domingos Barbeiro', 933512639, 'Particular'),
(901234564, 'Rua do Monte', 'Domingos Barreiros', 937619745, 'Particular'),
(123466789, 'Rua das Motas', 'Flávio Guimarães', 923648098, 'Particular'),
(234546890, 'Rua do Carpinteiro', 'Fernando Carpinteiro', 921679376, 'Particular'),
(345678904, 'Rua do Meio', 'Café Sampaio', 912345678, 'Restaurante'),
(456789977, 'Rua da Herdade', 'Taberna dos Herdeiros', 936851879, 'Restaurante'),
(678904234, 'Rua de Cima', 'Angélico Dino', 912645678, 'Particular');

INSERT INTO QB.fornecedor (NIF, morada, nome, telemovel) VALUES
(987654322, 'Avenida dos Vinhos, 321', 'Rolhas1', 961234567),
(256986503, 'Rua das Rolhas, N12', 'Rolhas2', 932560433),
(712983756, 'Rua da Cortiça', 'Rolhas3', 961234567),
(837249200, 'Rua da República', 'Rolhas4', 961234567);

INSERT INTO QB.encomenda (NIF_cliente, estadoPagamento, fatura, valor, notas, data, numero) VALUES
(123456789, 1, 1, 250.50, 'Primeira encomenda', '2024-05-01', 1),
(987654321, 1, 0, 150.75, 'Encomenda sem fatura', '2024-05-02', 2),
(256986703, 0, 1, 300.00, 'Cliente frequente', '2024-05-03', 3),
(234567890, 0, 1, 120.99, 'Nova encomenda', '2024-05-04', 4),
(345678901, 1, 0, 175.50, 'Promoção especial', '2024-05-05', 5),
(456789677, 1,1, 210.00, 'Encomenda grande', '2024-05-06', 6),
(567890123, 1, 0, 50.25, 'Pequena encomenda', '2024-05-07', 7),
(678901234, 0, 1, 400.75, 'Encomenda VIP', '2024-05-08', 8),
(789012345, 0, 1, 225.00, 'Cliente antigo', '2024-05-09', 9),
(890123456, 1, 0, 130.45, 'Encomenda rápida', '2024-05-10', 10),
(901234567, 1, 1, 300.50, 'Encomenda de grande volume', '2024-05-11', 11),
(234567880, 1, 0, 85.75, 'Encomenda para evento', '2024-05-12', 12),
(345672901, 1, 1, 500.00, 'Encomenda mensal', '2024-05-13', 13),
(456789657, 1, 0, 120.00, 'Encomenda pequena', '2024-05-14', 14),
(567890133, 0, 1, 250.25, 'Encomenda urgente', '2024-05-15', 15),
(678901434, 0, 0, 275.75, 'Encomenda especial', '2024-05-16', 16),
(789012343, 1, 1, 150.00, 'Encomenda de rotina', '2024-05-17', 17),
(890122456, 1, 0, 95.45, 'Encomenda de teste', '2024-05-18', 18),
(901235567, 1, 1, 350.75, 'Encomenda grande', '2024-05-19', 19),
(123457788, 0, 0, 220.99, 'Encomenda de promoção', '2024-05-20', 20);

INSERT INTO QB.stock (id_tipoVinho, id, quantidade, peso_liquido, peso_bruto, preco, dataEng) VALUES
(101, 1001, 100, 700, 800, 25.50, '2021-12-10'),
(102, 2002, 200, 750, 800, 7.30, '2023-05-12'),
(103, 3003, 150, 680, 750, 10.00, '2022-03-15'),
(104, 4001, 120, 600, 700, 12.50, '2023-07-20'),
(105, 5002, 180, 800, 850, 20.00, '2024-01-10'),
(101, 1002, 100, 200, 250, 30, '2020-12-29'),
(102, 2002, 100, 300, 250, 30, '2022-01-21'),
(103, 3003, 100, 300, 250, 30, '2022-02-02'),
(104, 4002, 100, 300, 250, 40, '2022-02-10'),
(105, 5002, 100, 150, 200, 50, '2022-03-12'),
(101, 1003, 100, 200, 250, 50, '2021-12-10'),
(101, 1003, 100, 200, 250, 40, '2023-05-12'),
(101, 1003, 100, 200, 250, 50, '2022-03-15'),
(101, 1003, 100, 200, 250, 50, '2023-07-20'),
(101, 1003, 100, 200, 250, 50, '2024-01-10'),
(105, 5003, 100, 150, 200, 50, '2024-01-10');

INSERT INTO QB.item (quantidadeItems, id_stock, dataEng, numero_encomenda) VALUES
(10, 1001,'2021-12-10', 1),
(15, 2002, '2023-05-12', 2),
(20, 3003, '2022-03-15', 3),
(25, 4001, '2023-07-20', 4),
(30, 5002, '2024-01-10', 5),
(14, 5003, '2024-01-10', 6);

INSERT INTO QB.garrafao (id_stock, dataEng) VALUES
(1001, '2021-12-10'),
(2002, '2023-05-12'),
(3003, '2022-03-15'),
(4001, '2023-07-20'),
(5002, '2024-01-10');

INSERT INTO QB.garrafa (id_tipoVinho, id_stock, dataEng) VALUES
(101, 1002, '2020-12-29'),
(102, 2002, '2022-01-21'),
(103, 3003, '2022-02-02'),
(104, 4002, '2022-02-10'),
(105, 5002, '2022-03-12'),
(105, 5002, '2024-01-10');

INSERT INTO QB.componente (id, quantidade) VALUES
(1001, 100),
(1002, 200),
(1003, 300),
(1004, 150),
(1005, 250);

INSERT INTO QB.rotulo (id_componente, NIF_cliente, notacao_tipoVinho) VALUES
(1001, 123456789, 'Grande Escolha'),
(1001, 987654321, 'Vinho Verde Rosado'),
(1001, 256986703, 'Vinho Frisante Branco'),
(1001, 234567890, 'Frisante Rosé'),
(1001, 345678901, 'Vinho Branco Tradicional');

INSERT INTO QB.tipoRolha (id, material, formato) VALUES
(21, 'Cortiça', 'Simples'),
(22, 'Cortiça', 'QB'),
(23, 'Metal', 'Carica'),
(24, 'Cortiça', 'Frizante');

INSERT INTO QB.rolha (id_componente, id_tipoRolha) VALUES
(1002, 21),
(1002, 22),
(1002, 23),
(1002, 24);

INSERT INTO QB.tipoRolha_fornecedor (id_tipoRolha, NIF, data, quantidade) VALUES
(21, 987654322, '2024-04-01', 2000),
(22, 256986503, '2024-04-02', 1500),
(23, 712983756, '2024-04-03', 1000),
(24, 837249200, '2024-04-04', 1800);


INSERT INTO QB.selo (id_componente, ano, categoria) VALUES
(1003, 2024, 'DOC'),
(1003, 2023, 'IGP'),
(1003, 2022, 'DOC'),
(1003, 2021, 'IGP'),
(1003, 2020, 'DOC');

INSERT INTO QB.certificados (id_componente, ano, associacao, titulo) VALUES
(1004, 2024, 'Wine Association', 'Quality Verified'),
(1004, 2023, 'Wine Association', 'Premium Quality'),
(1004, 2022, 'Wine Guild', 'Excellence Award'),
(1004, 2021, 'Vine Society', 'Top Choice'),
(1004, 2020, 'Winemakers Guild', 'Best Value');

INSERT INTO QB.caixa (numGarrafas, id_stock, dataEng, id_stock_garrafa) VALUES
(6, 1003, '2021-12-10', 1002),
(6, 1003, '2023-05-12', 1002),
(6, 1003, '2022-03-15', 1002),
(6, 1003, '2023-07-20', 1002),
(6, 1003, '2024-01-10', 1002),
(12, 5003, '2024-01-10', 5002);
