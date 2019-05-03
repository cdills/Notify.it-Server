var config = require('./parserConfig.js'); 
var snoowrap = require('snoowrap');
var sqlite = require('sqlite');
var Fuse = require('fuse.js');

const reddit = new snoowrap ({
    userAgent: config.userAgent,
    clientId: config.clientId,
    clientSecret: config.clientSecret,
    username: config.username,
    password: config.password
})

const fuseOptions = {
    shouldSort: true,
    includeMatches: true,
    threshold: 0.6,
    location: 0,
    distance: 100,
    maxPatternLength: 32,
    minMatchCharLength: 1,
    keys: [
      "title"
    ]
  };

var dbPromise = sqlite.open('./rsc/users.db', { Promise });

async function getUsers() {
    db = await dbPromise;
    result = await db.all( "SELECT ID, sub, query, udid FROM users Group BY sub, query, udid ORDER BY id")
    return result
    
}

async function downloadNewPost() {
    posts = await reddit.getSubreddit('rocketleagueexchange').getNew()
    return posts
}; 

async function parse () {
    var users = await getUsers()
    console.log(users);
    var newPosts = await downloadNewPost()
    users.forEach((user) => {

        var fuse = new Fuse(newPosts, fuseOptions)
        var result = fuse.search(user.query)
        result.forEach((post) => console.log(post.item.title))

        }
    )
};


parse();
