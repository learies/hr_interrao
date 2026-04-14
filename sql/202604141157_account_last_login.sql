-- Migration: 202604141157_account_last_login
-- Description: Создание таблицы last_login для хранения времени последнего входа пользователя
-- Created: 2026-04-14

CREATE TABLE IF NOT EXISTS account.last_login (
    user_id UUID PRIMARY KEY,
    last_login TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_last_login_user
        FOREIGN KEY (user_id)
        REFERENCES account."user"(id)
        ON DELETE CASCADE
);

COMMENT ON TABLE account.last_login IS 'Модель последнего входа пользователя';
COMMENT ON COLUMN account.last_login.user_id IS 'Идентификатор пользователя';
COMMENT ON COLUMN account.last_login.last_login IS 'Время последнего входа';