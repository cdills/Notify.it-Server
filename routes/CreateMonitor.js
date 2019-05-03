var express = require('express');
var router = express.Router();
var sqlite = require('sqlite');


var dbPromise = sqlite.open('./rsc/users.db', { Promise });

router.post('/', async function(req, res,) {
    try {
        const db = await dbPromise;
        const result = await db.run("INSERT INTO users (id, sub, query, udid) VALUES " + ` (null, "${req.query.sub}", "${req.query.text}", "${req.query.udid} ") `)
        res.send({"result": `${result.changes}`})
    } catch (err) {
        console.log(err)
        res.sendStatus(500)
    };
})

module.exports = router;