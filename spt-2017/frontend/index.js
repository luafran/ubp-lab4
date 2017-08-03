var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var request = require('request');
var handlebars = require('express-handlebars')
    .create({ defaultLayout:'main' });

var Log = require('log')
var log = new Log('info');

var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.use(session({
    secret: 'mys3cr3t',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}));

/** HOME **/

app.get('/', function (req, res) {
    var sess = req.session
    if (sess.token) {
        res.redirect('/home')
    }
    else {
        res.redirect('/login');
    }
});

app.get('/home', function(req, res) {

    var sess = req.session
    if (!sess.token) {
        res.redirect('/login');
        return;
    }

    var options = {
      uri: 'http://jobs-frontend-svc:8082/jobs',
      method: 'GET',

      headers: {
        "Accept": "application/json",
        "Authorization": "Bearer " + sess.token
      },

      json: {}
    };

    request(options, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        log.info(body);
        log.debug(body.jobs);
      }
    });

    res.render('home')
});

/** REGISTER **/

app.get('/register', function(req, res) {
    res.render('register')
});

app.get('/register/:id', function(req, res) {
    var id = req.params.id;
    res.render('register',{error_message: "USER ALREADY EXISTS"})
});

app.post('/register', function(req, res) {
    var username = req.body.username;
    var password = req.body.password;

    var options = {
      uri: 'http://auth-svc:8081/register',
      method: 'POST',

      headers: {
        "Content-type": "application/json"
      },

      json: {
        "username": username,
        "password": password
      }
    };

    request(options, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        log.info(body);
        if(body.status == "OK") {
            res.render("home");
        } else {
            res.redirect("/register/1");
        }
      }
    });
});


/** LOGIN **/

app.get('/login', function(req, res) {
    res.render('login')
});

app.get('/login/:id', function(req, res) {
    var id = req.params.id;
    res.render('login',{error_message: "AUTHENTICATION ERROR"})
});

app.post('/login', function(req, res) {
    var username = req.body.username;
    var password = req.body.password;

    var sess = req.session
    var options = {
      uri: 'http://auth-svc:8081/login',
      method: 'POST',

      headers: {
        "Content-type": "application/json"
      },

      json: {
        "username": username,
        "password": password
      }
    };

    request(options, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        log.info(body);
        if(body.status == "OK") {
            sess.token = body.token
            res.redirect('/home');
        } else {
            res.redirect("/login/1");
        }
      }
    });
});


app.get('/createjob', function(req, res) {
    res.render('upload');
});

/** TEST **/

app.get('/test', function(req, res) {

    var sess = req.session
    if (!sess.token) {
        res.redirect('/login');
        return;
    }

    var options = {
      uri: 'http://auth-svc:8081/test',
      method: 'GET',

      headers: {
        "Content-type": "application/json",
        "Authorization": "Bearer " + sess.token
      },

      json: {}
    };

    request(options, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        log.info(body);
        if(body.status == "OK") {
            res.redirect("/home");
        } else {
            res.redirect("/register/1");
        }
      }
    });

});

/** SERVER **/

var server = app.listen(8080, '0.0.0.0', function () {
  var host = server.address().address;
  var port = server.address().port;

  log.info("frontend listening at http://%s:%s", host, port);
});
