-- Extensiones opcionales
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- CREATE EXTENSION IF NOT EXISTS pgcrypto; -- para uuid_random()

-- Usuarios del sistema
CREATE TABLE app_user (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
email text UNIQUE NOT NULL,
password_hash text NOT NULL,
role text NOT NULL CHECK (role IN ('user','provider','admin')),
created_at timestamptz NOT NULL DEFAULT now(),
is_active boolean NOT NULL DEFAULT true
);

Perfiles (proveedoras)
CREATE TABLE profile (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
user_id -- uuid NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
alias text NOT NULL,
barrio text NOT NULL,
price_from_eur integer NOT NULL CHECK (price_from_eur >= 0),
languages text[] NOT NULL DEFAULT '{}',
schedule_slot text NOT NULL CHECK (schedule_slot IN ('mañana','tarde','noche')),
lat numeric(9,6),
lng numeric(9,6),
verified boolean NOT NULL DEFAULT false,
description text,
created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_profile_barrio ON profile(barrio);

-- Reseñas
CREATE TABLE review (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
author_user_id uuid NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
profile_id uuid NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
rating smallint NOT NULL CHECK (rating BETWEEN 1 AND 5),
body text NOT NULL,
created_at timestamptz NOT NULL DEFAULT now(),
is_visible boolean NOT NULL DEFAULT true
);
CREATE UNIQUE INDEX uniq_review_once ON review(author_user_id, profile_id);

-- Votos/Útil (evita spam)
CREATE TABLE review_vote (
user_id uuid NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
review_id uuid NOT NULL REFERENCES review(id) ON DELETE CASCADE,
is_helpful boolean NOT NULL,
PRIMARY KEY (user_id, review_id)
);

-- Reportes (notice & action)
CREATE TABLE report_ticket (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
target_type text NOT NULL CHECK (target_type IN ('profile','review')),
target_id uuid NOT NULL,
reporter_id uuid REFERENCES app_user(id) ON DELETE SET NULL,
reason text NOT NULL,
created_at timestamptz NOT NULL DEFAULT now(),
status text NOT NULL DEFAULT 'open' CHECK (status IN ('open','under_review','closed'))
);

-- Acciones de moderación
CREATE TABLE moderation_action (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
ticket_id uuid REFERENCES report_ticket(id) ON DELETE SET NULL,
actor_id uuid REFERENCES app_user(id),
action text NOT NULL, -- hide_profile, hide_review, warn_user, ban_user
notes text,
created_at timestamptz NOT NULL DEFAULT now()
);

-- Logs DSA (tomas de decisiones de retirada/transparencia)
CREATE TABLE dsa_event (
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
kind text NOT NULL, -- notice_received, content_removed, appeal_received, appeal_upheld
target_type text NOT NULL,
target_id uuid,
payload jsonb NOT NULL,
created_at timestamptz NOT NULL DEFAULT now()
);

-- Sesiones/JWT revocados (si aplicas invalidación)
CREATE TABLE revoked_token (
jti text PRIMARY KEY,
revoked_at timestamptz NOT NULL DEFAULT now()
);