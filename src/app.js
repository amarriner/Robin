// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';
let response;

const chowdown = require("chowdown");
const keys = require("./keys.json");
const Twitter = require('twitter');

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html 
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 * 
 */
exports.lambdaHandler = async (event, context) => {

    //
    // Base URL to get idioms from
    //
    const idiomBase = "http://www.idiomconnection.com";

    try {

        var idiom = formatIdiom(await getLink(idiomBase)
                            .then(getIdioms)
                            .then(getIdiom));

        var client = new Twitter({
            consumer_key: keys.consumerKey,
            consumer_secret: keys.consumerSecret,
            access_token_key: keys.accessToken,
            access_token_secret: keys.accessTokenSecret
        });

        client.post('statuses/update', { 
            status: idiom 
        }, function (error, tweet, response) {

            if (error) {
                return console.log(error);
            }

            console.log(tweet);

        });
                              
        // const ret = await axios(url);
        response = { 
            'statusCode': 200,
            'body': JSON.stringify({
                message: idiom,
                // location: ret.data.trim()
            })
        };
        
    } catch (err) {
        console.log(err);
        return err;
    }

    console.log(response);
    return response;

};

//
// Get a random entry in an array
//
function randomChoice(array) {

    return array[Math.floor(array.length * Math.random())];

}

//
// Function to get a link from the idiom website
//
function getLink(url) {

    //
    // Fetch the HTML from the idiom webpage, and then parse
    // the UL elements and strip the HREF attribute from the 
    // A tags within to get an array of possible links. Pick
    // one to get an idiom from
    //
    return chowdown(url)
        .collection("ul li", {
            "href": "a/href"
        });

}

//
// Function to get idioms from the link chosen by the getLink function
//
function getIdioms(links) {

    //
    // Fetch the HTML for a random link in the links parameter,
    // then parse it for all the B tags to get an idiom
    //
    return chowdown(randomChoice(links).href)
        .collection("b");

}

//
// Function to choose a random idiom from the collection returned by getIdioms
//
function getIdiom(idioms) {

    return randomChoice(idioms);

}

//
// Function to format an idiom to strip out some unnecessary words/punctuation
// as well as add the Holy ____ Batman template
//
function formatIdiom(inputIdiom) {

    var idiom = inputIdiom;

    //
    // Sometimes the idiom is one thing OR another, pick one
    //
    if (idiom.toLowerCase().split(' <i>or</i> ').length) {
        idiom = randomChoice(idiom.toLowerCase().split(' <i>or</i> '));
    }

    //
    // Some idioms have two words separated by a slash, we should pick one of those words to use
    //
    var str = "", word, i;

    for (i = 0; i < idiom.split(" ").length; i++) {
        
        word = idiom.split(" ")[i];

        if (idiom.split(" ")[i].split("/") && idiom.split(" ")[i].split("/").length > 1) {

            word = randomChoice(idiom.split(" ")[i].split('/'));

        }

        console.log(word);

        if (str && str.length) {
            str += " ";
        }

        str += word;

    }

    idiom = str;

    //
    // Replace (someone's) or one's with your
    //
    idiom = idiom.replace("one's", "your");
    idiom = idiom.replace("(someone's)", "your");

    //
    // Strip leading "A " if it exists
    //
    if (idiom.substring(0, 2) == "A ") {
        idiom = idiom.substring(2, idiom.length - 2);
    }

    //
    // Remove anything inside parentheses
    //
    idiom = idiom.replace(/\(.*?\)/g, "");

    //
    // Sometimes the previous regex will leave two spaces in a row and since I suck too much with regexes to do
    // this all in one step, I'll strip them out here
    //
    idiom = idiom.replace("  ", " ");

    //
    // Remove most punctuation
    //
    idiom = idiom.replace(/[^A-Za-z0-9 -\']/g, "");
     
    return "Holy " + idiom.toLowerCase() + ", Batman!";

}