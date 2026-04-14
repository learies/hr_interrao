-- Migration: 202604141155_account_user
-- Description: Создание схемы account и таблицу user
-- Created: 2026-04-14

CREATE SCHEMA IF NOT EXISTS account;

COMMENT ON SCHEMA account IS 'Схема для данных учетных записей пользователей';

CREATE TABLE IF NOT EXISTS account."user" (
    id UUID PRIMARY KEY,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE account."user" IS 'Модель пользователя';
COMMENT ON COLUMN account."user".id IS 'Идентификатор пользователя';
COMMENT ON COLUMN account."user".is_admin IS 'Права администратора';