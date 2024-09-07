-- Mock data para o banco de dados

-- Inserir esportes
INSERT INTO esportes (id_esporte, nome)
VALUES (1, 'Futebol'),
       (2, 'Vôlei'),
       (3, 'Basquete'),
       (4, 'Tênis'),
       (5, 'Natação'),
       (6, 'Musculação');

-- Inserir equipes de esportes
INSERT INTO equipes (nome, esporte_praticado)
VALUES ('Time de futebol', 1),
       ('Time de vôlei', 2),
       ('Time de basquete', 3);

-- Inserir planos
INSERT INTO planos (nome, valor)
VALUES ('OURO', 100),
       ('PRATA', 80),
       ('BRONZE', 60);

-- Inserir instalações
INSERT INTO instalacoes (id_instalacao, nome, em_funcionamento, capacidade)
VALUES (1, 'Campo de futebol', TRUE, 100),
       (2, 'Quadra de vôlei', TRUE, 50),
       (3, 'Quadra de basquete', TRUE, 50),
       (4, 'Quadra de tênis', TRUE, 20),
       (5, 'Piscina', TRUE, 100),
       (6, 'Sala de musculação', TRUE, 50),
       (7, 'Prédio administrativo', TRUE, 100),
       (8, 'Salão de festas', TRUE, 100);

-- Inserir cargos
INSERT INTO cargos (nome, descricao, salario_base)
VALUES ('Gerente', 'Gerente de departamento', 5000),
       ('Médico', 'Médico do clube', 10000),
       ('Treinador', 'Treinador de futebol', 2000),
       ('Secretária', 'Secretária', 1500),
       ('Auxiliar', 'Auxiliar de serviços gerais', 1200);

-- Inserir departamentos
INSERT INTO departamentos (nome, localizacao)
VALUES ('Administrativo', 7),
       ('Enfermaria', 7),
       ('Financeiro', 7),
       ('RH', 7),
       ('Marketing', 7),
       ('Comercial', 7),
       ('Técnico', 7),
       ('Serviços Gerais', 7);

-- função para setar o salário do funcionário de acordo com o cargo
CREATE OR REPLACE FUNCTION set_salario_from_cargo()
    RETURNS TRIGGER AS
$$
BEGIN
    SELECT salario_base
    INTO NEW.salario
    FROM cargos
    WHERE id_cargo = NEW.cargo;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- trigger para setar o salário do funcionário de acordo com o cargo
CREATE TRIGGER trigger_set_salario
    BEFORE INSERT OR UPDATE
    ON funcionarios
    FOR EACH ROW
EXECUTE FUNCTION set_salario_from_cargo();

-- Inserir funcionários com seus respectivos cargos e departamentos
INSERT INTO funcionarios (cpf, nome, data_nascimento, data_admissao, email, endereco, cargo, departamento)
VALUES
    -- Gerente (cargo 1)
    ('18764329840', 'Bruno Henrique dos Santos',
     '1985-12-12', '2020-05-15', 'bruno_henrique@gerentedept.com.br',
     'Rua 7', 1, 1),
    -- Médico (cargo 2)
    ('43578019423', 'Camila Vitória de Souza',
     '1980-07-21', '2019-02-20', 'camila_souza@medicoclube.com.br',
     'Rua 8', 2, 2),
    -- Treinador (cargo 3)
    ('51069921505', 'Lorena Sueli de Paula',
     '1990-01-01', '2021-01-01', 'lorena_sueli_depaula@numero.com.br',
     'Rua 4', 3, 7),
    -- Secretária (cargo 4)
    ('93080334914', 'Helena Betina Amanda da Cruz',
     '1990-01-01', '2021-01-01', 'helena_betina_dacruz@openlink.com.br',
     'Rua 5', 4, 1),
    -- Auxiliar (cargo 5)
    ('38500193220', 'Pietro Kauê Bryan Ramos',
     '1990-01-01', '2021-01-01', 'pietro_ramos98@jcffactoring.com.br',
     'Rua 6', 5, 8);

-- Inserir telefones dos funcionários
INSERT INTO funcionarios_telefones (funcionario, telefone)
VALUES
    -- Gerente
    ('18764329840', '11936206470'),
    ('18764329840', '11983373870'),
    -- Médico
    ('43578019423', '62925689899'),
    ('43578019423', '62989833544'),
    -- Treinador
    ('51069921505', '95936357066'),
    ('51069921505', '95994109007'),
    -- Secretária
    ('93080334914', '11936206470'),
    ('93080334914', '11983373870'),
    -- Auxiliar
    ('38500193220', '62925689899'),
    ('38500193220', '62989833544');

-- Inserir contratos e associados
INSERT INTO contratos (data_inicio, data_termino, plano)
VALUES ('2021-01-01', '2021-12-31', 'OURO'),
       ('2021-01-01', '2021-12-31', 'PRATA'),
       ('2021-01-01', '2021-12-31', 'BRONZE'),
       ('2021-01-01', '2021-12-31', 'OURO'),
       ('2021-01-01', '2021-12-31', 'PRATA'),
       ('2021-01-01', '2021-12-31', 'BRONZE');

INSERT INTO associados (cpf, nome, foto, data_adesao, data_nascimento, endereco, email, associado_titular, contrato)
VALUES ('02039461388', 'Simone Beatriz da Luz', 'foto',
        '2021-01-01', '1990-01-01', 'Rua 1', 'simone_daluz@fosj.unesp.br',
        NULL, 1),
       ('42331337322', 'Ester Regina da Rocha', 'foto',
        '2021-01-01', '1990-01-01', 'Rua 2', 'ester_regina_darocha@schon.com.br',
        '02039461388', 2),
       ('87166405600', 'Tânia Sara da Luz', 'foto',
        '2021-01-01', '1990-01-01', 'Rua 3', 'tania-daluz95@jp.ind.br',
        NULL, 3),
       ('20703896695', 'Márcia Maya Almada',
        'foto', '2021-01-01', '1990-01-01', 'Rua 4', 'marcia_almada@i9tec.com.br',
        NULL, 4),
       ('48169743346', 'Isaac Erick Dias', 'foto',
        '2021-01-01', '1990-01-01', 'Rua 5', 'isaac_erick_dias@wnetrj.com.br',
        '02039461388', 5),
       ('28373246711', 'João Pedro da Silva', 'foto',
        '2021-01-01', '1990-01-01', 'Rua 6', 'joao@email.com',
        '20703896695', 6);

-- Inserir telefones dos associados
INSERT INTO associados_telefones (associado, telefone)
VALUES
    -- Telefones para Simone Beatriz da Luz (02039461388)
    ('02039461388', '11936206470'),
    ('02039461388', '11983373870'),

    -- Telefones para Ester Regina da Rocha (42331337322)
    ('42331337322', '62925689899'),
    ('42331337322', '62989833544'),

    -- Telefones para Tânia Sara da Luz (87166405600)
    ('87166405600', '95936357066'),
    ('87166405600', '95994109007'),

    -- Telefones para Márcia Maya Almada (20703896695)
    ('20703896695', '21987654321'),
    ('20703896695', '21912345678'),

    -- Telefones para Isaac Erick Dias (48169743346)
    ('48169743346', '31987654321'),
    ('48169743346', '31912345678'),

    -- Telefones para João Pedro da Silva (28373246711)
    ('28373246711', '79925716702'),
    ('28373246711', '79984153381');

-- Inserir atestados
INSERT INTO atestados (associado, data_emissao, data_validade, emitido_pelo_funcionario)
VALUES ('02039461388', '2021-01-01', '2022-01-01', '43578019423'),
       ('42331337322', '2021-01-01', '2022-01-01', '43578019423'),
       ('87166405600', '2021-01-01', '2022-01-01', '43578019423');

-- Inserir pagamentos
INSERT INTO pagamentos (data_vencimento, contrato, valor, data_pagamento)
VALUES ('2021-01-01', 1, 100, '2021-01-01'),
       ('2021-01-01', 2, 80, '2021-01-01'),
       ('2021-01-01', 3, 60, '2021-01-01');

-- Inserir eventos
INSERT INTO eventos (nome, data, descricao)
VALUES ('Campeonato de Futebol', '2021-01-01', 'Campeonato de futebol do clube'),
       ('Campeonato de Vôlei', '2021-01-01', 'Campeonato de vôlei do clube'),
       ('Festa de Aniversário', '2021-01-01', 'Festa de aniversário do clube');

-- INSERIR DADOS PARA RELACIONAMENTOS N:N

-- Inserir associados nas equipes
INSERT INTO associados_equipes (associado, equipe)
VALUES
    -- Simone Beatriz da Luz (Futebol)
    ('02039461388', 1),
    -- Márcia Maya Almada (Futebol)
    ('20703896695', 1),
    -- Isaac Erick Dias (Futebol)
    ('48169743346', 1),
    -- Tânia Sara da Luz (Futebol)
    ('87166405600', 1),

    -- Ester Regina da Rocha (Vôlei)
    ('42331337322', 2),
    -- Tânia Sara da Luz (Vôlei)
    ('87166405600', 2),
    -- Isaac Erick Dias (Vôlei)
    ('48169743346', 2),
    -- Simone Beatriz da Luz (Vôlei)
    ('02039461388', 2),

    -- Simone Beatriz da Luz (Basquete)
    ('02039461388', 3),
    -- Ester Regina da Rocha (Basquete)
    ('42331337322', 3),
    -- Tânia Sara da Luz (Basquete)
    ('87166405600', 3),
    -- Márcia Maya Almada (Basquete)
    ('20703896695', 3),
    -- Isaac Erick Dias (Basquete)
    ('48169743346', 3);

-- Inserir associados nos eventos
INSERT INTO associados_eventos (evento, associado)
VALUES
    -- Campeonato de Futebol (Evento 1)
    -- Simone Beatriz da Luz
    (1, '02039461388'),
    -- Márcia Maya Almada
    (1, '20703896695'),
    -- Isaac Erick Dias
    (1, '48169743346'),
    -- Tânia Sara da Luz
    (1, '87166405600'),

    -- Campeonato de Vôlei (Evento 2)
    -- Ester Regina da Rocha
    (2, '42331337322'),
    -- Tânia Sara da Luz
    (2, '87166405600'),
    -- Isaac Erick Dias
    (2, '48169743346'),
    -- Simone Beatriz da Luz
    (2, '02039461388'),

    -- Festa de Aniversário (Evento 3)
    -- Simone Beatriz da Luz
    (3, '02039461388'),
    -- Ester Regina da Rocha
    (3, '42331337322'),
    -- Tânia Sara da Luz
    (3, '87166405600'),
    -- Márcia Maya Almada
    (3, '20703896695'),
    -- Isaac Erick Dias
    (3, '48169743346'),
    -- João Pedro da Silva
    (3, '28373246711');

-- Inserir equipes nos eventos
INSERT INTO equipes_eventos (equipe, evento)
VALUES
    -- Campeonato de Futebol (Evento 1)
    -- Time de futebol
    (1, 1),

    -- Campeonato de Vôlei (Evento 2)
    -- Time de vôlei
    (2, 2);

-- Inserir funcionários nos esportes
INSERT INTO funcionarios_esportes (funcionario, esporte)
VALUES
    -- Treinadora Lorena Sueli de Paula (Futebol)
    ('51069921505', 1),
    -- Treinadora Lorena Sueli de Paula (Vôlei)
    ('51069921505', 2),
    -- Treinadora Lorena Sueli de Paula (Basquete)
    ('51069921505', 3);

-- Inserir funcionários nas equipes
INSERT INTO funcionarios_equipes (funcionario, equipe)
VALUES
    -- Treinadora Lorena Sueli de Paula (Time de futebol)
    ('51069921505', 1),
    -- Treinadora Lorena Sueli de Paula (Time de vôlei)
    ('51069921505', 2),
    -- Treinadora Lorena Sueli de Paula (Time de basquete)
    ('51069921505', 3);

-- Inserir instalações nos departamentos
INSERT INTO instalacoes_departamentos (instalacao, departamento)
VALUES
    -- Administrativo
    (7, 1),
    -- Enfermaria
    (7, 2),
    -- Financeiro
    (7, 3),
    -- RH
    (7, 4),
    -- Marketing
    (7, 5),
    -- Comercial
    (7, 6),
    -- Técnico
    (7, 7);

-- Inserir instalações nos eventos
INSERT INTO instalacoes_eventos (instalacao, evento)
VALUES
    -- Campeonato de Futebol
    (3, 1),
    -- Campeonato de Vôlei
    (1, 2),
    -- Festa de Aniversário
    (5, 3);

-- Inserir instalações dos esportes
INSERT INTO instalacoes_esportes (esporte, instalacao)
VALUES
    -- Futebol
    (1, 1),
    -- Vôlei
    (2, 2),
    -- Basquete
    (3, 3),
    -- Tênis
    (4, 4),
    -- Natação
    (5, 5),
    -- Musculação
    (6, 6);