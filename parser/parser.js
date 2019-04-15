var config = require('./parserConfig.js'); 
var snoowrap = require('snoowrap');


const reddit = new snoowrap ({
    userAgent: config.userAgent,
    clientId: config.clientId,
    clientSecret: config.clientSecret,
    username: config.username,
    password: config.password
})

reddit.getSubreddit('all').getNew.map(post => post.title).then(console.log);