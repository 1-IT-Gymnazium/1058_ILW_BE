function login(username, password, callback) {
    const user_number = username;
    const bcrypt = require('bcrypt');
    const pg = require('pg');
    const conString = configuration.POSTGRE_URL;
    const pool = new pg.Pool({
      connectionString: conString,
      ssl: { rejectUnauthorized: false }
    });
    pool.connect(function (err, client, done) {
      if (err) return callback(err);
      const query = `
        SELECT id, password, "ISIC_id"
        FROM users
        WHERE user_number = $1
      `;
      client.query(query, [user_number], function (err, result) {
        done();
        if (err) return callback(err);
        if (result.rows.length === 0) return callback(new 	WrongUsernameOrPasswordError(user_number));
        const user = result.rows[0];
        if (!user.id) {
          return callback(new Error("User has no valid ID."));
        }
        const safeHash = user.password.replace('$2y$', '$2b$');
        bcrypt.compare(password, safeHash, function (err, isValid) {
          if (err) return callback(err);
          if (!isValid) return callback(new WrongUsernameOrPasswordError(user_number));
          const finalUserId = "ILW|" + String(user.id);
          return callback(null, {
            username: user_number,
            user_id: finalUserId,
            nickname: user.ISIC_id,
          });
        });
      });
    });
  }