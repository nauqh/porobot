create table
    if not exists summoners (
        s_id text PRIMARY KEY, -- Summoner puuid
        s_name text not null, -- Summoner name
        s_region text not null, -- Summoner region
        s_url text not null -- Summoner opgg url
    );

create table
    if not exists matches (
        m_id text PRIMARY KEY, -- Match id
        m_date text not null, -- Match date
        m_duration integer not null -- Match duration (ms)
    );

create table
    if not exists performs (
        s_id text not null, -- Summoner id
        m_id text not null, -- Match id
        p_stats blob not null, -- Summoner performance (json)
        PRIMARY KEY (s_id, m_id),
        FOREIGN KEY (s_id) REFERENCES summoners (s_id) ON DELETE CASCADE,
        FOREIGN KEY (m_id) REFERENCES matches (m_id) ON DELETE CASCADE
    );
