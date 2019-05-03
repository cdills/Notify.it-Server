var express = require('express');
var router = express.Router();


/* GET users listing. */
router.get('/', function(req, res, next) {
  async function getUsers() {
    db = await dbPromise;
    return users = await db.get( "SELECT DISTINCT ID, sub, query, udid FROM users Group BY sub, query, udid ORDER BY id");
  }
  res.send(getUsers());
});

module.exports = router;
