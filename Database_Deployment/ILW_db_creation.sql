CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    surname VARCHAR(30),
    ISIC_id VARCHAR,
    user_number INTEGER,
    password VARCHAR
);
CREATE TABLE public.meals (
    id SERIAL PRIMARY KEY,
    meal_number INTEGER,
    name VARCHAR,
    date DATE
);
CREATE TABLE public.orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    status BOOLEAN,
    withdrawed_at TIMESTAMP WITHOUT TIME ZONE,

CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES public.users(id) ON DELETE CASCADE,
CONSTRAINT fk_meal FOREIGN KEY(meal_id) REFERENCES public.meals(id) ON DELETE CASCADE
);