--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.1 (Debian 16.1-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    id integer NOT NULL,
    name character varying(50),
    surname character varying(50),
    email character varying(50),
    phone character varying(50),
    description character varying(250),
    birth_date date NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    user_id integer
);


ALTER TABLE public.contacts OWNER TO postgres;

--
-- Name: contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contacts_id_seq OWNER TO postgres;

--
-- Name: contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_id_seq OWNED BY public.contacts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(150) NOT NULL,
    password character varying(255) NOT NULL,
    refresh_token character varying(255),
    avatar character varying(255),
    confirmed boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts ALTER COLUMN id SET DEFAULT nextval('public.contacts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
1c7b22f94094
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (id, name, surname, email, phone, description, birth_date, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password, refresh_token, avatar, confirmed) FROM stdin;
5	dsasdasd111	wiyayo9176@flexvio.com	$2b$12$ob0GNYqX4qL9bLjlF.W15ONvO6/ONV/UYuCHE6g/2PLlDOo57FSw6	\N	https://www.gravatar.com/avatar/0e476f5c1e62b0a6925659d684ff934b	f
6	dsasdasd1111	nolef94889@gosarlar.com	$2b$12$ztKZgBWLQDs5eEcoIgLBkerzfBuGNiIum5zK7Ohi.ohLFwoBpv/ga	\N	https://www.gravatar.com/avatar/5b80dc69f6f94757c99af8bdaed96de8	f
7	dsasdasd1111	brawlpochtavi@gmail.com	$2b$12$RR7pUBzojrwv1Jwpw99Oju1l74shYkTtMs6xSl.9DmrC4jcHDAELO	\N	https://www.gravatar.com/avatar/9291925f28b8a8f53219f148f1cb4ac2	f
8	string223312	user11@example.com	$2b$12$W2g4su0nH6GgcBr7kdBZjeKC/NTHRtTRVyT/2ma44HsUb4gu19Pqu	\N	https://www.gravatar.com/avatar/ad6d67d0c4495e186010732a7d360028	f
9	11string	user1231@example.com	$2b$12$gBhh1Q80atvGy9K/L9snMe50NOy97e42ynNEqLNyYqrMNb/VrHEuC	\N	https://www.gravatar.com/avatar/0ab6d584554c369dc9af1459ff39eac2	f
10	11string	rijejat345@flexvio.com	$2b$12$nUJJa4u.T3im0pU31Iv.0etXLUFB.T7rhzhsJW3Vci2bdkf93Bpbq	\N	https://www.gravatar.com/avatar/adbf7911b66daed07e81479b7d433f96	t
\.


--
-- Name: contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: contacts contacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

