WITH ins AS (
    INSERT INTO users (id, username, email, password)
    VALUES (:user_id, :username, :email, :password)
    ON CONFLICT (username) DO NOTHING
    RETURNING id
)
INSERT INTO refresh_jwts (user_id, token, token_expire)
SELECT ins.id, unnest(:tokens), unnest(CAST(:expires) as TIMESTAMP WITH TIME ZONE)
FROM ins