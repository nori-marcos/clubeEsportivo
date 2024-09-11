----------------------------- Clube Esportivo -----------------------------

----------------------------- Setup  Database -----------------------------

-- O que seria passado para criar a role de DBA e o DB:
-- CREATE ROLE clube_dba WITH PASSWORD '1234567' CREATEDB LOGIN;
-- CREATE DATABASE db_clube_esportivo;

--------------------------------- Tabelas ---------------------------------


CREATE TABLE IF NOT EXISTS esportes
(
    id_esporte integer PRIMARY KEY,
    nome       varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS instalacoes
(
    id_instalacao    integer PRIMARY KEY,
    nome             varchar               NOT NULL,
    em_funcionamento boolean DEFAULT FALSE NOT NULL,
    capacidade       integer DEFAULT 0     NOT NULL
);

CREATE TABLE IF NOT EXISTS equipes
(
    id_equipe         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome              varchar NOT NULL,
    esporte_praticado integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados
(
    cpf               varchar(11) PRIMARY KEY,
    nome              varchar NOT NULL,
    foto              bytea,
    data_adesao       date    NOT NULL,
    data_nascimento   date    NOT NULL,
    endereco          varchar NOT NULL,
    email             varchar NOT NULL,
    associado_titular varchar(11),
    contrato          integer NOT NULL
);

CREATE TABLE IF NOT EXISTS associados_telefones
(
    associado varchar,
    telefone  varchar(13),
    PRIMARY KEY (associado, telefone)
);

CREATE TABLE IF NOT EXISTS atestados
(
    id_atestado              integer GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    associado                varchar NOT NULL REFERENCES associados (cpf) ON DELETE CASCADE,
    data_emissao             date    NOT NULL,
    data_validade            date    NOT NULL,
    emitido_pelo_funcionario varchar,
    PRIMARY KEY (id_atestado, associado)
);

CREATE TABLE IF NOT EXISTS contratos
(
    id_contrato  integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    data_inicio  date    NOT NULL,
    data_termino date    NOT NULL,
    plano        varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS pagamentos
(
    data_vencimento date           NOT NULL,
    contrato        integer        NOT NULL,
    valor           numeric(15, 2) NOT NULL,
    data_pagamento  date,
    PRIMARY KEY (data_vencimento, contrato)
);

CREATE TABLE IF NOT EXISTS planos
(
    nome  varchar PRIMARY KEY,
    valor numeric(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS eventos
(
    id_evento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome      varchar NOT NULL,
    data      date    NOT NULL,
    descricao varchar
);

CREATE TABLE IF NOT EXISTS funcionarios
(
    cpf             varchar(11) PRIMARY KEY,
    nome            varchar        NOT NULL,
    data_nascimento date           NOT NULL,
    data_admissao   date           NOT NULL,
    email           varchar        NOT NULL,
    salario         numeric(15, 2) NOT NULL,
    endereco        varchar        NOT NULL,
    cargo           integer        NOT NULL,
    departamento    integer        NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios_telefones
(
    funcionario varchar,
    telefone    varchar(13),
    PRIMARY KEY (funcionario, telefone)
);

CREATE TABLE IF NOT EXISTS departamentos
(
    id_departamento integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome            varchar NOT NULL,
    localizacao     integer
);

CREATE TABLE IF NOT EXISTS cargos
(
    id_cargo     integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    nome         varchar        NOT NULL,
    descricao    varchar        NOT NULL,
    salario_base numeric(15, 2) NOT NULL
);

----------------------------------- N-N -----------------------------------

CREATE TABLE IF NOT EXISTS associados_equipes
(
    associado varchar REFERENCES associados (cpf) ON DELETE CASCADE,
    equipe    integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (associado, equipe)
);

CREATE TABLE IF NOT EXISTS associados_eventos
(
    associado varchar REFERENCES associados (cpf) ON DELETE CASCADE,
    evento    integer REFERENCES eventos (id_evento),
    PRIMARY KEY (associado, evento)
);

CREATE TABLE IF NOT EXISTS equipes_eventos
(
    equipe integer REFERENCES equipes (id_equipe),
    evento integer REFERENCES eventos (id_evento),
    PRIMARY KEY (equipe, evento)
);

CREATE TABLE IF NOT EXISTS funcionarios_esportes
(
    funcionario varchar REFERENCES funcionarios (cpf),
    esporte     integer REFERENCES esportes (id_esporte),
    PRIMARY KEY (funcionario, esporte)
);

CREATE TABLE IF NOT EXISTS funcionarios_equipes
(
    funcionario varchar REFERENCES funcionarios (cpf),
    equipe      integer REFERENCES equipes (id_equipe),
    PRIMARY KEY (funcionario, equipe)
);

CREATE TABLE IF NOT EXISTS instalacoes_departamentos
(
    instalacao   integer REFERENCES instalacoes (id_instalacao),
    departamento integer REFERENCES departamentos (id_departamento),
    PRIMARY KEY (instalacao, departamento)
);

CREATE TABLE IF NOT EXISTS instalacoes_eventos
(
    instalacao integer REFERENCES instalacoes (id_instalacao),
    evento     integer REFERENCES eventos (id_evento),
    PRIMARY KEY (instalacao, evento)
);

CREATE TABLE IF NOT EXISTS instalacoes_esportes
(
    instalacao integer REFERENCES instalacoes (id_instalacao),
    esporte    integer REFERENCES esportes (id_esporte),
    PRIMARY KEY (instalacao, esporte)
);


-------------------------------- 1-N & FK --------------------------------

ALTER TABLE equipes
    ADD FOREIGN KEY (esporte_praticado) REFERENCES esportes (id_esporte) MATCH FULL;

ALTER TABLE associados
    ADD FOREIGN KEY (contrato) REFERENCES contratos (id_contrato) MATCH FULL;

ALTER TABLE associados
    ADD FOREIGN KEY (associado_titular) REFERENCES associados (cpf) MATCH FULL ON DELETE CASCADE;

ALTER TABLE associados_telefones
    ADD FOREIGN KEY (associado) REFERENCES associados (cpf) MATCH FULL ON DELETE CASCADE;

ALTER TABLE atestados
    ADD FOREIGN KEY (associado) REFERENCES associados (cpf) MATCH FULL;

ALTER TABLE atestados
    ADD FOREIGN KEY (emitido_pelo_funcionario) REFERENCES funcionarios (cpf) MATCH FULL;

ALTER TABLE contratos
    ADD FOREIGN KEY (plano) REFERENCES planos (nome) MATCH FULL;

ALTER TABLE pagamentos
    ADD FOREIGN KEY (contrato) REFERENCES contratos (id_contrato) MATCH FULL;

ALTER TABLE funcionarios
    ADD FOREIGN KEY (cargo) REFERENCES cargos (id_cargo) MATCH FULL;

ALTER TABLE funcionarios
    ADD FOREIGN KEY (departamento) REFERENCES departamentos (id_departamento) MATCH FULL;

ALTER TABLE funcionarios_telefones
    ADD FOREIGN KEY (funcionario) REFERENCES funcionarios (cpf) MATCH FULL;

ALTER TABLE departamentos
    ADD FOREIGN KEY (localizacao) REFERENCES instalacoes (id_instalacao) MATCH FULL;

-------------------------------- PROCEDURES --------------------------------

-- Procedimento para salvar um contrato, um associado e seus telefones
CREATE PROCEDURE salvar_contrato_associado_telefone(
    IN p_cpf varchar(11),
    IN p_nome varchar,
    IN p_email varchar,
    IN p_plano varchar,
    IN p_data_nascimento date,
    IN p_endereco varchar,
    IN p_foto bytea,
    IN p_telefones text[],
    IN p_associado_titular varchar(11))
    LANGUAGE plpgsql
AS
$$
DECLARE
    v_contrato integer;
    telefone   varchar(13);
BEGIN
    -- Primeiro, insere o contrato
    INSERT INTO contratos (data_inicio, data_termino, plano)
    VALUES (CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', p_plano)
    RETURNING id_contrato INTO v_contrato;

    -- Depois, insere o associado e salva o número do contrato
    INSERT INTO associados (cpf, nome, foto, data_adesao, data_nascimento, endereco, email, associado_titular, contrato)
    VALUES (p_cpf, p_nome, p_foto, CURRENT_DATE, p_data_nascimento, p_endereco, p_email, p_associado_titular,
            v_contrato);

    -- Adiciona o primeiro pagamento para daqui a 1 mês
    INSERT INTO pagamentos (data_vencimento, contrato, valor)
    VALUES (CURRENT_DATE + INTERVAL '1 month', v_contrato, (SELECT valor FROM planos WHERE nome = p_plano));

    -- Depois, insere os telefones em associados_telefones
    FOREACH telefone IN ARRAY p_telefones
        LOOP
            INSERT INTO associados_telefones (associado, telefone) VALUES (p_cpf, telefone);
        END LOOP;
END;
$$;

-- Procedimento para editar um contrato, um associado e seus telefones
CREATE PROCEDURE editar_contrato_associado_telefone(
    IN p_cpf varchar(11),
    IN p_nome varchar,
    IN p_email varchar,
    IN p_plano varchar,
    IN p_data_nascimento date,
    IN p_endereco varchar,
    IN p_foto bytea,
    IN p_telefones text[],
    IN p_associado_titular varchar(11))
    LANGUAGE plpgsql
AS
$$
DECLARE
    telefone                  varchar(13);
    v_associado_titular_antes varchar(11);
BEGIN
    -- Verifica se o associado era dependente e está sendo alterado para titular
    SELECT associado_titular
    INTO v_associado_titular_antes
    FROM associados
    WHERE cpf = p_cpf;

    IF v_associado_titular_antes IS NULL AND p_associado_titular IS NOT NULL THEN
        RAISE EXCEPTION 'Um titular não pode ser transformado em dependente. O associado deve ser excluído e cadastrado novamente como dependente.';
    END IF;

    -- Se o associado era dependente e está sendo alterado para titular
    IF v_associado_titular_antes IS NOT NULL AND p_associado_titular IS NULL THEN
        DELETE FROM associados
        WHERE cpf = p_cpf;

        CALL salvar_contrato_associado_telefone(
                p_cpf, p_nome, p_email, p_plano, p_data_nascimento,
                p_endereco, p_foto, p_telefones, p_associado_titular);

    ELSE
        -- Primeiro, atualiza o contrato
        UPDATE contratos
        SET plano = p_plano
        WHERE id_contrato = (SELECT contrato FROM associados WHERE cpf = p_cpf);

        -- Depois, atualiza os dados do associado
        IF p_nome IS NOT NULL THEN
            UPDATE associados
            SET nome = p_nome
            WHERE cpf = p_cpf
              AND nome IS DISTINCT FROM p_nome;
        END IF;

        IF p_email IS NOT NULL THEN
            UPDATE associados
            SET email = p_email
            WHERE cpf = p_cpf
              AND email IS DISTINCT FROM p_email;
        END IF;

        IF p_data_nascimento IS NOT NULL THEN
            UPDATE associados
            SET data_nascimento = p_data_nascimento
            WHERE cpf = p_cpf
              AND data_nascimento IS DISTINCT FROM p_data_nascimento;
        END IF;

        IF p_endereco IS NOT NULL THEN
            UPDATE associados
            SET endereco = p_endereco
            WHERE cpf = p_cpf
              AND endereco IS DISTINCT FROM p_endereco;
        END IF;

        IF p_foto IS NOT NULL THEN
            UPDATE associados
            SET foto = p_foto
            WHERE cpf = p_cpf
              AND foto IS DISTINCT FROM p_foto;
        END IF;

        -- Por fim, atualiza os telefones em associados_telefones
        DELETE FROM associados_telefones WHERE associado = p_cpf;
        FOREACH telefone IN ARRAY p_telefones
            LOOP
                INSERT INTO associados_telefones (associado, telefone) VALUES (p_cpf, telefone);
            END LOOP;
    END IF;
END;
$$;

-------------------------------- FUNCTION --------------------------------
CREATE FUNCTION verificar_pagamento_status(p_cpf varchar(11))
    RETURNS boolean
    LANGUAGE plpgsql
AS
$$
DECLARE
    v_associado_titular varchar(11);
    v_contrato          integer;
    v_status            boolean;
BEGIN
    -- Verifica se o associado é dependente ou titular
    SELECT associado_titular, contrato
    INTO v_associado_titular, v_contrato
    FROM associados
    WHERE cpf = p_cpf;

    -- Se for dependente, pegar o contrato do titular
    IF v_associado_titular IS NOT NULL THEN
        -- Dependente, verificar o pagamento do titular
        SELECT contrato
        INTO v_contrato
        FROM associados
        WHERE cpf = v_associado_titular;
    END IF;

    -- Lógica para verificar o status de pagamento
    SELECT CASE
               -- pagamento não realizado e ainda dentro do prazo de vencimento
               WHEN data_pagamento IS NULL AND data_vencimento > CURRENT_DATE THEN TRUE

               -- pagamento realizado e dentro do prazo de vencimento, status ativo
               WHEN data_pagamento IS NOT NULL AND data_pagamento <= data_vencimento THEN TRUE

               -- pagamento não realizado e fora do prazo de vencimento
               WHEN data_pagamento IS NULL AND data_vencimento < CURRENT_DATE THEN FALSE

               -- Caso 3: qualquer outro cenário, status suspenso
               ELSE FALSE
               END
    INTO v_status
    FROM pagamentos
    WHERE contrato = v_contrato;

    -- Retornar status (TRUE para ativo, FALSE para suspenso)
    RETURN v_status;
END;
$$;

------------------------------------------------- View -------------------------------------------------

CREATE VIEW associados_com_pagamento_pendente AS
    SELECT
    a.cpf AS cpf_associado,
    a.nome AS nome_associado,
    a.contrato,
    p.data_vencimento,
    p.data_pagamento,
    p.valor
    FROM pagamentos p
    LEFT JOIN associados a ON p.contrato = a.contrato
    LEFT JOIN contratos c ON c.id_contrato = a.contrato
    WHERE (p.data_pagamento IS NULL OR (
          p.data_vencimento >= p.data_pagamento)) AND (
          c.data_termino >= now())
